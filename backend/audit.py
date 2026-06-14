#!/usr/bin/env python3
"""
McGill Degree Requirements Audit
=================================
Compares every program seeded in Supabase against the live McGill course
catalogue (coursecatalogue.mcgill.ca).

Usage
-----
    pip install httpx supabase anthropic beautifulsoup4 rich
    python audit_degree_requirements.py

    # Limit to one faculty while testing:
    python audit_degree_requirements.py --faculty "Faculty of Engineering"

    # Audit a single program by key:
    python audit_degree_requirements.py --program-key cs_major_bsc

    # Write results to a CSV file as well:
    python audit_degree_requirements.py --csv results.csv

Environment variables required (same as your backend):
    SUPABASE_URL
    SUPABASE_SERVICE_ROLE_KEY   (or SUPABASE_KEY)
    ANTHROPIC_API_KEY

How it works
------------
For each program in the database the script:
  1. Reads the program row and all its requirement_blocks + block_courses
     straight from Supabase (source-of-truth for what you seeded).
  2. Fetches the programme's ecalendar_url with httpx and sends the raw HTML
     to Claude (claude-sonnet-4-5) together with a structured description of
     what you have in the DB.
  3. Claude returns a JSON diff: missing courses, extra courses, credit
     mismatches, title mismatches, etc.
  4. Results are printed with rich and optionally written to CSV.
"""

import argparse
import csv
import json
import os
import sys
import textwrap
import time
from typing import Optional

import anthropic
import httpx
from bs4 import BeautifulSoup
from rich.console import Console
from rich.table import Table
from rich import print as rprint
from supabase import create_client

console = Console()

# ── Configuration ─────────────────────────────────────────────────────────────

REQUEST_DELAY = 1.0          # seconds between catalogue fetches (be polite)
MAX_HTML_CHARS = 20_000      # truncate very large pages before sending to Claude
CLAUDE_MODEL   = "claude-haiku-4-5-20251001"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (compatible; McGill-Audit-Bot/1.0; "
        "academic research use)"
    ),
    "Accept-Language": "en-CA,en;q=0.9",
}


# ── Supabase helpers ──────────────────────────────────────────────────────────

def load_programs_from_db(
    supabase,
    faculty: Optional[str] = None,
    program_key: Optional[str] = None,
    program_keys: Optional[list[str]] = None,
) -> list[dict]:
    """Return program rows with their blocks and courses expanded."""
    q = supabase.table("degree_programs").select(
        "id, program_key, name, faculty, program_type, total_credits, ecalendar_url"
    )
    if faculty:
        q = q.eq("faculty", faculty)
    if program_key:
        q = q.eq("program_key", program_key)
    if program_keys:
        q = q.in_("program_key", program_keys)
    programs = q.order("faculty").order("name").execute().data or []

    for prog in programs:
        blocks = (
            supabase.table("requirement_blocks")
            .select("id, block_key, title, block_type, credits_needed, courses_needed, notes")
            .eq("program_id", prog["id"])
            .order("sort_order")
            .execute()
            .data or []
        )
        for block in blocks:
            courses = (
                supabase.table("requirement_courses")
                .select("subject, catalog, title, credits, is_required")
                .eq("block_id", block["id"])
                .execute()
                .data or []
            )
            block["courses"] = courses
        prog["blocks"] = blocks

    return programs


# ── Catalogue fetching ────────────────────────────────────────────────────────

def fetch_catalogue_page(url: str) -> tuple[str, str]:
    """
    Fetch the ecalendar page and return (clean_text, error_message).
    clean_text is empty on error; error_message is empty on success.
    """
    if not url:
        return "", "No ecalendar_url stored for this program."
    try:
        resp = httpx.get(url, headers=HEADERS, timeout=15, follow_redirects=True)
        resp.raise_for_status()
    except httpx.HTTPStatusError as exc:
        return "", f"HTTP {exc.response.status_code} fetching {url}"
    except Exception as exc:
        return "", f"Network error fetching {url}: {exc}"

    soup = BeautifulSoup(resp.text, "html.parser")

    # Remove nav / footer noise so Claude focuses on the course content
    for tag in soup.select("nav, footer, header, script, style, .breadcrumb, #menu"):
        tag.decompose()

    # Try to grab just the main content area if it exists
    main = soup.select_one("main") or soup.select_one(".main-content") or soup.body
    text = main.get_text(separator="\n", strip=True) if main else soup.get_text(separator="\n", strip=True)

    # Collapse blank lines
    lines = [l for l in text.splitlines() if l.strip()]
    clean = "\n".join(lines)

    return clean[:MAX_HTML_CHARS], ""


# ── Claude audit ──────────────────────────────────────────────────────────────

def build_db_summary(prog: dict) -> str:
    """Build a compact text representation of what we have in the DB."""
    lines = [
        f"Program: {prog['name']}",
        f"Faculty: {prog['faculty']}",
        f"Type: {prog['program_type']}",
        f"Total credits (DB): {prog['total_credits']}",
        "",
        "Requirement blocks and courses stored in our database:",
    ]
    for block in prog.get("blocks", []):
        lines.append(
            f"\n  Block: {block['title']} "
            f"[{block['block_type']}, credits_needed={block['credits_needed']}]"
        )
        for c in block.get("courses", []):
            req = "REQUIRED" if c.get("is_required") else "optional"
            code = f"{c['subject']} {c['catalog']}" if c.get("catalog") else c["subject"]
            lines.append(f"    - {code}: {c['title']} ({c['credits']} cr) [{req}]")
    return "\n".join(lines)


SYSTEM_PROMPT = textwrap.dedent("""
    You are an academic data auditor for McGill University.
    You will be given:
      1. A summary of what a McGill program looks like in our database.
      2. The raw text scraped from the official McGill course catalogue page for that program.

    Your job is to compare them and return a JSON object describing discrepancies.
    Be thorough but precise — only flag genuine differences, not formatting variations.

    IMPORTANT: Keep each "detail" string under 120 characters. Be terse.
    If there are more than 20 issues, summarise groups of similar issues into one entry.

    Return ONLY a valid JSON object (no markdown, no code fences, no preamble):
    {
      "catalogue_credits": <integer or null if not clearly stated>,
      "credit_match": <true | false | "unknown">,
      "issues": [
        {"type": "missing_course",  "detail": "DEPT 101 - Title: on catalogue, absent from DB"},
        {"type": "extra_course",    "detail": "DEPT 999 - Title: in DB, not on catalogue"},
        {"type": "credit_mismatch", "detail": "Catalogue: 136cr, DB: 131cr"},
        {"type": "title_mismatch",  "detail": "DEPT 101: catalogue='Intro to Foo', DB='Intro Foo'"},
        {"type": "block_missing",   "detail": "Catalogue has 'Complementary Courses' block, DB does not"},
        {"type": "page_issue",      "detail": "404 or login wall"}
      ],
      "notes": "<1-2 sentence plain-English summary of overall accuracy>"
    }

    Rules:
    - Course code mismatches (e.g. COMP 202 vs COMP 204) count as missing_course + extra_course.
    - Ignore cosmetic title differences (abbreviations, punctuation).
    - If the catalogue page text is clearly wrong (404, login required), add a page_issue entry.
    - If a block in our DB has no courses listed (empty elective pools) that is not an error.
    - Focus on required/core courses; optional elective pools that differ are lower priority.
""").strip()


def audit_with_claude(client: anthropic.Anthropic, prog: dict, catalogue_text: str) -> dict:
    """Send DB summary + catalogue text to Claude and parse the JSON response."""
    db_summary = build_db_summary(prog)

    user_content = (
        "=== OUR DATABASE ===\n"
        + db_summary
        + "\n\n=== MCGILL CATALOGUE PAGE ===\n"
        + (catalogue_text if catalogue_text else "[No content retrieved]")
    )

    try:
        msg = client.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=4000,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user_content}],
        )
        raw = msg.content[0].text.strip()
        # Strip accidental markdown fences
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        s, e = raw.find("{"), raw.rfind("}")
        if s == -1 or e == -1:
            raise ValueError("No JSON object in response")
        return json.loads(raw[s : e + 1])
    except Exception as exc:
        return {
            "catalogue_credits": None,
            "credit_match": "unknown",
            "issues": [{"type": "audit_error", "detail": str(exc)}],
            "notes": "Claude audit failed.",
        }


# ── Reporting ──────────────────────────────────────────────────────────────────

ISSUE_TYPE_COLOURS = {
    "missing_course":  "red",
    "extra_course":    "green",
    "credit_mismatch": "yellow",
    "title_mismatch":  "yellow",
    "block_missing":   "magenta",
    "page_issue":      "bright_red",
    "audit_error":     "bright_red",
}

ISSUE_TYPE_SYMBOLS = {
    "missing_course":  "−",
    "extra_course":    "+",
    "credit_mismatch": "≠",
    "title_mismatch":  "~",
    "block_missing":   "□",
    "page_issue":      "!",
    "audit_error":     "✗",
}


def print_program_result(prog: dict, result: dict) -> None:
    issues = result.get("issues", [])
    credit_ok = result.get("credit_match")
    cat_cr = result.get("catalogue_credits")

    # Status indicator
    if not issues:
        status = "[green]✓ OK[/green]"
    elif any(i["type"] in ("page_issue", "audit_error") for i in issues):
        status = "[bright_red]✗ ERROR[/bright_red]"
    else:
        status = f"[yellow]⚠ {len(issues)} issue(s)[/yellow]"

    credit_line = (
        f"[green]credits match ({cat_cr})[/green]"
        if credit_ok is True
        else f"[yellow]credit mismatch — catalogue: {cat_cr}, DB: {prog['total_credits']}[/yellow]"
        if credit_ok is False
        else f"catalogue credits: {cat_cr if cat_cr is not None else '?'}"
    )

    console.print(f"\n[bold]{prog['name']}[/bold]  {status}")
    console.print(f"  [dim]{prog['faculty']} · {prog['program_type']} · {credit_line}[/dim]")

    if result.get("notes"):
        console.print(f"  [dim italic]{result['notes']}[/dim italic]")

    for issue in issues:
        colour = ISSUE_TYPE_COLOURS.get(issue["type"], "white")
        sym = ISSUE_TYPE_SYMBOLS.get(issue["type"], "?")
        console.print(f"  [{colour}]{sym}[/{colour}] {issue['detail']}")


def print_summary(all_results: list[dict]) -> None:
    total   = len(all_results)
    ok      = sum(1 for r in all_results if not r["result"].get("issues"))
    errored = sum(1 for r in all_results if any(
        i["type"] in ("page_issue", "audit_error")
        for i in r["result"].get("issues", [])
    ))
    with_issues = total - ok - errored

    table = Table(title="\nAudit Summary", show_header=True, header_style="bold")
    table.add_column("", justify="right")
    table.add_column("Count", justify="right")
    table.add_row("Programs audited", str(total))
    table.add_row("[green]Match[/green]", str(ok))
    table.add_row("[yellow]Issues found[/yellow]", str(with_issues))
    table.add_row("[bright_red]Errors[/bright_red]", str(errored))
    console.print(table)


def write_csv(all_results: list[dict], path: str) -> None:
    fields = [
        "program_key", "name", "faculty", "program_type",
        "credits_db", "credits_catalogue", "credit_match",
        "status", "issue_count", "issues", "notes",
    ]
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for r in all_results:
            prog   = r["prog"]
            result = r["result"]
            issues = result.get("issues", [])
            has_error = any(i["type"] in ("page_issue", "audit_error") for i in issues)
            status = "error" if has_error else ("ok" if not issues else "issues")
            writer.writerow({
                "program_key":       prog["program_key"],
                "name":              prog["name"],
                "faculty":           prog["faculty"],
                "program_type":      prog["program_type"],
                "credits_db":        prog["total_credits"],
                "credits_catalogue": result.get("catalogue_credits", ""),
                "credit_match":      result.get("credit_match", ""),
                "status":            status,
                "issue_count":       len(issues),
                "issues":            " | ".join(i["detail"] for i in issues),
                "notes":             result.get("notes", ""),
            })
    console.print(f"\n[green]CSV written to {path}[/green]")


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(description="Audit McGill degree requirements vs catalogue.")
    parser.add_argument("--faculty",       help="Filter by exact faculty name")
    parser.add_argument("--program-key",   help="Audit a single program by its program_key")
    parser.add_argument("--program-keys",  help="Comma-separated list of program_keys to audit")
    parser.add_argument("--csv",           help="Write results to this CSV file path")
    parser.add_argument("--no-claude",     action="store_true",
                        help="Only fetch catalogue pages, skip Claude analysis (dry-run)")
    args = parser.parse_args()

    # Validate env vars
    missing = [v for v in ("SUPABASE_URL", "SUPABASE_KEY or SUPABASE_SERVICE_ROLE_KEY", "ANTHROPIC_API_KEY")
               if not os.environ.get(v.split(" ")[0])]
    if missing:
        # Check the compound SUPABASE_KEY option
        if not SUPABASE_KEY:
            console.print("[red]Missing env var: SUPABASE_URL or SUPABASE_KEY/SUPABASE_SERVICE_ROLE_KEY[/red]")
            sys.exit(1)
    if not ANTHROPIC_API_KEY and not args.no_claude:
        console.print("[red]Missing env var: ANTHROPIC_API_KEY (or use --no-claude for dry run)[/red]")
        sys.exit(1)

    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    claude   = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY) if not args.no_claude else None

    console.print("\n[bold]McGill Degree Requirements Audit[/bold]")
    console.print("Loading programs from Supabase…")

    program_keys_list = [k.strip() for k in args.program_keys.split(",")] if args.program_keys else None
    programs = load_programs_from_db(supabase, faculty=args.faculty, program_key=args.program_key, program_keys=program_keys_list)
    if not programs:
        console.print("[yellow]No programs found with the given filters.[/yellow]")
        sys.exit(0)

    console.print(f"Found [bold]{len(programs)}[/bold] program(s) to audit.\n")

    all_results = []

    for i, prog in enumerate(programs, 1):
        console.print(f"[dim]({i}/{len(programs)})[/dim] Fetching catalogue for [bold]{prog['name']}[/bold]…", end=" ")

        catalogue_text, fetch_error = fetch_catalogue_page(prog.get("ecalendar_url", ""))

        if fetch_error:
            console.print(f"[red]fetch error[/red]")
            result = {
                "catalogue_credits": None,
                "credit_match": "unknown",
                "issues": [{"type": "page_issue", "detail": fetch_error}],
                "notes": "Could not retrieve catalogue page.",
            }
        elif args.no_claude:
            console.print(f"[green]fetched ({len(catalogue_text)} chars)[/green]")
            result = {
                "catalogue_credits": None,
                "credit_match": "unknown",
                "issues": [],
                "notes": "Dry run — Claude analysis skipped.",
            }
        else:
            console.print(f"[green]fetched ({len(catalogue_text)} chars)[/green] → analysing with Claude…", end=" ")
            result = audit_with_claude(claude, prog, catalogue_text)
            console.print("[green]done[/green]")

        print_program_result(prog, result)
        all_results.append({"prog": prog, "result": result})

        # Polite delay between requests
        if i < len(programs):
            time.sleep(REQUEST_DELAY)

    print_summary(all_results)

    if args.csv:
        write_csv(all_results, args.csv)


if __name__ == "__main__":
    main()