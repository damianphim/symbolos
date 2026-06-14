#!/usr/bin/env python3
"""
Phase 3 – Seed Regeneration Script
====================================
Fetches the live McGill 2026-2027 course catalogue page for each program,
extracts the correct requirement blocks and courses using Claude, and outputs
a ready-to-run Python seed snippet matching your existing seed file format.

Does NOT write to Supabase automatically — you review the output first,
then run with --apply to commit.

Usage
-----
    # Preview output for one program:
    python reseed_programs.py --program-key religious_studies_major

    # Preview a comma-separated list:
    python reseed_programs.py --program-keys "religious_studies_major,religious_studies_minor"

    # Preview all programs flagged in the audit CSV:
    python reseed_programs.py --from-csv results_v2.csv --status issues

    # Write output to a Python file for review:
    python reseed_programs.py --program-key religious_studies_major --output-file reseeds/religious_studies_major.py

    # Apply directly to Supabase after reviewing:
    python reseed_programs.py --program-key religious_studies_major --apply

Environment variables
---------------------
    SUPABASE_URL
    SUPABASE_SERVICE_ROLE_KEY  (or SUPABASE_KEY)
    ANTHROPIC_API_KEY
"""

import argparse
import ast
import csv
import json
import os
import sys
import textwrap
import time

import anthropic
import httpx
from bs4 import BeautifulSoup
from rich.console import Console
from rich.syntax import Syntax
from supabase import create_client

console = Console()

CLAUDE_MODEL   = "claude-sonnet-4-6"          # Sonnet for large programs
MAX_HTML_CHARS = 20_000                       # Full page
REQUEST_DELAY  = 1.5

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; McGill-Reseed-Bot/1.0; academic use)",
    "Accept-Language": "en-CA,en;q=0.9",
}

# ── Block types supported in your seed format ─────────────────────────────────
BLOCK_TYPE_GUIDE = """
Block types:
  required       — every listed course must be taken
  choose_credits — student picks `credits_needed` credits from the list
  choose_courses — student picks `courses_needed` courses from the list
  group          — a named sub-group (Group A / Group B) within a multi_group parent
  multi_group    — parent block: "X credits from Group A AND Y credits from Group B"
  pool_group     — parent block: "at least X credits total from Groups A+B+C combined"
  level_elective — any course at a given level (use when catalogue says "any 300-level course")
"""

SYSTEM_PROMPT = textwrap.dedent(f"""
    You are a precise academic data extractor for McGill University's 2026-2027 course catalogue.

    You will be given:
    1. The program's metadata (program_key, name, faculty, program_type, total_credits, ecalendar_url)
    2. The raw text of the programme's 2026-2027 McGill course catalogue page

    Your task is to extract the complete, accurate requirement structure and output it as a
    Python data structure that matches the exact seed format used in this codebase.

    {BLOCK_TYPE_GUIDE}

    CRITICAL RULE — Stream/Group credits_needed:
    When the catalogue says "X credits from ONE OF the following streams/groups", the
    individual `group` blocks must have `credits_needed: null`. Only the parent `multi_group`
    or `pool_group` block carries the credit requirement (e.g. credits_needed: 12).
    Example: "12 credits from one of: Stream A, Stream B, Stream C"
      → parent multi_group: credits_needed=12
      → each group child: credits_needed=null
    When the catalogue says "X credits from Group A AND Y credits from Group B" (both required),
    each group block carries its own credits_needed value.

    Course fields:
      subject        — e.g. "COMP"
      catalog        — e.g. "202" or "302D1" (include D1/D2/N1/N2 suffixes)
      title          — exact title from the catalogue
      credits        — numeric (e.g. 3, 4, 1.5)
      is_required    — True if the course is mandatory, False if it's a choice
      recommended    — False unless you have a strong reason
      recommendation_reason — "" unless recommended=True
      choose_from_group — group label string if this course belongs to a named group (e.g. "Group A"), else null
      choose_n_credits  — null
      notes          — "" unless there's a specific note about this course in the catalogue

    Rules:
    - Ignore any superscript footnote markers (1, 2, 3, etc.) that appear adjacent to credit values. For example, "3 1" or "1 3" means 3 credits with footnote 1, not "3.1" credits. Always extract credits as whole numbers or standard halves (e.g. 1.5, 4.5).
    - Extract ONLY what the catalogue page actually states. Do not infer or hallucinate.
    - Use the exact course codes from the catalogue (e.g. FREN not TRSL, EDES not EDTL).
    - If the catalogue lists D1/D2 pairs, include both as separate course entries.
    - Preserve the block structure exactly as the catalogue organises it.
    - Set `credits_needed` to the number of credits required from that block.
    - Set `courses_needed` to null unless the catalogue says "choose N courses".
    - If the catalogue page does not contain sufficient detail to extract courses,
      set "extraction_status" to "insufficient_data" and explain in "extraction_notes".
    - If the page contains full details, set "extraction_status" to "ok".

    In "extraction_notes" always include a brief plain-English summary covering:
    - Overall accuracy confidence (high/medium/low)
    - Whether the page was truncated and what was missed
    - Any structural decisions you made (e.g. how you modelled stream choices)
    - Any courses with unusual credits, mutual-exclusion rules, or footnotes
    - Any warnings the advisor should know about

    Output ONLY a valid JSON object (no markdown fences, no preamble):
    {{
      "extraction_status": "ok",
      "extraction_notes": "High confidence. Page complete. 3 blocks: 1 required (9cr) + 1 multi_group parent (12cr) with 4 stream children (credits_needed=null each). MECH 536 appears in 2 streams per catalogue.",
      "program": {{
        "program_key": "...",
        "name": "...",
        "program_type": "...",
        "faculty": "...",
        "total_credits": 0,
        "description": "...",
        "ecalendar_url": "...",
        "blocks": [
          {{
            "block_key": "prog_key_block_name",
            "title": "Required Courses (X credits)",
            "block_type": "required",
            "credits_needed": 0,
            "courses_needed": null,
            "group_name": null,
            "notes": "",
            "sort_order": 1,
            "courses": [
              {{
                "subject": "DEPT",
                "catalog": "101",
                "title": "Course Title",
                "credits": 3,
                "is_required": true,
                "recommended": false,
                "recommendation_reason": "",
                "choose_from_group": null,
                "choose_n_credits": null,
                "notes": ""
              }}
            ]
          }}
        ]
      }}
    }}
""").strip()


# ── Fetching ──────────────────────────────────────────────────────────────────

def fetch_page(url: str) -> tuple[str, str]:
    """Return (clean_text, error). clean_text is empty on error."""
    if not url:
        return "", "No ecalendar_url set for this program."
    try:
        r = httpx.get(url, headers=HEADERS, timeout=20, follow_redirects=True)
        r.raise_for_status()
    except httpx.HTTPStatusError as e:
        return "", f"HTTP {e.response.status_code}"
    except Exception as e:
        return "", str(e)

    soup = BeautifulSoup(r.text, "html.parser")

    # Remove boilerplate elements
    for tag in soup.select(
        "nav, footer, header, script, style, "
        ".breadcrumb, #menu, .back-to-top, "
        ".print-options, .pdf-options, "
        "[class*='cookie'], [class*='Cookie'], "
        "[class*='sidebar'], [class*='Sidebar'], "
        "[id*='sidebar'], [id*='Sidebar'], "
        ".contact-info, .department-info, "
        "[class*='social'], [class*='share'], "
        "[class*='search'], [class*='Search'], "
        "[class*='alert'], [class*='banner'], "
        "[class*='download'], [class*='print']"
    ):
        tag.decompose()

    # Remove repeated boilerplate text blocks specific to McGill catalogue
    for tag in soup.find_all(string=lambda t: t and any(phrase in t for phrase in [
        "Most students use Visual Schedule Builder",
        "Launch Visual Schedule Builder",
        "Back to top",
        "Close this window",
        "Send Page to Printer",
        "Print this page",
        "Download PDF",
        "The PDF will include",
        "2026-2027 Undergraduate Catalogue",
        "2025-2026 Undergraduate Catalogue",
        "2026-2027 Graduate Catalogue",
        "We use cookies",
        "Essential cookies",
        "Performance cookies",
        "Marketing cookies",
        "McGill University Mail",
        "Strathcona Music Building",
        "Note: Course availabilities for the 2026",
    ])):
        if tag.parent:
            tag.parent.decompose()

    main = soup.select_one("main") or soup.select_one(".main-content") or soup.body
    text = main.get_text(separator="\n", strip=True) if main else soup.get_text(separator="\n", strip=True)

    # Collapse excessive blank lines and deduplicate
    lines = [l for l in text.splitlines() if l.strip()]
    deduped = []
    for line in lines:
        if not deduped or line != deduped[-1]:
            deduped.append(line)

    # Strip course descriptions: McGill catalogue pages list courses as:
    #   DEPT 123  Course Title.  3 credits
    #   <description paragraph(s)>
    #   Prerequisite: ...
    #   Terms offered: ...
    # We only need the course code/title/credits line, not the description.
    import re
    course_code_pattern = re.compile(r'^[A-Z]{2,5}\s+\d{2,3}[A-Z0-9]*\b')
    prereq_pattern = re.compile(r'^(Prerequisite|Corequisite|Restriction|Note|Terms offered|Offered by|Not open|Students who|Open to|This course|Fall|Winter|Summer)', re.IGNORECASE)

    filtered = []
    skip_description = False
    for line in deduped:
        if course_code_pattern.match(line):
            # This is a course code line — keep it and start skipping description
            filtered.append(line)
            skip_description = True
        elif skip_description and prereq_pattern.match(line):
            # Prerequisite/restriction lines are useful — keep and continue skipping
            filtered.append(line)
        elif skip_description and (
            course_code_pattern.match(line) or
            line.startswith(('Required', 'Complementary', 'Choose', 'Group', 'Stream',
                             'List', 'Note:', 'Students', 'The following', 'credits'))
        ):
            # New section or heading — stop skipping
            filtered.append(line)
            skip_description = False
        elif skip_description:
            # This is a description line — skip it
            continue
        else:
            filtered.append(line)
            skip_description = False

    return "\n".join(filtered)[:MAX_HTML_CHARS], ""


# ── Claude extraction ─────────────────────────────────────────────────────────

def extract_with_claude(client: anthropic.Anthropic, prog_meta: dict, page_text: str) -> dict:
    user_content = (
        "=== PROGRAM METADATA ===\n"
        + json.dumps(prog_meta, indent=2)
        + "\n\n=== 2026-2027 MCGILL CATALOGUE PAGE ===\n"
        + (page_text if page_text else "[No content retrieved — page may be an overview only]")
    )

    try:
        msg = client.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=16000,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user_content}],
        )
        raw = msg.content[0].text.strip()
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        s, e = raw.find("{"), raw.rfind("}")
        if s == -1:
            raise ValueError("No JSON in response")
        return json.loads(raw[s:e+1])
    except Exception as exc:
        return {
            "extraction_status": "error",
            "extraction_notes": str(exc),
            "program": None,
        }


# ── Output formatting ─────────────────────────────────────────────────────────

def prog_to_python(prog: dict) -> str:
    """Convert extracted program dict to a formatted Python snippet."""
    lines = []
    lines.append("  {")
    lines.append(f'    "program_key":   {repr(prog["program_key"])},')
    lines.append(f'    "name":          {repr(prog["name"])},')
    lines.append(f'    "program_type":  {repr(prog["program_type"])},')
    lines.append(f'    "faculty":       {repr(prog["faculty"])},')
    lines.append(f'    "total_credits": {prog["total_credits"]},')
    lines.append(f'    "description":   {repr(prog.get("description", ""))},')
    lines.append(f'    "ecalendar_url": {repr(prog.get("ecalendar_url", ""))},')
    lines.append('    "blocks": [')

    for block in prog.get("blocks", []):
        lines.append("      {")
        lines.append(f'        "block_key":      {repr(block["block_key"])},')
        lines.append(f'        "title":          {repr(block["title"])},')
        lines.append(f'        "block_type":     {repr(block["block_type"])},')
        lines.append(f'        "credits_needed": {block.get("credits_needed")},')
        lines.append(f'        "courses_needed": {block.get("courses_needed")},')
        lines.append(f'        "group_name":     {repr(block.get("group_name"))},')
        lines.append(f'        "notes":          {repr(block.get("notes", ""))},')
        lines.append(f'        "sort_order":     {block.get("sort_order", 0)},')
        lines.append('        "courses": [')

        for c in block.get("courses", []):
            parts = [
                f'"subject": {repr(c.get("subject", ""))}',
                f'"catalog": {repr(c.get("catalog", ""))}',
                f'"title": {repr(c.get("title", ""))}',
                f'"credits": {c.get("credits", 3)}',
                f'"is_required": {c.get("is_required", False)}',
                f'"recommended": {c.get("recommended", False)}',
                f'"recommendation_reason": {repr(c.get("recommendation_reason", ""))}',
                f'"choose_from_group": {repr(c.get("choose_from_group"))}',
                f'"choose_n_credits": {repr(c.get("choose_n_credits"))}',
                f'"notes": {repr(c.get("notes", ""))}',
            ]
            lines.append("          {" + ", ".join(parts) + "},")

        lines.append("        ],")
        lines.append("      },")

    lines.append("    ],")
    lines.append("  },")
    return "\n".join(lines)


def apply_to_supabase(supabase, prog: dict) -> dict:
    """Upsert program + blocks + courses to Supabase."""
    counts = {"blocks": 0, "courses": 0}

    prog_payload = {
        "program_key":   prog["program_key"],
        "name":          prog["name"],
        "program_type":  prog["program_type"],
        "faculty":       prog["faculty"],
        "total_credits": prog["total_credits"],
        "description":   prog.get("description", ""),
        "ecalendar_url": prog.get("ecalendar_url", ""),
    }
    result = supabase.table("degree_programs").upsert(
        prog_payload, on_conflict="program_key"
    ).execute()
    prog_id = result.data[0]["id"]

    # Delete existing blocks (cascades to requirement_courses)
    supabase.table("requirement_blocks").delete().eq("program_id", prog_id).execute()

    for i, block in enumerate(prog.get("blocks", [])):
        block_payload = {
            "program_id":     prog_id,
            "block_key":      block["block_key"],
            "title":          block["title"],
            "block_type":     block["block_type"],
            "credits_needed": block.get("credits_needed"),
            "courses_needed": block.get("courses_needed"),
            "group_name":     block.get("group_name"),
            "notes":          block.get("notes", ""),
            "sort_order":     block.get("sort_order", i),
        }
        block_result = supabase.table("requirement_blocks").insert(block_payload).execute()
        block_id = block_result.data[0]["id"]
        counts["blocks"] += 1

        course_rows = []
        for j, c in enumerate(block.get("courses", [])):
            course_rows.append({
                "block_id":              block_id,
                "subject":               c["subject"],
                "catalog":               c["catalog"],
                "title":                 c.get("title", ""),
                "credits":               float(c.get("credits", 3)),
                "is_required":           c.get("is_required", False),
                "recommended":           c.get("recommended", False),
                "recommendation_reason": c.get("recommendation_reason", ""),
                "choose_from_group":     c.get("choose_from_group"),
                "choose_n_credits":      c.get("choose_n_credits"),
                "notes":                 c.get("notes", ""),
                "sort_order":            j,
            })

        if course_rows:
            supabase.table("requirement_courses").insert(course_rows).execute()
            counts["courses"] += len(course_rows)

    return counts


# ── Main ──────────────────────────────────────────────────────────────────────

def load_program_keys_from_csv(csv_path: str, status_filter: str) -> list[str]:
    keys = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if status_filter == "all" or row.get("status") == status_filter:
                keys.append(row["program_key"])
    return keys


def main():
    parser = argparse.ArgumentParser(description="Regenerate seed data from live McGill catalogue.")
    parser.add_argument("--program-key",  help="Single program_key to reseed")
    parser.add_argument("--program-keys", help="Comma-separated list of program_keys")
    parser.add_argument("--from-csv",     help="Path to audit CSV; use with --status")
    parser.add_argument("--status",       default="issues",
                        help="Filter CSV by status: issues | error | ok | all (default: issues)")
    parser.add_argument("--output-file",  help="Write Python seed snippet to this file")
    parser.add_argument("--apply",        action="store_true",
                        help="Write changes to Supabase (default: preview only)")
    args = parser.parse_args()

    if not SUPABASE_URL or not SUPABASE_KEY:
        console.print("[red]Missing SUPABASE_URL / SUPABASE_KEY env vars.[/red]")
        sys.exit(1)
    if not ANTHROPIC_API_KEY:
        console.print("[red]Missing ANTHROPIC_API_KEY env var.[/red]")
        sys.exit(1)

    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    claude   = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    # ── Resolve program keys ──────────────────────────────────────────
    if args.program_key:
        keys = [args.program_key.strip()]
    elif args.program_keys:
        keys = [k.strip() for k in args.program_keys.split(",")]
    elif args.from_csv:
        keys = load_program_keys_from_csv(args.from_csv, args.status)
    else:
        console.print("[red]Provide --program-key, --program-keys, or --from-csv.[/red]")
        sys.exit(1)

    # ── Load program metadata from Supabase ───────────────────────────
    rows = (
        supabase.table("degree_programs")
        .select("program_key, name, program_type, faculty, total_credits, ecalendar_url, description")
        .in_("program_key", keys)
        .execute()
        .data or []
    )
    prog_map = {r["program_key"]: r for r in rows}

    missing = [k for k in keys if k not in prog_map]
    if missing:
        console.print(f"[yellow]Warning: program_keys not found in DB: {missing}[/yellow]")

    programs_to_process = [prog_map[k] for k in keys if k in prog_map]
    console.print(f"\n[bold]Phase 3 – Seed Regeneration[/bold]")
    console.print(f"{'Applying to Supabase' if args.apply else 'Preview mode (--apply to commit)'}")
    console.print(f"Processing [bold]{len(programs_to_process)}[/bold] program(s)\n")

    all_snippets = []
    errors = []

    for i, prog_meta in enumerate(programs_to_process, 1):
        key  = prog_meta["program_key"]
        name = prog_meta["name"]
        url  = prog_meta.get("ecalendar_url", "")

        console.print(f"[dim]({i}/{len(programs_to_process)})[/dim] [bold]{name}[/bold]")
        console.print(f"  Fetching: {url}", end=" … ")

        page_text, fetch_err = fetch_page(url)
        if fetch_err:
            console.print(f"[red]fetch error: {fetch_err}[/red]")
            errors.append({"key": key, "error": fetch_err})
            continue
        console.print(f"[green]{len(page_text)} chars[/green]")

        console.print("  Extracting with Claude…", end=" ")
        result = extract_with_claude(claude, prog_meta, page_text)

        status = result.get("extraction_status", "error")
        notes  = result.get("extraction_notes", "")

        if status == "insufficient_data":
            if result.get("program") and result["program"].get("blocks"):
                console.print(f"[yellow]partial data[/yellow]")
                console.print(f"  [yellow]⚠ Partial:[/yellow] {notes}")
                # Fall through to apply what we have
            else:
                console.print(f"[yellow]insufficient data[/yellow]")
                console.print(f"  [dim]{notes}[/dim]")
                errors.append({"key": key, "error": f"insufficient_data: {notes}"})
                continue
        elif status == "error" or result.get("program") is None:
            console.print(f"[red]extraction error[/red]")
            console.print(f"  [dim]{notes}[/dim]")
            errors.append({"key": key, "error": notes})
            continue

        extracted = result["program"]
        # Preserve the original program_key and ecalendar_url in case Claude changed them
        extracted["program_key"]   = key
        extracted["ecalendar_url"] = url

        block_count  = len(extracted.get("blocks", []))
        course_count = sum(len(b.get("courses", [])) for b in extracted.get("blocks", []))
        console.print(f"[green]done[/green] — {block_count} blocks, {course_count} courses")

        # Print concise summary instead of full code preview
        console.print(f"  [bold]Credits:[/bold] {extracted.get('total_credits')}cr  "
                      f"[bold]Blocks:[/bold] {block_count}  "
                      f"[bold]Courses:[/bold] {course_count}")
        for block in extracted.get("blocks", []):
            cr = f"{block.get('credits_needed')}cr" if block.get('credits_needed') else "—"
            n  = len(block.get("courses", []))
            console.print(f"    [dim]{block['block_type']:15} {cr:6} {n:3} courses  {block['title'][:60]}[/dim]")
        if notes:
            console.print(f"  [yellow]⚠ Note:[/yellow] {notes}")
        console.print()

        snippet = prog_to_python(extracted)
        all_snippets.append(snippet)

        if args.apply:
            console.print("  Writing to Supabase…", end=" ")
            try:
                counts = apply_to_supabase(supabase, extracted)
                console.print(f"[green]✓ {counts['blocks']} blocks, {counts['courses']} courses[/green]")
            except Exception as exc:
                console.print(f"[red]✗ DB error: {exc}[/red]")
                errors.append({"key": key, "error": str(exc)})

        if i < len(programs_to_process):
            time.sleep(REQUEST_DELAY)

    # ── Write output file ─────────────────────────────────────────────
    if args.output_file and all_snippets:
        header = (
            '"""\nAuto-generated seed data from McGill 2026-2027 Course Catalogue.\n'
            'Review carefully before running with --apply.\n"""\n\n'
            "RESEEDED_PROGRAMS = [\n"
        )
        footer = "\n]\n"
        os.makedirs(os.path.dirname(args.output_file) or ".", exist_ok=True)
        with open(args.output_file, "w", encoding="utf-8") as f:
            f.write(header + "\n".join(all_snippets) + footer)
        console.print(f"\n[green]Output written to {args.output_file}[/green]")

    # ── Summary ───────────────────────────────────────────────────────
    console.print(f"\n{'='*60}")
    console.print(f"Done. {len(all_snippets)} extracted  |  {len(errors)} errors")
    if errors:
        console.print("\n[yellow]Errors:[/yellow]")
        for e in errors:
            console.print(f"  {e['key']}: {e['error']}")

    if not args.apply and all_snippets:
        console.print(
            "\n[dim]Run with [bold]--apply[/bold] to write these changes to Supabase.[/dim]"
        )


if __name__ == "__main__":
    main()