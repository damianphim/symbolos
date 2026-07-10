#!/usr/bin/env python3
"""
Import McGill class-section data (instructor, times, location) into the
`mcgill_sections` table from Minerva "Class Schedule Listing" HTML that YOU
export while logged in.

This tool does NOT scrape anything — it only parses local files you saved
from a source you are authenticated to view. Access stays human; parsing +
loading is automated.

How to get the input files
--------------------------
1. Log in to Minerva → Student Menu → Registration → "Class Schedule Search"
   (or "Look Up Courses"). Pick a term (Fall 2026 / Winter 2027), pick a
   subject (or "All"), search.
2. On the results page ("Class Schedule Listing"), Save Page As → *Web Page,
   HTML only* into backend/scripts/section_exports/.
   One file per subject is fine; the parser reads every *.html in the folder.

Usage
-----
    # Self-test the parser on a synthetic fixture (no network, no DB):
    python scripts/import_sections.py --self-test

    # Dry-run: parse every export and print a summary (writes NOTHING):
    python scripts/import_sections.py

    # Parse only one term, filter to a subject, show sample rows:
    python scripts/import_sections.py --term "Fall 2026" --course COMP

    # Write to Supabase after reviewing the dry-run:
    python scripts/import_sections.py --apply

Environment
-----------
Reads SUPABASE_URL / SUPABASE_SERVICE_KEY from backend/.env(.local) — same as
the other scripts. Only needed with --apply.
"""
from __future__ import annotations

import argparse
import os
import re
import sys
from html import unescape
from pathlib import Path

# ── Term-code helpers ───────────────────────────────────────────────────────
# Minerva shows the human term ("Fall 2026") in the "Associated Term" line, so
# we key off that. This map is only used for --term validation / filenames.
TERM_CODE = {  # Banner YYYYMM  ->  human label used in mcgill_sections
    "202609": "Fall 2026",
    "202701": "Winter 2027",
    "202705": "Summer 2027",
    "202509": "Fall 2025",
    "202601": "Winter 2026",
}


# ── Parser (stdlib only) ────────────────────────────────────────────────────
# Minerva/Banner "Class Schedule Listing" structure (stable for ~15 years):
#   <th class="ddtitle"><a ...>TITLE - CRN - SUBJ NUM - SECTION</a></th>
#   <td class="dddefault">
#       ... Associated Term: <span>Fall 2026</span> ...
#       ... <table class="datadisplaytable"> meeting rows </table> ...
#   </td>
_TAG = re.compile(r"<[^>]+>")
_TITLE_ANCHOR = re.compile(
    r'<th[^>]*class="ddtitle"[^>]*>.*?<a[^>]*>(.*?)</a>', re.I | re.S
)
_ASSOC_TERM = re.compile(r"Associated Term:\s*(?:</span>)?\s*([A-Za-z]+ \d{4})", re.I)
_CREDITS = re.compile(r"([\d.]+)\s*Credits", re.I)
_INNER_TABLE = re.compile(
    r'<table[^>]*class="datadisplaytable"[^>]*>(.*?)</table>', re.I | re.S
)
_ROW = re.compile(r"<tr[^>]*>(.*?)</tr>", re.I | re.S)
_CELL = re.compile(r"<t[dh][^>]*>(.*?)</t[dh]>", re.I | re.S)


def _text(html: str) -> str:
    return unescape(_TAG.sub("", html)).replace("\xa0", " ").strip()


def _parse_title(anchor_text: str) -> dict | None:
    """'Intro to CS - 12345 - COMP 202 - 001' -> parts. Order is stable."""
    parts = [p.strip() for p in _text(anchor_text).split(" - ")]
    if len(parts) < 4:
        return None
    # code + number sit in the 3rd-from-... but titles can contain ' - ' too,
    # so anchor from the RIGHT: [..., 'COMP 202', '001'] with CRN before code.
    section = parts[-1]
    subj_num = parts[-2]
    crn = parts[-3]
    title = " - ".join(parts[:-3])
    m = re.match(r"([A-Z]{2,4})\s+(\d{3}[A-Z]?\d?)", subj_num)
    if not m or not crn.isdigit():
        return None
    return {
        "title": title,
        "crn": crn,
        "subject": m.group(1),
        "number": m.group(2),
        "section": section,
    }


def _parse_meetings(block_html: str) -> list[dict]:
    """Parse the inner meeting-times table into rows keyed by header."""
    tbl = _INNER_TABLE.search(block_html)
    if not tbl:
        return []
    rows = _ROW.findall(tbl.group(1))
    if len(rows) < 2:
        return []
    headers = [_text(c).lower() for c in _CELL.findall(rows[0])]
    out = []
    for r in rows[1:]:
        cells = [_text(c) for c in _CELL.findall(r)]
        if not cells:
            continue
        rec = {headers[i]: cells[i] for i in range(min(len(headers), len(cells)))}
        out.append(rec)
    return out


def parse_export(html: str, default_term: str | None = None) -> list[dict]:
    """Return one dict per section found in a Class Schedule Listing file."""
    sections: list[dict] = []
    # Split into per-course blocks on each ddtitle header.
    starts = [m.start() for m in re.finditer(r'<th[^>]*class="ddtitle"', html, re.I)]
    for i, s in enumerate(starts):
        block = html[s : starts[i + 1] if i + 1 < len(starts) else len(html)]
        am = _TITLE_ANCHOR.search(block)
        if not am:
            continue
        head = _parse_title(am.group(1))
        if not head:
            continue
        term_m = _ASSOC_TERM.search(block)
        term = term_m.group(1) if term_m else default_term
        cred_m = _CREDITS.search(block)
        meetings = _parse_meetings(block)

        # Collapse meetings into the single-row-per-section shape the table
        # already uses (join multiple meeting patterns with '; ').
        def col(rec, *names):
            for n in names:
                for k in rec:
                    if n in k:
                        return rec[k]
            return None

        days = "; ".join(filter(None, (col(m, "days") for m in meetings)))
        times = "; ".join(filter(None, (col(m, "time") for m in meetings)))
        locs = "; ".join(filter(None, (col(m, "where") for m in meetings)))
        instr = next(
            (col(m, "instructor") for m in meetings if col(m, "instructor")), None
        )
        stype = next(
            (col(m, "schedule type", "type") for m in meetings if col(m, "schedule type", "type")),
            None,
        )
        sections.append(
            {
                "course_code": f"{head['subject']} {head['number']}",
                "crn": head["crn"],
                "term": term,
                "section": head["section"],
                "section_type": (stype or "Lecture").strip() or "Lecture",
                "instructor": _clean_instructor(instr),
                "days": days or None,
                "times": times or None,
                "location": locs or None,
                "credits": float(cred_m.group(1)) if cred_m else None,
                "title": head["title"],
            }
        )
    return sections


def _clean_instructor(raw: str | None) -> str | None:
    if not raw:
        return None
    # Banner marks the primary with "(P)" and separates co-instructors by ", ".
    txt = re.sub(r"\s*\(P\)", "", raw).strip(" ,")
    txt = re.sub(r"\s+", " ", txt)
    if not txt or txt.upper() in ("TBA", "TBD", "STAFF"):
        return None
    return txt[:120]


def _flt(v: str | None) -> float | None:
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


# ── Parser #2: "Look Up Classes" results (bwskfcls.P_GetCrse) ────────────────
# Flat "Sections Found" table: one row per section, continuation rows (blank
# CRN) carry extra meeting patterns. Columns are matched by header name so
# small column-order changes don't break it.
def parse_lookup_classes(html: str, default_term: str | None = None) -> list[dict]:
    # Scan EVERY datadisplaytable for a *header row* with CRN + (Instructor or
    # Select). The real header is often NOT row 0 — Banner puts a subject-banner
    # (ddtitle) row above it. A multi-subject page has one such table per
    # subject, so accumulate across all of them (don't stop at the first).
    all_out: list[dict] = []
    for body in _INNER_TABLE.findall(html):
        rows = _ROW.findall(body)
        hdr_i = header = None
        for i, r in enumerate(rows):
            cells = [_text(c).lower() for c in _CELL.findall(r)]
            if any("crn" in h for h in cells) and any(
                ("instructor" in h or "select" in h) for h in cells
            ):
                hdr_i, header = i, cells
                break
        if hdr_i is None:
            continue

        def idx(*names):
            for j, h in enumerate(header):
                if any(n in h for n in names):
                    return j
            return None

        ci = {
            "crn": idx("crn"), "subj": idx("subj"), "crse": idx("crse", "cour"),
            "sec": idx("sec"), "type": idx("type"), "cred": idx("cred", "units"),
            "title": idx("title"), "days": idx("days"), "time": idx("time"),
            "instr": idx("instructor"), "loc": idx("location", "where"),
        }
        cur: dict | None = None
        for r in rows[hdr_i + 1:]:
            cells = [_text(c) for c in _CELL.findall(r)]
            if len(cells) < len(header) // 2:
                continue  # notes / spacer rows

            def g(k):
                i = ci[k]
                return cells[i] if i is not None and i < len(cells) else None

            crn = g("crn")
            if crn and crn.isdigit():
                subj, crse = (g("subj") or ""), (g("crse") or "")
                cur = {
                    "course_code": f"{subj} {crse}".strip(),
                    "crn": crn,
                    "term": default_term,
                    "section": g("sec"),
                    "section_type": (g("type") or "Lecture").strip() or "Lecture",
                    "instructor": _clean_instructor(g("instr")),
                    "days": g("days") or None,
                    "times": g("time") or None,
                    "location": g("loc") or None,
                    "credits": _flt(g("cred")),
                    "title": g("title"),
                }
                all_out.append(cur)
            elif cur:  # continuation meeting row for the current section
                for k, key in (("days", "days"), ("time", "times"), ("loc", "location")):
                    v = g(k)
                    if v:
                        cur[key] = f"{cur[key]}; {v}" if cur[key] else v
                if not cur["instructor"]:
                    cur["instructor"] = _clean_instructor(g("instr"))
    return all_out


def _detect_term(html: str) -> str | None:
    m = _ASSOC_TERM.search(html)
    if m:
        return m.group(1)
    m = re.search(r'term_in[^0-9]{0,10}(20\d{4})', html)
    if m:
        return TERM_CODE.get(m.group(1))
    m = re.search(r"\b(Fall|Winter|Summer) (20\d{2})\b", html)
    if m:
        return f"{m.group(1)} {m.group(2)}"
    return None


def parse_file(html: str, term_override: str | None = None) -> list[dict]:
    """Auto-detect the Banner export format and parse it.

    Try the flat "Look Up Classes" table first (it has a CRN+Instructor header
    row, possibly under a ddtitle subject banner). Only fall back to the
    Class Schedule Listing parser when there's no such table.
    """
    term = term_override or _detect_term(html)
    lk = parse_lookup_classes(html, term)
    if lk:
        return lk
    return parse_export(html, term)


def to_row(sec: dict) -> dict:
    """Map a parsed section to a `mcgill_sections` insert row."""
    return {
        "course_code": sec["course_code"],
        "crn": sec["crn"],
        "term": sec["term"],
        "section_type": sec["section_type"],
        "instructor": sec["instructor"],
        "days": sec["days"],
        "times": sec["times"],
        "location": sec["location"],
        "credits": sec["credits"],
    }


# ── Self-test fixture (synthetic markup — authored here, not from McGill) ────
_FIXTURE = """
<table class="datadisplaytable">
 <tr><th class="ddtitle"><a href="x">Introduction to Computer Science - 12345 - COMP 202 - 001</a></th></tr>
 <tr><td class="dddefault">
   <span class="fieldlabeltext">Associated Term: </span>Fall 2026<br>
   3.000 Credits<br>
   <table class="datadisplaytable">
     <tr><th>Type</th><th>Time</th><th>Days</th><th>Where</th><th>Date Range</th><th>Schedule Type</th><th>Instructors</th></tr>
     <tr><td>Class</td><td>10:35 am - 11:25 am</td><td>MWF</td><td>Trottier 100</td><td>Sep 02 - Dec 04</td><td>Lecture</td><td>Jane Doe (P)</td></tr>
   </table>
 </td></tr>
 <tr><th class="ddtitle"><a href="x">Algorithms &amp; Data Structures - 67890 - COMP 251 - 002</a></th></tr>
 <tr><td class="dddefault">
   <span class="fieldlabeltext">Associated Term: </span>Fall 2026<br>
   <table class="datadisplaytable">
     <tr><th>Type</th><th>Time</th><th>Days</th><th>Where</th><th>Date Range</th><th>Schedule Type</th><th>Instructors</th></tr>
     <tr><td>Class</td><td>TBA</td><td>TBA</td><td>TBA</td><td>Sep 02 - Dec 04</td><td>Lecture</td><td>TBA</td></tr>
   </table>
 </td></tr>
</table>
"""


# "Look Up Classes" fixture (synthetic markup) — flat table + continuation row.
_FIXTURE_LOOKUP = """
<input type="hidden" name="term_in" value="202609">
<table class="datadisplaytable" summary="sections found">
 <tr><th>Select</th><th>CRN</th><th>Subj</th><th>Crse</th><th>Sec</th><th>Cred</th>
     <th>Title</th><th>Days</th><th>Time</th><th>Cap</th><th>Instructor</th>
     <th>Date (MM/DD)</th><th>Location</th></tr>
 <tr><td>C</td><td>12345</td><td>COMP</td><td>202</td><td>001</td><td>3.000</td>
     <td>Intro to CS</td><td>MWF</td><td>10:35 am-11:25 am</td><td>200</td>
     <td>Jane Doe (P)</td><td>09/02-12/04</td><td>Trottier 100</td></tr>
 <tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td>
     <td>T</td><td>14:35 pm-15:25 pm</td><td></td><td></td><td></td><td>McConnell 11</td></tr>
 <tr><td>C</td><td>67890</td><td>MATH</td><td>133</td><td>002</td><td>4.000</td>
     <td>Linear Algebra</td><td>TR</td><td>08:35 am-09:55 am</td><td>150</td>
     <td>TBA</td><td>09/02-12/04</td><td>Burnside 1B23</td></tr>
</table>
<table class="datadisplaytable" summary="second subject">
 <tr><th colspan="13" class="ddtitle">Physics (Sci)</th></tr>
 <tr><th>Select</th><th>CRN</th><th>Subj</th><th>Crse</th><th>Sec</th><th>Cred</th>
     <th>Title</th><th>Days</th><th>Time</th><th>Cap</th><th>Instructor</th>
     <th>Date (MM/DD)</th><th>Location</th></tr>
 <tr><td>C</td><td>11111</td><td>PHYS</td><td>101</td><td>001</td><td>4.000</td>
     <td>Intro Physics</td><td>MWF</td><td>09:35 am-10:25 am</td><td>300</td>
     <td>Alan Weeks (P)</td><td>09/02-12/04</td><td>Rutherford 112</td></tr>
</table>
"""


def _self_test() -> int:
    # ── Format 2: Look Up Classes (two subject tables on one page) ──
    lk = parse_file(_FIXTURE_LOOKUP)
    assert len(lk) == 3, f"lookup: expected 3 across 2 tables, got {len(lk)}"
    c202, m133, phys = lk
    assert c202["course_code"] == "COMP 202" and c202["crn"] == "12345", c202
    assert c202["term"] == "Fall 2026", c202
    assert c202["instructor"] == "Jane Doe", c202
    assert c202["days"] == "MWF; T", c202            # continuation row merged
    assert "McConnell 11" in c202["location"], c202
    assert c202["credits"] == 3.0, c202
    assert m133["instructor"] is None, "TBA -> None"
    assert phys["course_code"] == "PHYS 101", phys  # 2nd table accumulated
    assert phys["instructor"] == "Alan Weeks", phys
    print("lookup-classes self-test PASSED:")
    for s in lk:
        print(f"  {s['course_code']} CRN {s['crn']} [{s['term']}] "
              f"{s['instructor'] or 'TBA'} — {s['days']} {s['times']} @ {s['location']}")

    # ── Format 1: Class Schedule Listing ──
    secs = parse_export(_FIXTURE)
    assert len(secs) == 2, f"expected 2 sections, got {len(secs)}"
    a, b = secs
    assert a["course_code"] == "COMP 202", a
    assert a["crn"] == "12345" and a["section"] == "001", a
    assert a["term"] == "Fall 2026", a
    assert a["instructor"] == "Jane Doe", a
    assert a["days"] == "MWF" and a["times"] == "10:35 am - 11:25 am", a
    assert a["location"] == "Trottier 100", a
    assert a["credits"] == 3.0, a
    assert b["course_code"] == "COMP 251" and b["crn"] == "67890", b
    assert b["instructor"] is None, "TBA instructor should be None"
    print("self-test PASSED — parsed 2 sections correctly:")
    for s in secs:
        print(f"  {s['course_code']} CRN {s['crn']} [{s['term']}] "
              f"{s['instructor'] or 'TBA'} — {s['days']} {s['times']} @ {s['location']}")
    return 0


# ── Main ────────────────────────────────────────────────────────────────────
def _load_env():
    from dotenv import load_dotenv
    here = Path(__file__).resolve().parent.parent  # backend/
    load_dotenv(here / ".env")
    load_dotenv(here / ".env.local", override=True)


def _supabase():
    from supabase import create_client
    url = os.environ["SUPABASE_URL"].strip().strip('"')
    key = os.environ["SUPABASE_SERVICE_KEY"].strip().strip('"')
    return create_client(url, key)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dir", default=str(Path(__file__).parent / "section_exports"),
                    help="Folder of exported *.html files")
    ap.add_argument("--term", help="Only import this term label (e.g. 'Fall 2026')")
    ap.add_argument("--course", help="Filter to a subject prefix (e.g. COMP)")
    ap.add_argument("--apply", action="store_true", help="Write to Supabase (else dry-run)")
    ap.add_argument("--self-test", action="store_true", help="Run the parser self-test and exit")
    args = ap.parse_args()

    if args.self_test:
        return _self_test()

    export_dir = Path(args.dir)
    files = sorted(export_dir.glob("*.html"))
    if not files:
        print(f"No *.html files in {export_dir}. Export from Minerva first "
              f"(see this script's docstring).")
        return 1

    all_secs: list[dict] = []
    for f in files:
        html = f.read_text(encoding="utf-8", errors="replace")
        secs = parse_file(html, term_override=args.term)
        fmt = "schedule-listing" if "ddtitle" in html.lower() else "look-up-classes"
        print(f"  {f.name}: {len(secs)} sections ({fmt})")
        if not secs and "ddtitle" not in html.lower() and "instructor" not in html.lower():
            print(f"    ⚠ {f.name} looks like the COURSE INDEX (term → subject → "
                  f"course list), not a sections listing — it has no CRNs, times, "
                  f"or instructors. Save the 'Class Schedule Search' results page "
                  f"instead (see docstring).")
        all_secs.extend(secs)

    # Filters
    if args.term:
        all_secs = [s for s in all_secs if s["term"] == args.term]
    if args.course:
        pfx = args.course.upper()
        all_secs = [s for s in all_secs if s["course_code"].startswith(pfx)]

    # Drop sections with no term (couldn't determine) and dedupe by (crn, term).
    missing_term = [s for s in all_secs if not s["term"]]
    if missing_term:
        print(f"  ⚠ {len(missing_term)} sections had no detectable term — skipped "
              f"(pass --term to force).")
    seen, rows = set(), []
    for s in all_secs:
        if not s["term"]:
            continue
        key = (s["course_code"], s["crn"], s["term"])
        if key in seen:
            continue
        seen.add(key)
        rows.append(s)

    terms = sorted({s["term"] for s in rows})
    print(f"\nParsed {len(rows)} unique sections across terms: {terms}")
    for s in rows[:8]:
        print(f"  {s['course_code']:10} CRN {s['crn']}  [{s['term']}]  "
              f"{(s['instructor'] or 'TBA'):22}  {s['days'] or '-'} {s['times'] or ''}")
    if len(rows) > 8:
        print(f"  … and {len(rows) - 8} more")

    if not args.apply:
        print("\nDRY-RUN — nothing written. Re-run with --apply to load into "
              "mcgill_sections.")
        return 0

    # ── Apply: replace each imported term wholesale (safe: these terms are new)
    _load_env()
    sb = _supabase()
    total = 0
    for term in terms:
        term_rows = [to_row(s) for s in rows if s["term"] == term]
        existing = sb.table("mcgill_sections").select("id").eq("term", term).execute()
        n_existing = len(existing.data or [])
        if n_existing:
            print(f"  {term}: replacing {n_existing} existing rows")
            sb.table("mcgill_sections").delete().eq("term", term).execute()
        for i in range(0, len(term_rows), 500):
            sb.table("mcgill_sections").insert(term_rows[i:i + 500]).execute()
        print(f"  {term}: inserted {len(term_rows)} sections")
        total += len(term_rows)
    print(f"\n✓ Loaded {total} sections into mcgill_sections.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
