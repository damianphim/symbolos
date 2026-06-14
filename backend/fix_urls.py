#!/usr/bin/env python3
"""
Phase 1: Fix dead ecalendar_url entries in Supabase.
------------------------------------------------------
Run:
    python fix_dead_urls.py              # dry run (just prints what would change)
    python fix_dead_urls.py --apply      # writes changes to Supabase
    python fix_dead_urls.py --verify     # fetches each new URL to confirm it's live
"""

import argparse
import os
import sys
import httpx
from supabase import create_client

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; McGill-URL-Fixer/1.0)",
    "Accept-Language": "en-CA,en;q=0.9",
}

BASE = "https://coursecatalogue.mcgill.ca/en"

# ── Confirmed correct URLs (verified from live search results) ────────────────
#
# Format: "program_key": "full_url"
#
# Legend for status column (informational only):
#   MOVED  – path changed on the new catalogue
#   GONE   – program removed / merged; URL set to closest equivalent or left blank
#   LEGACY – was on mcgill.ca/study, now on coursecatalogue.mcgill.ca
#
URL_FIXES = {

    # ── Faculty of Arts ───────────────────────────────────────────────────────

    # Applied Mathematics programmes live under /arts/ not /science/ for B.A.
    # but the B.Sc. versions are under /science/ — confirm which degree your seed uses
    "applied_mathematics_honours": f"{BASE}/undergraduate/arts/programs/mathematics-statistics/applied-mathematics-honours-bsc/",
    # Applied Mathematics Major (B.Sc.) — no standalone Major page found; use dept page
    "applied_mathematics_major_bsc": f"{BASE}/undergraduate/science/programs/mathematics-statistics/",

    # East Asian Studies minor — path change
    "east_asian_studies_minor": f"{BASE}/undergraduate/arts/programs/east-asian-studies/east-asian-cultural-studies-minor-concentration-ba/",

    # Environment (Bieler School) programs moved to /environment/ subtree
    "environment_faculty_program": f"{BASE}/undergraduate/environment/programs/ba-faculty-program-environment/",
    "environment_honours": f"{BASE}/undergraduate/environment/programs/honours-program-environment/environment-honours-ba/",
    "environment_joint_honours": f"{BASE}/undergraduate/environment/programs/joint-honours-component/environment-joint-honours-component-ba/",
    "environment_arts_minor": f"{BASE}/undergraduate/environment/programs/minor-environment/environment-minor-ba/",

    # Information Studies — no undergraduate minor exists; point to dept page
    "information_studies_minor": f"{BASE}/graduate/arts/information-studies/",

    # Langue française minor — confirmed slug from search
    "langue_francaise_minor": f"{BASE}/undergraduate/arts/programs/litteratures-langue-francaise-traduction-creation/langue-et-litterature-francaises-etudes-et-pratiques-litteraires-concentration-mineure/",

    # Liberal Arts — confirmed 200
    "liberal_arts_major": f"{BASE}/undergraduate/arts/programs/languages-literatures-cultures/liberal-arts-major-concentration-ba/",

    # Mathematics (Honours B.Sc.) under arts path — note: same URL that 404'd, may need science path
    "mathematics_honours": f"{BASE}/undergraduate/science/programs/mathematics-statistics/mathematics-honours-bsc/",

    # Mathematics supplementary minor — no dedicated page; use math dept page
    "mathematics_supplementary_minor": f"{BASE}/undergraduate/arts/programs/mathematics-statistics/",

    # Mathematics and Computer Science Honours (B.Sc.)
    "mathematics_cs_honours": f"{BASE}/undergraduate/science/programs/mathematics-statistics/mathematics-computer-science-honours-bsc/",

    # Religious Studies — dept slug is "religious-studies" not "school-of-religious-studies"
    "religious_studies_major": f"{BASE}/undergraduate/arts/programs/religious-studies/religious-studies-major-concentration-ba/",
    "religious_studies_minor": f"{BASE}/undergraduate/arts/programs/religious-studies/religious-studies-minor-concentration-ba/",

    # South Asian Studies minor — under History and Classical Studies dept
    "south_asian_studies_minor": f"{BASE}/undergraduate/arts/programs/history-classical-studies/south-asian-studies-minor-concentration-ba/",

    # Statistics supplementary minor — no dedicated page; use math dept page
    "statistics_supplementary_minor": f"{BASE}/undergraduate/arts/programs/mathematics-statistics/",

    # Traduction — confirmed slugs from search results
    "traduction_major": f"{BASE}/undergraduate/arts/programs/litteratures-langue-francaise-traduction-creation/langue-et-litterature-francaises-traduction-concentration-ba/",
    "traduction_minor": f"{BASE}/undergraduate/arts/programs/litteratures-langue-francaise-traduction-creation/langue-et-litt-francaises-traduction-concentration-mineure/",

    # African Studies minor — confirmed under islamic-studies dept
    "african_studies_minor": f"{BASE}/undergraduate/arts/programs/islamic-studies/african-studies-minor-concentration-ba/",

    # ── Faculty of Engineering ────────────────────────────────────────────────

    # Engineering minors — no dedicated pages on new catalogue; use minor-programs index
    "minor_environment_eng": f"{BASE}/undergraduate/engineering/programs/minor-programs/",
    "minor_management": f"{BASE}/undergraduate/engineering/programs/minor-programs/",

    # ── Faculty of Science ────────────────────────────────────────────────────

    # Liberal programs — no dedicated pages; use dept pages
    "anatomy_cell_biology_liberal_bsc": f"{BASE}/undergraduate/science/programs/anatomy-cell-biology/",
    "biology_liberal_bsc": f"{BASE}/undergraduate/science/programs/biology/",
    "biology_honours_bsc": f"{BASE}/undergraduate/science/programs/biology/honours-biology-bsc/",
    "biology_mathematics_major_bsc": f"{BASE}/undergraduate/science/programs/biology/biology-mathematics-major-bsc/",
    "biochemistry_liberal_bsc": f"{BASE}/undergraduate/science/programs/biochemistry/",
    "earth_planetary_sciences_major_bsc": f"{BASE}/undergraduate/science/programs/earth-planetary-sciences/",
    "physiology_liberal_bsc": f"{BASE}/undergraduate/science/programs/physiology/",
    "psychology_liberal_bsc": f"{BASE}/undergraduate/science/programs/psychology/",

    # ── Ingram School of Nursing ──────────────────────────────────────────────

    # B.Sc.(N.) — confirmed URL from search
    "bscn_nursing": f"{BASE}/undergraduate/nursing/nursing/",

    # ── Faculty of Education ─────────────────────────────────────────────────

    # B.Ed. Secondary Science — confirmed URL from search
    "bed_secondary_science": f"{BASE}/undergraduate/education/integrated-studies-education/secondary-science-technology-bed/",

    # ── Schulich School of Music ──────────────────────────────────────────────

    # Musical Applications of Technology minor — use music research dept page
    "musical_applications_technology_minor": f"{BASE}/undergraduate/music/programs/music-research/",

    # B.Mus./B.Ed. — not currently offered; use overview page (confirmed 200)
    "bmus_bed_music_education": f"{BASE}/undergraduate/music/overview-programs/degrees-diplomas-offered/",

    # Early Music Performance — confirmed 200
    "performance_early_music_bmus": f"{BASE}/undergraduate/music/programs/performance/early-music-performance-major-bmus/",

    # Faculty Program (classical) — use music research dept page
    "faculty_program_bmus": f"{BASE}/undergraduate/music/programs/music-research/",

    # Faculty Program Jazz — use music research dept page (PDF slug doesn't have HTML counterpart)
    "faculty_program_jazz_bmus": f"{BASE}/undergraduate/music/programs/music-research/",

    # Music Theory — confirmed 200
    "music_theory_major_bmus": f"{BASE}/undergraduate/music/programs/music-research/theory-major-bmus/",

    # Orchestral Instruments — confirmed 200
    "performance_orchestral_bmus": f"{BASE}/undergraduate/music/programs/performance/performance-orchestral-instruments-major-bmus/",
}


def verify_url(url: str) -> tuple[bool, int]:
    """Return (is_ok, status_code). is_ok = True if 200."""
    try:
        r = httpx.get(url, headers=HEADERS, timeout=10, follow_redirects=True)
        return r.status_code == 200, r.status_code
    except Exception as e:
        return False, -1


def main():
    parser = argparse.ArgumentParser(description="Fix dead ecalendar_url values in Supabase.")
    parser.add_argument("--apply", action="store_true", help="Write changes to Supabase (default: dry run)")
    parser.add_argument("--verify", action="store_true", help="HTTP-check each new URL before applying")
    args = parser.parse_args()

    if not SUPABASE_URL or not SUPABASE_KEY:
        print("ERROR: Set SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY (or SUPABASE_KEY) env vars.")
        sys.exit(1)

    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

    print(f"\n{'DRY RUN' if not args.apply else 'APPLYING CHANGES'} — {len(URL_FIXES)} programs to update\n")
    print(f"{'program_key':<45} {'status':<10} {'result'}")
    print("-" * 100)

    applied = skipped = errors = 0

    for program_key, new_url in URL_FIXES.items():
        # Optionally verify the URL is live first
        if args.verify:
            ok, code = verify_url(new_url)
            status = f"HTTP {code}"
            if not ok:
                print(f"{program_key:<45} {status:<10} ⚠  URL still returns non-200 — skipping")
                skipped += 1
                continue
        else:
            status = "unverified"

        if args.apply:
            try:
                result = supabase.table("degree_programs") \
                    .update({"ecalendar_url": new_url}) \
                    .eq("program_key", program_key) \
                    .execute()
                count = len(result.data) if result.data else 0
                if count == 0:
                    print(f"{program_key:<45} {status:<10} ⚠  No row matched — check program_key spelling")
                    skipped += 1
                else:
                    print(f"{program_key:<45} {status:<10} ✓  Updated → {new_url}")
                    applied += 1
            except Exception as e:
                print(f"{program_key:<45} {status:<10} ✗  DB error: {e}")
                errors += 1
        else:
            # Dry run — just show what would happen
            print(f"{program_key:<45} {status:<10} →  {new_url}")
            applied += 1

    print("\n" + "=" * 100)
    if args.apply:
        print(f"Done. Applied: {applied}  |  Skipped: {skipped}  |  Errors: {errors}")
    else:
        print(f"Dry run complete. {applied} changes would be applied. Run with --apply to execute.")
        print("Add --verify to HTTP-check each URL before applying.")


if __name__ == "__main__":
    main()