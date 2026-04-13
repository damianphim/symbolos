"""
McGill Schulich School of Music – Degree Requirements Seed Data
Source: McGill Course Catalogue 2025-2026 & Official Program Pages
https://coursecatalogue.mcgill.ca/en/undergraduate/music/
https://www.mcgill.ca/music/programs/bmus

This file covers all undergraduate B.Mus. programs plus the concurrent B.Mus./B.Ed.:

  Performance Department:
    1. Voice Performance (B.Mus.)           – 123 credits
    2. Piano Performance (B.Mus.)           – 125 credits
    3. Orchestral Instruments (B.Mus.)      – 125 credits
    4. Organ / Guitar (B.Mus.)              – 125 credits
    5. Early Music Performance (B.Mus.)     – 125 credits
    6. Early Music Voice (B.Mus.)           – 126 credits
    7. Jazz Performance (B.Mus.)            – 126 credits

  Music Research Department:
    8.  Composition Major (B.Mus.)          – 124 credits
    9.  Music History Major (B.Mus.)        – 124 credits
   10.  Music Theory Major (B.Mus.)         – 124 credits
   11.  Music Studies Major (B.Mus.)        – 123 credits  [Fall 2025+]
   12.  Faculty Program – General (B.Mus.) – 123 credits  [pre-2025]
   13.  Faculty Program – Jazz (B.Mus.)    – 123 credits

  Concurrent:
   14.  B.Mus. / B.Ed. Music Education      – 170 credits

Accuracy notes:
  - All programs require an audition for admission into Schulich.
  - MUSP 170/171 (Keyboard Proficiency) are waived for students whose principal
    instrument is keyboard; MUJZ 170/171 substitutes for Jazz majors.
  - Quebec CEGEP Music graduates may be exempt from MUHL 186, some MUTH and MUSP
    courses via placement exams; out-of-province students complete a Freshman/Foundation
    year of prerequisite courses before the core program.
  - MUIN practical lesson credits carry a supplemental per-credit Music Private Lesson Fee
    in addition to regular tuition.
  - Continuation in performance programs requires min. B- in practical instruction and
    ensemble courses; research programs require min. B- in designated major courses.
  - Students may add B.Mus. minors (Composition, Conducting, Early Music, Jazz Performance,
    Music Education, Music History, Music Theory, Applied Performance Sciences, Music
    Entrepreneurship, Technology) or minors from other faculties.
  - Music Studies program (prog_key: music_studies_bmus) is for students admitted Fall 2025
    or later; Faculty Program (music_faculty_bmus) is for Fall 2024 and prior.
"""

import logging
logger = logging.getLogger(__name__)


# ─────────────────────────────────────────────────────────────────────────────
# Common core courses shared across all B.Mus. programs
# (listed separately for clarity; each program's blocks reference them)
# ─────────────────────────────────────────────────────────────────────────────

BMUS_CORE = [
    {"subject": "MUHL", "catalog": "186",  "title": "Western Musical Traditions",     "credits": 3, "is_required": True,  "recommended": True,  "recommendation_reason": "Survey of Western music from the Middle Ages to present; required for all BMus programs in Year 1"},
    {"subject": "MUTH", "catalog": "150",  "title": "Theory and Analysis 1",          "credits": 3, "is_required": True,  "recommended": True,  "recommendation_reason": "Diatonic harmony, voice leading, counterpoint; Year 1 Fall"},
    {"subject": "MUTH", "catalog": "151",  "title": "Theory and Analysis 2",          "credits": 3, "is_required": True,  "recommended": True,  "recommendation_reason": "Continuation of Theory 1; Year 1 Winter"},
    {"subject": "MUTH", "catalog": "250",  "title": "Theory and Analysis 3",          "credits": 3, "is_required": True,  "recommended": True,  "recommendation_reason": "Chromatic harmony; modulation; Year 2 Fall"},
    {"subject": "MUTH", "catalog": "251",  "title": "Theory and Analysis 4",          "credits": 3, "is_required": True,  "recommended": True,  "recommendation_reason": "Advanced chromatic harmony and 19th-century forms; Year 2 Winter"},
    {"subject": "MUSP", "catalog": "140",  "title": "Musicianship Training 1",        "credits": 2, "is_required": True,  "recommended": True,  "recommendation_reason": "Sight-singing, dictation, rhythmic training; Year 1 Fall"},
    {"subject": "MUSP", "catalog": "141",  "title": "Musicianship Training 2",        "credits": 2, "is_required": True,  "recommended": True,  "recommendation_reason": "Continuation of Musicianship 1; Year 1 Winter"},
    {"subject": "MUSP", "catalog": "170",  "title": "Musicianship (Keyboard) 1",      "credits": 1, "is_required": True,  "recommended": False, "recommendation_reason": "Keyboard proficiency: harmonisation, transposition; waived for keyboard/guitar principals"},
    {"subject": "MUSP", "catalog": "171",  "title": "Musicianship (Keyboard) 2",      "credits": 1, "is_required": True,  "recommended": False, "recommendation_reason": "Continuation of keyboard proficiency; waived for keyboard principals"},
    {"subject": "MUPD", "catalog": "135",  "title": "Music as a Profession 1",        "credits": 1, "is_required": True,  "recommended": True,  "recommendation_reason": "Introduction to professional, mental-health and well-being skills for musicians; Year 1 Fall"},
    {"subject": "MUIN", "catalog": "180",  "title": "BMus Practical Lessons 1",       "credits": 3, "is_required": True,  "recommended": True,  "recommendation_reason": "Private instruction on principal instrument/voice; Year 1 Fall"},
    {"subject": "MUIN", "catalog": "181",  "title": "BMus Practical Lessons 2",       "credits": 3, "is_required": True,  "recommended": True,  "recommendation_reason": "Private instruction on principal instrument/voice; Year 1 Winter"},
    {"subject": "MUHL", "catalog": "286",  "title": "Critical Thinking About Music",  "credits": 3, "is_required": True,  "recommended": True,  "recommendation_reason": "Research methods, writing, and analytical skills for music scholars; Year 2 or 3"},
    {"subject": "MUSP", "catalog": "240",  "title": "Musicianship Training 3",        "credits": 2, "is_required": True,  "recommended": True,  "recommendation_reason": "Advanced sight-singing and dictation; Year 2 Fall"},
    {"subject": "MUSP", "catalog": "241",  "title": "Musicianship Training 4",        "credits": 2, "is_required": True,  "recommended": True,  "recommendation_reason": "Advanced musicianship; Year 2 Winter"},
    {"subject": "MUPD", "catalog": "235",  "title": "Music as a Profession 2",        "credits": 1, "is_required": True,  "recommended": True,  "recommendation_reason": "Advanced professional development: career planning, entrepreneurship; Year 2"},
    {"subject": "MUIN", "catalog": "280",  "title": "BMus Practical Lessons 3",       "credits": 2.5,"is_required": True, "recommended": True,  "recommendation_reason": "Private instruction, Year 2 Fall; note 2.5-credit weight"},
    {"subject": "MUIN", "catalog": "281",  "title": "BMus Practical Lessons 4",       "credits": 2.5,"is_required": True, "recommended": True,  "recommendation_reason": "Private instruction, Year 2 Winter; note 2.5-credit weight"},
    {"subject": "MUIN", "catalog": "283",  "title": "BMus Concentration Final Exam",  "credits": 1, "is_required": True,  "recommended": True,  "recommendation_reason": "Applied for in the semester you plan to perform the jury examination"},
]

MUTH_350 = {"subject": "MUTH", "catalog": "350", "title": "Theory and Analysis 5", "credits": 3, "is_required": True, "recommended": True, "recommendation_reason": "Post-tonal theory and analysis; Year 3"}

# Upper-year practical lessons (Years 3–4) used by most performance programs
UPPER_LESSONS = [
    {"subject": "MUIN", "catalog": "380", "title": "BMus Practical Lessons 5",  "credits": 2.5, "is_required": True, "recommended": True, "recommendation_reason": "Private instruction Year 3 Fall"},
    {"subject": "MUIN", "catalog": "381", "title": "BMus Practical Lessons 6",  "credits": 2.5, "is_required": True, "recommended": True, "recommendation_reason": "Private instruction Year 3 Winter"},
    {"subject": "MUIN", "catalog": "480", "title": "BMus Practical Lessons 7",  "credits": 2,   "is_required": True, "recommended": True, "recommendation_reason": "Private instruction Year 4 Fall"},
    {"subject": "MUIN", "catalog": "481", "title": "BMus Practical Lessons 8",  "credits": 2,   "is_required": True, "recommended": True, "recommendation_reason": "Private instruction Year 4 Winter"},
    {"subject": "MUIN", "catalog": "282", "title": "BMus Perf Practical Exam 1", "credits": 1,  "is_required": True, "recommended": True, "recommendation_reason": "Applied for separately; Year 2 jury exam"},
    {"subject": "MUIN", "catalog": "382", "title": "BMus Perf Practical Exam 2", "credits": 1,  "is_required": True, "recommended": True, "recommendation_reason": "Applied for separately; Year 3 jury exam"},
    {"subject": "MUIN", "catalog": "482", "title": "BMus Perf Practical Exam 3", "credits": 2,  "is_required": True, "recommended": True, "recommendation_reason": "Final jury / recital exam; Year 4"},
]


# ─────────────────────────────────────────────────────────────────────────────
MUSIC_PROGRAMS = [

  # ══════════════════════════════════════════════════════════════════════════
  #  1. VOICE PERFORMANCE – B.MUS. (123 credits)
  # ══════════════════════════════════════════════════════════════════════════
  {
    "program_key":   "performance_voice_bmus",
    "name":          "Voice Performance – B.Mus. (Major) (123 credits)",
    "program_type":  "major",
    "faculty":       "Schulich School of Music",
    "total_credits": 123,
    "description": (
      "The B.Mus. Major in Voice Performance provides comprehensive training in the "
      "practical and theoretical elements of classical singing. Students receive weekly "
      "private vocal instruction, participate in opera scenes, art-song coaching, "
      "choral ensembles, and opera productions. Language diction courses in Italian, "
      "German, and French are required. A minimum grade of B- is required in all "
      "practical instruction, exams, and ensemble courses."
    ),
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/music/programs/performance/performance-voice-major-bmus/",
    "blocks": [
      {
        "block_key": "voice_core",
        "title": "Core Music Requirements (all B.Mus. programs)",
        "block_type": "required",
        "credits_needed": None,
        "courses_needed": None,
        "group_name": None,
        "notes": "Shared foundation required in all BMus programs: music theory, musicianship, keyboard proficiency, music history, practical lessons, and professional development. Voice Performance also requires MUTH 350 Theory and Analysis 5.",
        "sort_order": 1,
        "courses": BMUS_CORE + [MUTH_350],
      },
      {
        "block_key": "voice_upper_lessons",
        "title": "Upper-Year Practical Instruction & Exams (Years 3–4)",
        "block_type": "required",
        "credits_needed": None,
        "courses_needed": None,
        "group_name": None,
        "notes": "Private voice lessons in Years 3 and 4, plus three jury/practical exams applied for separately each year.",
        "sort_order": 2,
        "courses": UPPER_LESSONS,
      },
      {
        "block_key": "voice_diction",
        "title": "Vocal Diction & Language Courses",
        "block_type": "required",
        "credits_needed": None,
        "courses_needed": None,
        "group_name": None,
        "notes": "All five diction courses (9 credits total) are required for voice performance majors. A language requirement applies concurrently: evidence of Italian (ITAL 205D1/D2 or equivalent), German (GERM 202 or equivalent), and English second language as applicable.",
        "sort_order": 3,
        "courses": [
          {"subject": "MUPG", "catalog": "209", "title": "Introduction to Lyric Diction", "credits": 1, "is_required": True,  "recommended": True,  "recommendation_reason": "Foundational IPA and lyric diction survey; Year 1 or 2; required for all voice performance majors"},
          {"subject": "MUPG", "catalog": "210", "title": "Italian Diction",               "credits": 2, "is_required": True,  "recommended": True,  "recommendation_reason": "IPA-based Italian lyric diction; essential for operatic and song repertoire"},
          {"subject": "MUPG", "catalog": "211", "title": "French Diction",                "credits": 2, "is_required": True,  "recommended": True,  "recommendation_reason": "French mélodie and opera diction"},
          {"subject": "MUPG", "catalog": "212", "title": "English Diction",               "credits": 2, "is_required": True,  "recommended": True,  "recommendation_reason": "English lyric diction; required for English song repertoire"},
          {"subject": "MUPG", "catalog": "213", "title": "German Diction",                "credits": 2, "is_required": True,  "recommended": True,  "recommendation_reason": "German Lied and opera diction"},
        ],
      },
      {
        "block_key": "voice_ensembles",
        "title": "Complementary Performance – Ensembles & Voice Courses (10 credits)",
        "block_type": "choose_credits",
        "credits_needed": 10,
        "courses_needed": None,
        "group_name": None,
        "notes": "10 credits of complementary performance from approved ensemble and voice-specific courses. Voice majors are primarily assigned to choral ensembles and opera production ensembles.",
        "sort_order": 4,
        "courses": [
          {"subject": "MUEN", "catalog": "593", "title": "Choral Ensembles",                       "credits": 2, "is_required": False, "recommended": True,  "choose_from_group": "voice_performance", "choose_n_credits": 10, "recommendation_reason": "Primary large ensemble for voice students; assigned each semester"},
          {"subject": "MUEN", "catalog": "587", "title": "Cappella McGill",                         "credits": 2, "is_required": False, "recommended": True,  "choose_from_group": "voice_performance", "choose_n_credits": 10, "recommendation_reason": "McGill's premier choral ensemble"},
          {"subject": "MUEN", "catalog": "572", "title": "Cappella Antica",                         "credits": 2, "is_required": False, "recommended": False, "choose_from_group": "voice_performance", "choose_n_credits": 10},
          {"subject": "MUEN", "catalog": "454", "title": "Introductory Opera Repertoire Experience","credits": 2, "is_required": False, "recommended": True,  "choose_from_group": "voice_performance", "choose_n_credits": 10, "recommendation_reason": "Opera scenes workshop for voice students"},
          {"subject": "MUEN", "catalog": "496", "title": "Opera Studio",                            "credits": 2, "is_required": False, "recommended": True,  "choose_from_group": "voice_performance", "choose_n_credits": 10, "recommendation_reason": "Full opera production; audition required"},
          {"subject": "MUEN", "catalog": "578", "title": "Song Interpretation 1",                  "credits": 1, "is_required": False, "recommended": True,  "choose_from_group": "voice_performance", "choose_n_credits": 10, "recommendation_reason": "Art-song coaching and masterclass"},
          {"subject": "MUEN", "catalog": "579", "title": "Song Interpretation 2",                  "credits": 1, "is_required": False, "recommended": False, "choose_from_group": "voice_performance", "choose_n_credits": 10},
          {"subject": "MUEN", "catalog": "580", "title": "Early Music Ensemble",                   "credits": 1, "is_required": False, "recommended": False, "choose_from_group": "voice_performance", "choose_n_credits": 10},
          {"subject": "MUEN", "catalog": "563", "title": "Jazz Vocal Workshop",                     "credits": 2, "is_required": False, "recommended": False, "choose_from_group": "voice_performance", "choose_n_credits": 10},
          {"subject": "MUEN", "catalog": "594", "title": "Contemporary Music Ensemble",             "credits": 2, "is_required": False, "recommended": False, "choose_from_group": "voice_performance", "choose_n_credits": 10},
          {"subject": "MUIN", "catalog": "300", "title": "Voice Coaching 1",                        "credits": 2, "is_required": False, "recommended": True,  "choose_from_group": "voice_performance", "choose_n_credits": 10, "recommendation_reason": "Private voice coaching complement to principal lessons"},
          {"subject": "MUIN", "catalog": "301", "title": "Voice Coaching 2",                        "credits": 2, "is_required": False, "recommended": True,  "choose_from_group": "voice_performance", "choose_n_credits": 10, "recommendation_reason": "Continuation of voice coaching"},
          {"subject": "MUPG", "catalog": "296", "title": "Acting for Voice",                        "credits": 1, "is_required": False, "recommended": True,  "choose_from_group": "voice_performance", "choose_n_credits": 10, "recommendation_reason": "Stage acting technique for opera and art song"},
          {"subject": "MUPG", "catalog": "297", "title": "Movement for Voice",                      "credits": 1, "is_required": False, "recommended": False, "choose_from_group": "voice_performance", "choose_n_credits": 10},
          {"subject": "MUPG", "catalog": "300", "title": "Music Performance Strategies",            "credits": 3, "is_required": False, "recommended": True,  "choose_from_group": "voice_performance", "choose_n_credits": 10, "recommendation_reason": "Performance psychology and stage preparation"},
          {"subject": "MUPG", "catalog": "309", "title": "Advanced Diction",                        "credits": 1, "is_required": False, "recommended": False, "choose_from_group": "voice_performance", "choose_n_credits": 10},
          {"subject": "MUPG", "catalog": "353", "title": "Song Repertoire Class",                   "credits": 2, "is_required": False, "recommended": True,  "choose_from_group": "voice_performance", "choose_n_credits": 10, "recommendation_reason": "Art-song and vocal chamber music repertoire survey"},
          {"subject": "MUPG", "catalog": "380", "title": "Oratorio Class",                          "credits": 2, "is_required": False, "recommended": False, "choose_from_group": "voice_performance", "choose_n_credits": 10},
          {"subject": "MUPG", "catalog": "453", "title": "Contemporary Repertoire for Voice",       "credits": 2, "is_required": False, "recommended": False, "choose_from_group": "voice_performance", "choose_n_credits": 10},
        ],
      },
      {
        "block_key": "voice_history_electives",
        "title": "Music History / Performance Practice (6 credits)",
        "block_type": "choose_credits",
        "credits_needed": 6,
        "courses_needed": None,
        "group_name": None,
        "notes": "6 credits from the approved MUHL history/literature list for voice majors. The official list emphasises opera and Lied repertoire.",
        "sort_order": 5,
        "courses": [
          {"subject": "MUHL", "catalog": "377", "title": "Baroque Opera",             "credits": 3, "is_required": False, "recommended": True,  "choose_from_group": "music_history_300", "choose_n_credits": 6, "recommendation_reason": "Directly relevant for opera singers; core voice history course"},
          {"subject": "MUHL", "catalog": "387", "title": "Opera from Mozart to Puccini","credits": 3,"is_required": False, "recommended": True,  "choose_from_group": "music_history_300", "choose_n_credits": 6, "recommendation_reason": "Core operatic repertoire for voice students"},
          {"subject": "MUHL", "catalog": "388", "title": "Opera After 1900",          "credits": 3, "is_required": False, "recommended": True,  "choose_from_group": "music_history_300", "choose_n_credits": 6, "recommendation_reason": "20th-century opera repertoire; voice-specific"},
          {"subject": "MUHL", "catalog": "390", "title": "The German Lied",           "credits": 3, "is_required": False, "recommended": True,  "choose_from_group": "music_history_300", "choose_n_credits": 6, "recommendation_reason": "Art-song history; directly relevant for voice students"},
          {"subject": "MUHL", "catalog": "382", "title": "Baroque Music",             "credits": 3, "is_required": False, "recommended": False, "choose_from_group": "music_history_300", "choose_n_credits": 6},
          {"subject": "MUHL", "catalog": "383", "title": "Classical Music",           "credits": 3, "is_required": False, "recommended": False, "choose_from_group": "music_history_300", "choose_n_credits": 6},
        ],
      },
    ],
  },

  # ══════════════════════════════════════════════════════════════════════════
  #  2. PIANO PERFORMANCE – B.MUS. (125 credits)
  # ══════════════════════════════════════════════════════════════════════════
  {
    "program_key":   "performance_piano_bmus",
    "name":          "Piano Performance – B.Mus. (Major) (125 credits)",
    "program_type":  "major",
    "faculty":       "Schulich School of Music",
    "total_credits": 125,
    "description": (
      "The B.Mus. in Piano Performance provides intensive individual instruction from "
      "world-class faculty, combined with chamber music, piano ensemble, and large "
      "ensemble participation. Three jury exams (MUIN 282, 382, 482) are required across "
      "Years 2–4. Pianists are automatically exempt from MUSP 170/171 keyboard proficiency. "
      "A minimum grade of B- is required in all practical instruction, exams, and ensembles."
    ),
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/music/programs/performance/performance-piano-major-bmus/",
    "blocks": [
      {
        "block_key": "piano_core",
        "title": "Core Music Requirements (all B.Mus. programs)",
        "block_type": "required",
        "credits_needed": None, "courses_needed": None, "group_name": None,
        "notes": "Note: Piano majors are automatically exempt from MUSP 170 and MUSP 171 (keyboard proficiency).",
        "sort_order": 1,
        "courses": BMUS_CORE,
      },
      {
        "block_key": "piano_upper_lessons",
        "title": "Upper-Year Practical Instruction & Exams (Years 3–4)",
        "block_type": "required",
        "credits_needed": None, "courses_needed": None, "group_name": None,
        "notes": "Private piano lessons Years 3–4 plus three required jury examinations.",
        "sort_order": 2,
        "courses": UPPER_LESSONS,
      },
      {
        "block_key": "piano_chamber",
        "title": "Chamber Music & Ensembles",
        "block_type": "required",
        "credits_needed": 8,
        "courses_needed": None, "group_name": None,
        "notes": "8 credits total: 4 credits large ensemble (Years 1–2) plus chamber music and other MUEN courses. Large ensemble first four semesters is required.",
        "sort_order": 3,
        "courses": [
          {"subject": "MUEN", "catalog": "597", "title": "McGill Symphony Orchestra",  "credits": 2, "is_required": False, "recommended": True, "choose_from_group": "ensembles", "recommendation_reason": "Required large ensemble (4 credits over 4 semesters in Years 1–2)"},
          {"subject": "MUEN", "catalog": "590", "title": "McGill Wind Orchestra",       "credits": 2, "is_required": False, "recommended": False, "choose_from_group": "ensembles"},
          {"subject": "MUEN", "catalog": "593", "title": "Choral Ensembles",            "credits": 2, "is_required": False, "recommended": False, "choose_from_group": "ensembles"},
          {"subject": "MUEN", "catalog": "560", "title": "Piano Ensemble",              "credits": 1, "is_required": False, "recommended": True,  "choose_from_group": "ensembles", "recommendation_reason": "Chamber music credit for pianists"},
          {"subject": "MUEN", "catalog": "564", "title": "Piano Accompaniment Lab",     "credits": 1, "is_required": False, "recommended": True,  "choose_from_group": "ensembles", "recommendation_reason": "Collaborative piano skills"},
        ],
      },
      {
        "block_key": "piano_specific_required",
        "title": "Piano-Specific Required Courses",
        "block_type": "required",
        "credits_needed": None, "courses_needed": None, "group_name": None,
        "notes": "Courses specific to the Piano Performance major including advanced seminars, repertoire studies, piano techniques, concerto, and Theory 5. Pass/fail courses (0 credits) are graded P/F and do not count toward credit totals.",
        "sort_order": 4,
        "courses": [
          {"subject": "MUPG", "catalog": "357",  "title": "Piano Repertoire Studies 2",  "credits": 2, "is_required": True, "recommended": True, "recommendation_reason": "Piano repertoire survey; Year 3"},
          {"subject": "MUPG", "catalog": "541",  "title": "Senior Piano Seminar 1",      "credits": 2, "is_required": True, "recommended": True, "recommendation_reason": "Advanced seminar for senior piano students; Year 4 Fall"},
          {"subject": "MUPG", "catalog": "542",  "title": "Senior Piano Seminar 2",      "credits": 2, "is_required": True, "recommended": True, "recommendation_reason": "Continuation; Year 4 Winter"},
          {"subject": "MUTH", "catalog": "350",  "title": "Theory and Analysis 5",       "credits": 3, "is_required": True, "recommended": True, "recommendation_reason": "Post-tonal theory and analysis; required for Piano Performance major"},
          {"subject": "MUIN", "catalog": "333",  "title": "Piano Techniques 2",          "credits": 0, "is_required": True, "recommended": True, "recommendation_reason": "Pass/fail; piano technique seminar; Year 2–3"},
          {"subject": "MUIN", "catalog": "369",  "title": "Concerto",                    "credits": 0, "is_required": True, "recommended": True, "recommendation_reason": "Pass/fail; concerto performance requirement; Year 3–4"},
          {"subject": "MUIN", "catalog": "433",  "title": "Piano Techniques 3",          "credits": 0, "is_required": True, "recommended": True, "recommendation_reason": "Pass/fail; advanced piano technique seminar; Year 3–4"},
        ],
      },
      {
        "block_key": "piano_history_electives",
        "title": "Music History / Performance Practice (upper-level)",
        "block_type": "choose_credits",
        "credits_needed": 6,
        "courses_needed": None, "group_name": None,
        "notes": "6 credits from MUHL or MUPP at 300-level or above, selected in consultation with adviser.",
        "sort_order": 5,
        "courses": [
          {"subject": "MUHL", "catalog": "366", "title": "Era of the Fortepiano",       "credits": 3, "is_required": False, "recommended": True,  "choose_from_group": "music_history_300", "choose_n_credits": 6, "recommendation_reason": "Directly relevant to piano performance history"},
          {"subject": "MUHL", "catalog": "382", "title": "Baroque Music",               "credits": 3, "is_required": False, "recommended": True,  "choose_from_group": "music_history_300", "choose_n_credits": 6},
          {"subject": "MUHL", "catalog": "383", "title": "Classical Music",             "credits": 3, "is_required": False, "recommended": True,  "choose_from_group": "music_history_300", "choose_n_credits": 6},
          {"subject": "MUPP", "catalog": "381", "title": "Topics in Performance Practice", "credits": 3, "is_required": False, "recommended": True, "choose_from_group": "music_history_300", "choose_n_credits": 6},
        ],
      },
    ],
  },

  # ══════════════════════════════════════════════════════════════════════════
  #  3. ORCHESTRAL INSTRUMENTS – B.MUS. (125 credits)
  # ══════════════════════════════════════════════════════════════════════════
  {
    "program_key":   "performance_orchestral_bmus",
    "name":          "Orchestral Instruments – B.Mus. (Major) (125 credits)",
    "program_type":  "major",
    "faculty":       "Schulich School of Music",
    "total_credits": 125,
    "description": (
      "The B.Mus. in Orchestral Instruments covers all standard orchestral string, wind, "
      "brass, and percussion instruments. Students receive private instruction and participate "
      "in the McGill Symphony Orchestra, Contemporary Music Ensemble, and Wind Orchestra. "
      "Violin, viola, and cello majors must begin with two terms each of MUEN 565 (String "
      "Quartet) and MUEN 560. A minimum grade of B- is required in practical instruction, "
      "exams, and ensembles."
    ),
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/music/programs/performance/orchestral-instruments-major-bmus/",
    "blocks": [
      {
        "block_key": "orch_core",
        "title": "Core Music Requirements (all B.Mus. programs)",
        "block_type": "required",
        "credits_needed": None, "courses_needed": None, "group_name": None,
        "notes": "Percussionists must also include 3 credits of non-music electives.",
        "sort_order": 1,
        "courses": BMUS_CORE,
      },
      {
        "block_key": "orch_upper_lessons",
        "title": "Upper-Year Practical Instruction & Exams (Years 3–4)",
        "block_type": "required",
        "credits_needed": None, "courses_needed": None, "group_name": None,
        "notes": "Private lessons Years 3–4 plus three jury exams applied for separately.",
        "sort_order": 2,
        "courses": UPPER_LESSONS,
      },
      {
        "block_key": "orch_ensembles",
        "title": "Ensembles",
        "block_type": "required",
        "credits_needed": 8,
        "courses_needed": None, "group_name": None,
        "notes": "8 credits of ensemble courses (MUEN prefix). String players (violin/viola/cello) begin with 2 terms of MUEN 565 String Quartet Seminar.",
        "sort_order": 3,
        "courses": [
          {"subject": "MUEN", "catalog": "597", "title": "McGill Symphony Orchestra",        "credits": 2, "is_required": False, "recommended": True,  "choose_from_group": "ensembles", "recommendation_reason": "Primary large ensemble for most orchestral instrument students"},
          {"subject": "MUEN", "catalog": "590", "title": "McGill Wind Orchestra",            "credits": 2, "is_required": False, "recommended": True,  "choose_from_group": "ensembles", "recommendation_reason": "Primary large ensemble for wind and brass students"},
          {"subject": "MUEN", "catalog": "565", "title": "String Quartet Seminar",          "credits": 1, "is_required": False, "recommended": True,  "choose_from_group": "ensembles", "recommendation_reason": "Required for violin, viola, cello majors (2 terms minimum)"},
          {"subject": "MUEN", "catalog": "560", "title": "Chamber Music",                   "credits": 1, "is_required": False, "recommended": True,  "choose_from_group": "ensembles", "recommendation_reason": "Chamber music training for string players"},
          {"subject": "MUEN", "catalog": "591", "title": "Contemporary Music Ensemble",     "credits": 1, "is_required": False, "recommended": False, "choose_from_group": "ensembles"},
        ],
      },
      {
        "block_key": "orch_history_electives",
        "title": "Music History / Performance Practice (upper-level)",
        "block_type": "choose_credits",
        "credits_needed": 6,
        "courses_needed": None, "group_name": None,
        "notes": "6 credits from MUHL or MUPP at 300-level or above.",
        "sort_order": 4,
        "courses": [
          {"subject": "MUHL", "catalog": "380", "title": "Medieval Music",            "credits": 3, "is_required": False, "recommended": False, "choose_from_group": "music_history_300", "choose_n_credits": 6},
          {"subject": "MUHL", "catalog": "381", "title": "Renaissance Music",         "credits": 3, "is_required": False, "recommended": False, "choose_from_group": "music_history_300", "choose_n_credits": 6},
          {"subject": "MUHL", "catalog": "382", "title": "Baroque Music",             "credits": 3, "is_required": False, "recommended": True,  "choose_from_group": "music_history_300", "choose_n_credits": 6},
          {"subject": "MUHL", "catalog": "383", "title": "Classical Music",           "credits": 3, "is_required": False, "recommended": True,  "choose_from_group": "music_history_300", "choose_n_credits": 6},
          {"subject": "MUPP", "catalog": "381", "title": "Topics in Performance Practice", "credits": 3, "is_required": False, "recommended": True, "choose_from_group": "music_history_300", "choose_n_credits": 6},
        ],
      },
    ],
  },

  # ══════════════════════════════════════════════════════════════════════════
  #  4. JAZZ PERFORMANCE – B.MUS. (126 credits)
  # ══════════════════════════════════════════════════════════════════════════
  {
    "program_key":   "performance_jazz_bmus",
    "name":          "Jazz Performance – B.Mus. (Major) (126 credits)",
    "program_type":  "major",
    "faculty":       "Schulich School of Music",
    "total_credits": 126,
    "description": (
      "The B.Mus. in Jazz Performance covers jazz theory and harmony, keyboard, history, "
      "performance practice, improvisation, composition, and arranging. Students receive "
      "private instruction and participate in McGill's jazz orchestras, chamber jazz "
      "orchestra, and approximately twenty combos. Jazz guitarists and pianists are "
      "automatically exempt from MUJZ 170/171 keyboard proficiency. Rhythm section players "
      "(piano, guitar, bass, drums, vibraphone) may substitute 4 credits of large ensemble "
      "with free electives. A minimum grade of B- is required in all MUJZ-prefix courses, "
      "practical instruction, and ensemble courses."
    ),
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/music/programs/performance/performance-jazz-major-bmus/",
    "blocks": [
      {
        "block_key": "jazz_theory_history",
        "title": "Jazz Theory, History & Keyboard",
        "block_type": "required",
        "credits_needed": None, "courses_needed": None, "group_name": None,
        "notes": "Jazz-specific theory and history courses replace general MUTH/MUHL requirements in Years 1–2. Keyboard proficiency substituted by MUJZ 170/171 for all Jazz majors.",
        "sort_order": 1,
        "courses": [
          {"subject": "MUJZ", "catalog": "160",  "title": "Jazz Materials 1",            "credits": 3, "is_required": True, "recommended": True, "recommendation_reason": "Jazz harmony, scales, chord symbols; Year 1 Fall"},
          {"subject": "MUJZ", "catalog": "161",  "title": "Jazz Materials 2",            "credits": 3, "is_required": True, "recommended": True, "recommendation_reason": "Continuation; Year 1 Winter"},
          {"subject": "MUJZ", "catalog": "170",  "title": "Jazz Keyboard Proficiency 1", "credits": 1, "is_required": True, "recommended": True, "recommendation_reason": "Jazz voicings, comping basics; waived for guitar/piano majors"},
          {"subject": "MUJZ", "catalog": "171",  "title": "Jazz Keyboard Proficiency 2", "credits": 1, "is_required": True, "recommended": True, "recommendation_reason": "Advanced jazz keyboard; waived for guitar/piano majors"},
          {"subject": "MUJZ", "catalog": "187",  "title": "Jazz History Survey",                 "credits": 3, "is_required": True, "recommended": True, "recommendation_reason": "Overview of jazz from its origins to the present; Year 1"},
          {"subject": "MUJZ", "catalog": "223",  "title": "Jazz Improvisation/Musicianship 1",   "credits": 3, "is_required": True, "recommended": True, "recommendation_reason": "Jazz improvisation foundations and ear training for instrumental majors; Year 2 Fall"},
          {"subject": "MUJZ", "catalog": "224",  "title": "Jazz Improvisation/Musicianship 2",   "credits": 3, "is_required": True, "recommended": True, "recommendation_reason": "Continuation; Year 2 Winter. Vocal majors substitute MUJZ 225/226."},
          {"subject": "MUJZ", "catalog": "260",  "title": "Jazz Arranging 1",                    "credits": 3, "is_required": True, "recommended": True, "recommendation_reason": "Introduction to jazz arranging; Year 2 Fall"},
          {"subject": "MUJZ", "catalog": "261",  "title": "Jazz Arranging 2",                    "credits": 3, "is_required": True, "recommended": True, "recommendation_reason": "Continuation; Year 2 Winter"},
          {"subject": "MUJZ", "catalog": "340",  "title": "Jazz Composition 1",                  "credits": 3, "is_required": True, "recommended": True, "recommendation_reason": "Jazz composition; Year 3 Fall"},
          {"subject": "MUJZ", "catalog": "341",  "title": "Jazz Composition 2",                  "credits": 3, "is_required": True, "recommended": True, "recommendation_reason": "Continuation; Year 3 Winter"},
          {"subject": "MUJZ", "catalog": "423",  "title": "Jazz Improvisation/Musicianship 3",   "credits": 3, "is_required": True, "recommended": True, "recommendation_reason": "Advanced improvisation and ear training for instrumental majors; Year 3 Fall"},
          {"subject": "MUJZ", "catalog": "424",  "title": "Jazz Improvisation/Musicianship 4",   "credits": 3, "is_required": True, "recommended": True, "recommendation_reason": "Continuation; Year 3 Winter. Vocal majors substitute MUJZ 325/326."},
          {"subject": "MUJZ", "catalog": "493",  "title": "Jazz Performance Practice",           "credits": 3, "is_required": True, "recommended": True, "recommendation_reason": "Jazz history and performance practice seminar; required; Year 3 Winter"},
        ],
      },
      {
        "block_key": "jazz_composition_arranging",
        "title": "Advanced Composition or Arranging (choose one track)",
        "block_type": "choose_credits",
        "credits_needed": 4,
        "courses_needed": None, "group_name": None,
        "notes": "4 credits: choose either MUJZ 440+441 (Composition) OR MUJZ 461D1/D2 (Advanced Arranging). Rhythm section instruments only.",
        "sort_order": 2,
        "courses": [
          {"subject": "MUJZ", "catalog": "440", "title": "Advanced Jazz Composition 1",  "credits": 2, "is_required": False, "recommended": True,  "choose_from_group": "jazz_comp_arr", "choose_n_credits": 4, "recommendation_reason": "Track A – Jazz composition"},
          {"subject": "MUJZ", "catalog": "441", "title": "Advanced Jazz Composition 2",  "credits": 2, "is_required": False, "recommended": True,  "choose_from_group": "jazz_comp_arr", "choose_n_credits": 4},
          {"subject": "MUJZ", "catalog": "461D1","title": "Advanced Jazz Arranging D1",  "credits": 2, "is_required": False, "recommended": False, "choose_from_group": "jazz_comp_arr", "choose_n_credits": 4, "recommendation_reason": "Track B – Advanced jazz arranging"},
          {"subject": "MUJZ", "catalog": "461D2","title": "Advanced Jazz Arranging D2",  "credits": 2, "is_required": False, "recommended": False, "choose_from_group": "jazz_comp_arr", "choose_n_credits": 4},
        ],
      },
      {
        "block_key": "jazz_practical_lessons",
        "title": "Practical Instruction (Private Lessons)",
        "block_type": "required",
        "credits_needed": None, "courses_needed": None, "group_name": None,
        "notes": "Private lessons across all four years plus jury exams applied for separately.",
        "sort_order": 3,
        "courses": [
          {"subject": "MUPD", "catalog": "135",  "title": "Music as a Profession 1",     "credits": 1, "is_required": True, "recommended": True, "recommendation_reason": "Professional development; Year 1"},
          {"subject": "MUPD", "catalog": "235",  "title": "Music as a Profession 2",     "credits": 1, "is_required": True, "recommended": True, "recommendation_reason": "Advanced professional development; Year 2"},
          {"subject": "MUIN", "catalog": "180",  "title": "BMus Practical Lessons 1",    "credits": 3, "is_required": True, "recommended": True, "recommendation_reason": "Year 1 Fall"},
          {"subject": "MUIN", "catalog": "181",  "title": "BMus Practical Lessons 2",    "credits": 3, "is_required": True, "recommended": True, "recommendation_reason": "Year 1 Winter"},
          {"subject": "MUIN", "catalog": "280",  "title": "BMus Practical Lessons 3",    "credits": 2.5,"is_required": True, "recommended": True, "recommendation_reason": "Year 2 Fall"},
          {"subject": "MUIN", "catalog": "281",  "title": "BMus Practical Lessons 4",    "credits": 2.5,"is_required": True, "recommended": True, "recommendation_reason": "Year 2 Winter"},
          {"subject": "MUIN", "catalog": "380",  "title": "BMus Practical Lessons 5",    "credits": 2.5, "is_required": True, "recommended": True, "recommendation_reason": "Year 3 Fall"},
          {"subject": "MUIN", "catalog": "381",  "title": "BMus Practical Lessons 6",    "credits": 2.5, "is_required": True, "recommended": True, "recommendation_reason": "Year 3 Winter"},
          {"subject": "MUIN", "catalog": "480",  "title": "BMus Practical Lessons 7",    "credits": 2,   "is_required": True, "recommended": True, "recommendation_reason": "Year 4 Fall"},
          {"subject": "MUIN", "catalog": "481",  "title": "BMus Practical Lessons 8",    "credits": 2,   "is_required": True, "recommended": True, "recommendation_reason": "Year 4 Winter"},
          {"subject": "MUIN", "catalog": "282",  "title": "BMus Perf Practical Exam 1",  "credits": 1,   "is_required": True, "recommended": True, "recommendation_reason": "Year 2 jury exam"},
          {"subject": "MUIN", "catalog": "382",  "title": "BMus Perf Practical Exam 2",  "credits": 1,   "is_required": True, "recommended": True, "recommendation_reason": "Year 3 jury exam"},
          {"subject": "MUIN", "catalog": "482",  "title": "BMus Perf Practical Exam 3",  "credits": 2,   "is_required": True, "recommended": True, "recommendation_reason": "Final recital exam; Year 4"},
          {"subject": "MUIN", "catalog": "283",  "title": "BMus Concentration Final Exam","credits": 1,"is_required": True, "recommended": True, "recommendation_reason": "Applied for separately"},
        ],
      },
      {
        "block_key": "jazz_ensembles",
        "title": "Jazz Ensembles",
        "block_type": "required",
        "credits_needed": 10,
        "courses_needed": None, "group_name": None,
        "notes": "10 credits: 6 credits MUEN 570 Jazz Combo (6 semesters × 1 credit) + 4 credits large ensemble. Rhythm section instruments may substitute 4 large ensemble credits with free electives.",
        "sort_order": 4,
        "courses": [
          {"subject": "MUEN", "catalog": "570", "title": "Jazz Combo",          "credits": 1, "is_required": True,  "recommended": True,  "recommendation_reason": "Required for 6 semesters (6 credits)"},
          {"subject": "MUEN", "catalog": "563", "title": "Jazz Vocal Workshop", "credits": 1, "is_required": False, "recommended": False, "choose_from_group": "jazz_large_ensemble"},
          {"subject": "MUEN", "catalog": "595", "title": "Jazz Ensembles",      "credits": 2, "is_required": False, "recommended": True,  "choose_from_group": "jazz_large_ensemble", "recommendation_reason": "Primary large jazz ensemble"},
          {"subject": "MUEN", "catalog": "597", "title": "McGill Symphony Orchestra", "credits": 2, "is_required": False, "recommended": False, "choose_from_group": "jazz_large_ensemble"},
        ],
      },
      {
        "block_key": "jazz_muhl",
        "title": "Music History (upper-level electives)",
        "block_type": "choose_credits",
        "credits_needed": 3,
        "courses_needed": None, "group_name": None,
        "notes": "3 credits from MUHL or MUPP at any level.",
        "sort_order": 5,
        "courses": [
          {"subject": "MUHL", "catalog": "386", "title": "History of Jazz",      "credits": 3, "is_required": False, "recommended": True,  "choose_from_group": "jazz_hist", "choose_n_credits": 3, "recommendation_reason": "Highly recommended contextual course for jazz majors"},
          {"subject": "MUHL", "catalog": "383", "title": "Classical Music",      "credits": 3, "is_required": False, "recommended": False, "choose_from_group": "jazz_hist", "choose_n_credits": 3},
          {"subject": "MUHL", "catalog": "388", "title": "Popular Music",        "credits": 3, "is_required": False, "recommended": False, "choose_from_group": "jazz_hist", "choose_n_credits": 3},
        ],
      },
    ],
  },

  # ══════════════════════════════════════════════════════════════════════════
  #  5. EARLY MUSIC PERFORMANCE – B.MUS. (125 credits)
  # ══════════════════════════════════════════════════════════════════════════
  {
    "program_key":   "performance_early_music_bmus",
    "name":          "Early Music Performance – B.Mus. (Major) (125 credits)",
    "program_type":  "major",
    "faculty":       "Schulich School of Music",
    "total_credits": 125,
    "description": (
      "The B.Mus. in Early Music Performance trains performers on historical instruments "
      "including baroque violin, viola, cello, viola da gamba, lute, flute, recorder, oboe, "
      "organ, harpsichord, pianoforte, and early brass. Students participate in Baroque "
      "Orchestra and Cappella Antica. A strong emphasis is placed on historical performance "
      "practice, ornamentation, and improvisation in period styles."
    ),
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/music/programs/performance/early-music-major-bmus/",
    "blocks": [
      {
        "block_key": "early_music_core",
        "title": "Core Music Requirements (all B.Mus. programs)",
        "block_type": "required",
        "credits_needed": None, "courses_needed": None, "group_name": None,
        "notes": "Same foundational core as all B.Mus. programs.",
        "sort_order": 1,
        "courses": BMUS_CORE,
      },
      {
        "block_key": "early_music_upper",
        "title": "Upper-Year Practical Instruction & Exams",
        "block_type": "required",
        "credits_needed": None, "courses_needed": None, "group_name": None,
        "notes": "Private lessons on historical instrument plus three required jury exams.",
        "sort_order": 2,
        "courses": UPPER_LESSONS,
      },
      {
        "block_key": "early_music_specific",
        "title": "Early Music Specific Requirements",
        "block_type": "required",
        "credits_needed": None, "courses_needed": None, "group_name": None,
        "notes": "Courses in historical performance practice and ornamentation required for early music majors.",
        "sort_order": 3,
        "courses": [
          {"subject": "MUSP", "catalog": "354", "title": "Introduction to Improvisation and Ornamentation", "credits": 2, "is_required": True, "recommended": True, "recommendation_reason": "Historical improvisation and ornamentation essential for early music performance"},
          {"subject": "MUSP", "catalog": "381", "title": "Singing Renaissance Notation",                    "credits": 2, "is_required": False,"recommended": True, "recommendation_reason": "Reading mensural notation; important for instrumental and vocal early music"},
          {"subject": "MUPP", "catalog": "381", "title": "Topics in Performance Practice",                  "credits": 3, "is_required": True, "recommended": True, "recommendation_reason": "Historical performance practice: tuning, ornamentation, rhetoric"},
          {"subject": "MUHL", "catalog": "380", "title": "Medieval Music",      "credits": 3, "is_required": False, "recommended": True, "recommendation_reason": "Context for early repertoire"},
          {"subject": "MUHL", "catalog": "381", "title": "Renaissance Music",   "credits": 3, "is_required": False, "recommended": True, "recommendation_reason": "Core historical context for early music performers"},
          {"subject": "MUHL", "catalog": "382", "title": "Baroque Music",       "credits": 3, "is_required": False, "recommended": True, "recommendation_reason": "Core historical context for baroque performance"},
        ],
      },
      {
        "block_key": "early_music_ensembles",
        "title": "Early Music Ensembles",
        "block_type": "required",
        "credits_needed": 8,
        "courses_needed": None, "group_name": None,
        "notes": "8 credits of MUEN ensembles including Baroque Orchestra and Cappella Antica.",
        "sort_order": 4,
        "courses": [
          {"subject": "MUEN", "catalog": "583", "title": "Baroque Orchestra",  "credits": 1, "is_required": True,  "recommended": True, "recommendation_reason": "Primary ensemble for early music instrumentalists"},
          {"subject": "MUEN", "catalog": "584", "title": "Cappella Antica",    "credits": 1, "is_required": False, "recommended": True, "recommendation_reason": "Early choral ensemble; open to early music voice and some instrumentalists"},
          {"subject": "MUEN", "catalog": "593", "title": "Choral Ensembles",   "credits": 2, "is_required": False, "recommended": False, "choose_from_group": "ensembles"},
          {"subject": "MUEN", "catalog": "597", "title": "McGill Symphony Orchestra", "credits": 2, "is_required": False, "recommended": False, "choose_from_group": "ensembles"},
        ],
      },
    ],
  },

  # ══════════════════════════════════════════════════════════════════════════
  #  6. EARLY MUSIC PERFORMANCE – VOICE – B.MUS. (126 credits)
  # ══════════════════════════════════════════════════════════════════════════
  {
    "program_key":   "performance_early_music_voice_bmus",
    "name":          "Early Music Performance – Voice (B.Mus.) (126 credits)",
    "program_type":  "major",
    "faculty":       "Schulich School of Music",
    "total_credits": 126,
    "description": (
      "The B.Mus. in Early Music Performance – Voice trains singers in historical vocal "
      "styles from the medieval through baroque periods. Students receive private voice "
      "instruction and coaching (MUIN 300/301), participate in Cappella Antica and Early "
      "Music Ensemble, and complete comprehensive lyric diction in Italian, French, English, "
      "and German (MUPG 209–213). The program requires Theory and Analysis 5 (MUTH 350), "
      "Topics in Early Music Analysis (MUTH 426), Topics in Performance Practice (MUPP 381), "
      "and three practical jury examinations across Years 2–4. The voice variant carries "
      "126 credits due to diction and voice coaching requirements beyond the instruments variant."
    ),
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/music/programs/performance/early-music-performance-voice-major-bmus/",
    "blocks": [
      {
        "block_key": "early_music_voice_core",
        "title": "Core Music Requirements (all B.Mus. programs)",
        "block_type": "required",
        "credits_needed": None, "courses_needed": None, "group_name": None,
        "notes": "Shared BMus foundation: theory, musicianship, keyboard proficiency, music history, practical lessons (Years 1–2), and professional development.",
        "sort_order": 1,
        "courses": BMUS_CORE,
      },
      {
        "block_key": "early_music_voice_upper",
        "title": "Upper-Year Practical Instruction & Exams (Years 3–4)",
        "block_type": "required",
        "credits_needed": None, "courses_needed": None, "group_name": None,
        "notes": "Private voice lessons on historical repertoire (MUIN 380/381/480/481) plus three required jury/performance examinations (MUIN 282/382/482).",
        "sort_order": 2,
        "courses": UPPER_LESSONS,
      },
      {
        "block_key": "early_music_voice_specific",
        "title": "Early Music Voice Required Courses",
        "block_type": "required",
        "credits_needed": None, "courses_needed": None, "group_name": None,
        "notes": (
          "Voice-specific required courses: voice coaching (Years 2–4), lyric diction in four "
          "languages, Theory and Analysis 5, Topics in Early Music Analysis, and Topics in "
          "Performance Practice. Source: mcgill.ca/music/programs/bmus/early-music-voice/requirements"
        ),
        "sort_order": 3,
        "courses": [
          # Voice coaching – required for early music voice (Years 2 and 3)
          {"subject": "MUIN", "catalog": "300", "title": "Voice Coaching 1",                    "credits": 2, "is_required": True,  "recommended": True,  "recommendation_reason": "Voice coaching in historical vocal styles; Year 2"},
          {"subject": "MUIN", "catalog": "301", "title": "Voice Coaching 2",                    "credits": 2, "is_required": True,  "recommended": True,  "recommendation_reason": "Continuation of voice coaching; Year 3"},
          # Lyric diction (MUPG prefix) – all five are required
          {"subject": "MUPG", "catalog": "209", "title": "Introduction to Lyric Diction",       "credits": 1, "is_required": True,  "recommended": True,  "recommendation_reason": "Foundational IPA and lyric diction survey; Year 1 or 2"},
          {"subject": "MUPG", "catalog": "210", "title": "Italian Diction",                     "credits": 2, "is_required": True,  "recommended": True,  "recommendation_reason": "Italian lyric diction; essential for Italian early and baroque repertoire"},
          {"subject": "MUPG", "catalog": "211", "title": "French Diction",                      "credits": 2, "is_required": True,  "recommended": True,  "recommendation_reason": "French lyric diction; required for French baroque and mélodie repertoire"},
          {"subject": "MUPG", "catalog": "212", "title": "English Diction",                     "credits": 2, "is_required": True,  "recommended": True,  "recommendation_reason": "English lyric diction; required for English song and lute-song repertoire"},
          {"subject": "MUPG", "catalog": "213", "title": "German Diction",                      "credits": 2, "is_required": True,  "recommended": True,  "recommendation_reason": "German lyric diction; required for Lied and German baroque repertoire"},
          # Theory
          {"subject": "MUTH", "catalog": "350", "title": "Theory and Analysis 5",               "credits": 3, "is_required": True,  "recommended": True,  "recommendation_reason": "Post-tonal theory and analysis; required for Early Music Voice program"},
          {"subject": "MUTH", "catalog": "426", "title": "Topics in Early Music Analysis",      "credits": 3, "is_required": True,  "recommended": True,  "recommendation_reason": "Analysis of medieval, Renaissance, and baroque repertoire using period-appropriate methods"},
          # Performance practice
          {"subject": "MUPP", "catalog": "381", "title": "Topics in Performance Practice",      "credits": 3, "is_required": True,  "recommended": True,  "recommendation_reason": "Historical performance practice: tuning, ornamentation, rhetoric; required"},
        ],
      },
      {
        "block_key": "early_music_voice_complementary_musicianship",
        "title": "Complementary Musicianship (choose 2 credits)",
        "block_type": "choose_credits",
        "credits_needed": 2,
        "courses_needed": None, "group_name": None,
        "notes": "2 credits from approved MUSP musicianship courses; MUSP 354 and MUSP 381 are highly recommended for early music vocalists.",
        "sort_order": 4,
        "courses": [
          {"subject": "MUSP", "catalog": "354", "title": "Introduction to Improvisation and Ornamentation", "credits": 2, "is_required": False, "recommended": True,  "choose_from_group": "em_voice_musp", "choose_n_credits": 2, "recommendation_reason": "Historical improvisation and ornamentation; strongly recommended for early music vocalists"},
          {"subject": "MUSP", "catalog": "381", "title": "Singing Renaissance Notation",                    "credits": 2, "is_required": False, "recommended": True,  "choose_from_group": "em_voice_musp", "choose_n_credits": 2, "recommendation_reason": "Reading mensural notation; essential for performing Renaissance vocal repertoire"},
          {"subject": "MUSP", "catalog": "353", "title": "Musicianship for Voice",                          "credits": 2, "is_required": False, "recommended": False, "choose_from_group": "em_voice_musp", "choose_n_credits": 2},
          {"subject": "MUSP", "catalog": "346", "title": "Post-Tonal Musicianship",                         "credits": 2, "is_required": False, "recommended": False, "choose_from_group": "em_voice_musp", "choose_n_credits": 2},
          {"subject": "MUSP", "catalog": "361", "title": "Topics in Musicianship",                          "credits": 2, "is_required": False, "recommended": False, "choose_from_group": "em_voice_musp", "choose_n_credits": 2},
        ],
      },
      {
        "block_key": "early_music_voice_ensembles",
        "title": "Performance Ensembles (choose 10 credits)",
        "block_type": "choose_credits",
        "credits_needed": 10,
        "courses_needed": None, "group_name": None,
        "notes": "10 credits from approved MUEN ensembles. Voice students in Early Music primarily participate in Cappella Antica (MUEN 572) and Early Music Ensemble (MUEN 580).",
        "sort_order": 5,
        "courses": [
          {"subject": "MUEN", "catalog": "572", "title": "Cappella Antica",              "credits": 2, "is_required": False, "recommended": True,  "choose_from_group": "em_voice_ensembles", "choose_n_credits": 10, "recommendation_reason": "Primary choral ensemble for early music voice students"},
          {"subject": "MUEN", "catalog": "580", "title": "Early Music Ensemble",         "credits": 1, "is_required": False, "recommended": True,  "choose_from_group": "em_voice_ensembles", "choose_n_credits": 10, "recommendation_reason": "Small ensemble for early music vocalists"},
          {"subject": "MUEN", "catalog": "553", "title": "Vocal Chamber Ensemble",       "credits": 1, "is_required": False, "recommended": True,  "choose_from_group": "em_voice_ensembles", "choose_n_credits": 10, "recommendation_reason": "Chamber ensemble for voice students"},
          {"subject": "MUEN", "catalog": "578", "title": "Song Interpretation 1",        "credits": 1, "is_required": False, "recommended": True,  "choose_from_group": "em_voice_ensembles", "choose_n_credits": 10, "recommendation_reason": "Song interpretation masterclass/ensemble"},
          {"subject": "MUEN", "catalog": "579", "title": "Song Interpretation 2",        "credits": 1, "is_required": False, "recommended": False, "choose_from_group": "em_voice_ensembles", "choose_n_credits": 10},
          {"subject": "MUEN", "catalog": "454", "title": "Introductory Opera Repertoire Experience", "credits": 2, "is_required": False, "recommended": False, "choose_from_group": "em_voice_ensembles", "choose_n_credits": 10},
          {"subject": "MUEN", "catalog": "496", "title": "Opera Studio",                 "credits": 2, "is_required": False, "recommended": False, "choose_from_group": "em_voice_ensembles", "choose_n_credits": 10},
          {"subject": "MUEN", "catalog": "587", "title": "Cappella McGill",              "credits": 2, "is_required": False, "recommended": False, "choose_from_group": "em_voice_ensembles", "choose_n_credits": 10},
          {"subject": "MUEN", "catalog": "593", "title": "Choral Ensembles",             "credits": 2, "is_required": False, "recommended": False, "choose_from_group": "em_voice_ensembles", "choose_n_credits": 10},
        ],
      },
      {
        "block_key": "early_music_voice_history",
        "title": "Complementary Music History (choose 3 credits)",
        "block_type": "choose_credits",
        "credits_needed": 3,
        "courses_needed": None, "group_name": None,
        "notes": "3 credits from MUHL courses at 300-level or above, or MUHL 591D1/D2 Paleography.",
        "sort_order": 6,
        "courses": [
          {"subject": "MUHL", "catalog": "377", "title": "Baroque Opera",         "credits": 3, "is_required": False, "recommended": True,  "choose_from_group": "em_voice_history", "choose_n_credits": 3, "recommendation_reason": "Directly relevant for early music vocalists"},
          {"subject": "MUHL", "catalog": "380", "title": "Medieval Music",        "credits": 3, "is_required": False, "recommended": True,  "choose_from_group": "em_voice_history", "choose_n_credits": 3, "recommendation_reason": "Context for early vocal repertoire"},
          {"subject": "MUHL", "catalog": "381", "title": "Renaissance Music",     "credits": 3, "is_required": False, "recommended": True,  "choose_from_group": "em_voice_history", "choose_n_credits": 3, "recommendation_reason": "Core historical context for early music vocalists"},
          {"subject": "MUHL", "catalog": "382", "title": "Baroque Music",         "credits": 3, "is_required": False, "recommended": True,  "choose_from_group": "em_voice_history", "choose_n_credits": 3, "recommendation_reason": "Core historical context for baroque vocal performance"},
          {"subject": "MUHL", "catalog": "383", "title": "Classical Music",       "credits": 3, "is_required": False, "recommended": False, "choose_from_group": "em_voice_history", "choose_n_credits": 3},
          {"subject": "MUHL", "catalog": "591D1","title": "Paleography (Part 1)", "credits": 1.5,"is_required": False,"recommended": False, "choose_from_group": "em_voice_history", "choose_n_credits": 3},
          {"subject": "MUHL", "catalog": "591D2","title": "Paleography (Part 2)", "credits": 1.5,"is_required": False,"recommended": False, "choose_from_group": "em_voice_history", "choose_n_credits": 3},
        ],
      },
    ],
  },

  # ══════════════════════════════════════════════════════════════════════════
  #  7. COMPOSITION MAJOR – B.MUS. (124 credits)
  # ══════════════════════════════════════════════════════════════════════════
  {
    "program_key":   "composition_major_bmus",
    "name":          "Music Composition – B.Mus. (Major) (124 credits)",
    "program_type":  "major",
    "faculty":       "Schulich School of Music",
    "total_credits": 124,
    "description": (
      "The B.Mus. in Composition provides a solid grounding in classical music composition "
      "through lecture courses and private tutorials (Years 3–4). The program integrates "
      "music theory, music history, instrumentation, orchestration, and elective composition "
      "with electronic/computer music. Students must achieve a minimum grade of B- in all "
      "MUCO-prefix courses. Free electives allow pursuit of a minor or double major."
    ),
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/music/programs/music-research/composition-major-bmus/",
    "blocks": [
      {
        "block_key": "comp_core",
        "title": "Core Music Requirements (all B.Mus. programs)",
        "block_type": "required",
        "credits_needed": None, "courses_needed": None, "group_name": None,
        "notes": None,
        "sort_order": 1,
        "courses": BMUS_CORE + [MUTH_350],
      },
      {
        "block_key": "comp_required",
        "title": "Required Composition Courses",
        "block_type": "required",
        "credits_needed": 39, "courses_needed": None, "group_name": None,
        "notes": "All MUCO courses require minimum grade of B- to continue in the program.",
        "sort_order": 2,
        "courses": [
          {"subject": "MUCO", "catalog": "241",   "title": "Tonal Composition 1A",       "credits": 3, "is_required": True, "recommended": True, "recommendation_reason": "Tonal composition fundamentals; Year 2 Fall"},
          {"subject": "MUCO", "catalog": "242",   "title": "Tonal Composition 1B",       "credits": 3, "is_required": True, "recommended": True, "recommendation_reason": "Continuation; Year 2 Winter"},
          {"subject": "MUCO", "catalog": "245",   "title": "Composition 1A",             "credits": 2, "is_required": True, "recommended": True, "recommendation_reason": "Private composition tutorial; Year 2 Fall"},
          {"subject": "MUCO", "catalog": "246",   "title": "Composition 1B",             "credits": 3, "is_required": True, "recommended": True, "recommendation_reason": "Continuation; Year 2 Winter"},
          {"subject": "MUCO", "catalog": "261",   "title": "Orchestration 1",            "credits": 3, "is_required": True, "recommended": True, "recommendation_reason": "Writing for orchestral sections; Year 2–3"},
          {"subject": "MUCO", "catalog": "340D1", "title": "Composition 2 (Part 1)",     "credits": 2, "is_required": True, "recommended": True, "recommendation_reason": "Year 3 private composition tutorial Part 1"},
          {"subject": "MUCO", "catalog": "340D2", "title": "Composition 2 (Part 2)",     "credits": 2, "is_required": True, "recommended": True, "recommendation_reason": "Continuation; Year 3 Part 2"},
          {"subject": "MUCO", "catalog": "341",   "title": "Digital Studio 1",           "credits": 3, "is_required": True, "recommended": True, "recommendation_reason": "Electronic and computer music composition; Year 3"},
          {"subject": "MUCO", "catalog": "342",   "title": "Digital Studio 2",           "credits": 3, "is_required": True, "recommended": True, "recommendation_reason": "Advanced digital studio; Year 3–4"},
          {"subject": "MUCO", "catalog": "360",   "title": "Orchestration 2",            "credits": 3, "is_required": True, "recommended": True, "recommendation_reason": "Advanced orchestration; Year 3"},
          {"subject": "MUCO", "catalog": "440D1", "title": "Composition 3 (Part 1)",     "credits": 2, "is_required": True, "recommended": True, "recommendation_reason": "Year 4 advanced composition tutorial Part 1"},
          {"subject": "MUCO", "catalog": "440D2", "title": "Composition 3 (Part 2)",     "credits": 2, "is_required": True, "recommended": True, "recommendation_reason": "Continuation; Year 4 Part 2"},
          {"subject": "MUCO", "catalog": "460",   "title": "Orchestration 3",            "credits": 2, "is_required": True, "recommended": True, "recommendation_reason": "Advanced orchestration; Year 4"},
          {"subject": "MUCO", "catalog": "541",   "title": "Advanced Digital Studio",    "credits": 3, "is_required": True, "recommended": True, "recommendation_reason": "Senior digital studio; Year 4"},
          {"subject": "MUCO", "catalog": "575",   "title": "Topics in Composition",      "credits": 3, "is_required": True, "recommended": True, "recommendation_reason": "Advanced seminar on special composition topics; Year 4"},
        ],
      },
      {
        "block_key": "comp_ensembles",
        "title": "Ensembles",
        "block_type": "required",
        "credits_needed": 4,
        "courses_needed": None, "group_name": None,
        "notes": "4 credits of ensemble courses (MUEN prefix). Composition students may choose any ensemble.",
        "sort_order": 3,
        "courses": [
          {"subject": "MUEN", "catalog": "597", "title": "McGill Symphony Orchestra",    "credits": 2, "is_required": False, "recommended": True, "choose_from_group": "ensembles", "recommendation_reason": "Provides orchestral listening experience for composers"},
          {"subject": "MUEN", "catalog": "591", "title": "Contemporary Music Ensemble",  "credits": 1, "is_required": False, "recommended": True, "choose_from_group": "ensembles", "recommendation_reason": "Ideal for new-music composers"},
          {"subject": "MUEN", "catalog": "590", "title": "McGill Wind Orchestra",        "credits": 2, "is_required": False, "recommended": False, "choose_from_group": "ensembles"},
        ],
      },
      {
        "block_key": "comp_history_electives",
        "title": "Music History Electives",
        "block_type": "choose_credits",
        "credits_needed": 6,
        "courses_needed": None, "group_name": None,
        "notes": "6 credits from MUHL or MUPP at 300-level or above.",
        "sort_order": 4,
        "courses": [
          {"subject": "MUHL", "catalog": "370", "title": "Early 20th-Century Music",    "credits": 3, "is_required": False, "recommended": True, "choose_from_group": "music_history_300", "choose_n_credits": 6, "recommendation_reason": "Modern compositional styles"},
          {"subject": "MUHL", "catalog": "371", "title": "Music since 1945",             "credits": 3, "is_required": False, "recommended": True, "choose_from_group": "music_history_300", "choose_n_credits": 6, "recommendation_reason": "Contemporary compositional techniques"},
          {"subject": "MUHL", "catalog": "380", "title": "Medieval Music",               "credits": 3, "is_required": False, "recommended": False,"choose_from_group": "music_history_300", "choose_n_credits": 6},
          {"subject": "MUHL", "catalog": "382", "title": "Baroque Music",                "credits": 3, "is_required": False, "recommended": False,"choose_from_group": "music_history_300", "choose_n_credits": 6},
        ],
      },
    ],
  },

  # ══════════════════════════════════════════════════════════════════════════
  #  8. MUSIC HISTORY MAJOR – B.MUS. (124 credits)
  # ══════════════════════════════════════════════════════════════════════════
  {
    "program_key":   "music_history_major_bmus",
    "name":          "Music History – B.Mus. (Major) (124 credits)",
    "program_type":  "major",
    "faculty":       "Schulich School of Music",
    "total_credits": 124,
    "description": (
      "The B.Mus. in Music History challenges students to think critically about music "
      "across cultural contexts, social conditions, performance practice, and music as "
      "a vehicle of meaning and identity. Coursework spans medieval to contemporary music "
      "including jazz and popular idioms. The program provides preparation for graduate "
      "study in musicology and for professional careers in journalism, information sciences, "
      "arts administration, and teaching."
    ),
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/music/programs/music-research/music-history-major-bmus/",
    "blocks": [
      {
        "block_key": "hist_core",
        "title": "Core Music Requirements (all B.Mus. programs)",
        "block_type": "required",
        "credits_needed": None, "courses_needed": None, "group_name": None,
        "notes": "Music History majors also complete MUTH 350 Theory and Analysis 5.",
        "sort_order": 1,
        "courses": BMUS_CORE + [MUTH_350],
      },
      {
        "block_key": "hist_required_groups",
        "title": "History Requirements – Groups I, II, III (27 credits)",
        "block_type": "choose_credits",
        "credits_needed": 27,
        "courses_needed": None, "group_name": None,
        "notes": "27 credits from three groups, minimum 6 credits from each group. Group I: pre-1750; Group II: 1750–1900; Group III: 1900–present.",
        "sort_order": 2,
        "courses": [
          # Group I – Pre-1750
          {"subject": "MUHL", "catalog": "377",  "title": "Baroque Opera",            "credits": 3, "is_required": False, "recommended": True,  "choose_from_group": "hist_group_I",   "choose_n_credits": 6, "recommendation_reason": "Group I – pre-1750 repertoire"},
          {"subject": "MUHL", "catalog": "380",  "title": "Medieval Music",            "credits": 3, "is_required": False, "recommended": True,  "choose_from_group": "hist_group_I",   "choose_n_credits": 6},
          {"subject": "MUHL", "catalog": "381",  "title": "Renaissance Music",         "credits": 3, "is_required": False, "recommended": True,  "choose_from_group": "hist_group_I",   "choose_n_credits": 6},
          {"subject": "MUHL", "catalog": "382",  "title": "Baroque Music",             "credits": 3, "is_required": False, "recommended": True,  "choose_from_group": "hist_group_I",   "choose_n_credits": 6},
          {"subject": "MUHL", "catalog": "591D1","title": "Paleography",               "credits": 1.5,"is_required": False,"recommended": False, "choose_from_group": "hist_group_I",   "choose_n_credits": 6},
          {"subject": "MUHL", "catalog": "591D2","title": "Paleography",               "credits": 1.5,"is_required": False,"recommended": False, "choose_from_group": "hist_group_I",   "choose_n_credits": 6},
          # Group II – 1750–1900
          {"subject": "MUHL", "catalog": "383",  "title": "Classical Music",           "credits": 3, "is_required": False, "recommended": True,  "choose_from_group": "hist_group_II",  "choose_n_credits": 6},
          {"subject": "MUHL", "catalog": "366",  "title": "Era of the Fortepiano",     "credits": 3, "is_required": False, "recommended": True,  "choose_from_group": "hist_group_II",  "choose_n_credits": 6},
          {"subject": "MUHL", "catalog": "365",  "title": "Opera after 1900",          "credits": 3, "is_required": False, "recommended": False, "choose_from_group": "hist_group_II",  "choose_n_credits": 6},
          # Group III – 1900–present
          {"subject": "MUHL", "catalog": "370",  "title": "Early 20th-Century Music",  "credits": 3, "is_required": False, "recommended": True,  "choose_from_group": "hist_group_III", "choose_n_credits": 6},
          {"subject": "MUHL", "catalog": "371",  "title": "Music since 1945",           "credits": 3, "is_required": False, "recommended": True,  "choose_from_group": "hist_group_III", "choose_n_credits": 6},
          {"subject": "MUHL", "catalog": "386",  "title": "History of Jazz",            "credits": 3, "is_required": False, "recommended": True,  "choose_from_group": "hist_group_III", "choose_n_credits": 6},
          {"subject": "MUHL", "catalog": "388",  "title": "Popular Music",              "credits": 3, "is_required": False, "recommended": False, "choose_from_group": "hist_group_III", "choose_n_credits": 6},
          {"subject": "MUHL", "catalog": "375",  "title": "Canadian Music",             "credits": 3, "is_required": False, "recommended": False, "choose_from_group": "hist_group_III", "choose_n_credits": 6},
        ],
      },
      {
        "block_key": "hist_ensembles",
        "title": "Ensembles",
        "block_type": "required",
        "credits_needed": 4,
        "courses_needed": None, "group_name": None,
        "notes": "4 credits of MUEN ensembles across the program.",
        "sort_order": 3,
        "courses": [
          {"subject": "MUEN", "catalog": "597", "title": "McGill Symphony Orchestra", "credits": 2, "is_required": False, "recommended": True,  "choose_from_group": "ensembles"},
          {"subject": "MUEN", "catalog": "593", "title": "Choral Ensembles",          "credits": 2, "is_required": False, "recommended": False, "choose_from_group": "ensembles"},
          {"subject": "MUEN", "catalog": "591", "title": "Contemporary Music Ensemble","credits": 1, "is_required": False, "recommended": False, "choose_from_group": "ensembles"},
        ],
      },
    ],
  },

  # ══════════════════════════════════════════════════════════════════════════
  #  9. MUSIC THEORY MAJOR – B.MUS. (124 credits)
  # ══════════════════════════════════════════════════════════════════════════
  {
    "program_key":   "music_theory_major_bmus",
    "name":          "Music Theory – B.Mus. (Major) (124 credits)",
    "program_type":  "major",
    "faculty":       "Schulich School of Music",
    "total_credits": 124,
    "description": (
      "The B.Mus. in Music Theory focuses on the in-depth study of tonal and post-tonal "
      "analytical methods, counterpoint, form, and music perception. The program develops "
      "advanced analytical skills applicable to performance, composition, and academic "
      "research. Students take upper-level MUTH courses in Schenkerian analysis, post-tonal "
      "theory, and music cognition."
    ),
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/music/programs/music-research/music-theory-major-bmus/",
    "blocks": [
      {
        "block_key": "theory_core",
        "title": "Core Music Requirements (all B.Mus. programs)",
        "block_type": "required",
        "credits_needed": None, "courses_needed": None, "group_name": None,
        "notes": None,
        "sort_order": 1,
        "courses": BMUS_CORE + [MUTH_350],
      },
      {
        "block_key": "theory_upper",
        "title": "Upper-Level Theory Complementary Courses (40 credits)",
        "block_type": "choose_credits",
        "credits_needed": 40,
        "courses_needed": None, "group_name": None,
        "notes": (
          "40 complementary credits of advanced theory from four sub-groups: "
          "(1) Counterpoint – 6 credits: one pair from MUTH 202+302 (modal) or MUTH 204+304 (tonal); "
          "(2) Advanced Analysis – 6 credits: two courses from MUTH 321/322/426/541; "
          "(3) Methods and Special Topics – 6 credits: two courses from MUTH 526/528/529/538; "
          "(4) Additional Theory/History Electives – 22 credits. "
          "MUSP 346 Post-Tonal Musicianship (2 credits) is required within the core required section. "
          "Minimum grade of B- in all MUTH-prefix courses."
        ),
        "sort_order": 2,
        "courses": [
          # Counterpoint (choose one pair)
          {"subject": "MUTH", "catalog": "202", "title": "Modal Counterpoint 1",              "credits": 3, "is_required": False, "recommended": True,  "choose_from_group": "theory_counterpoint", "choose_n_credits": 6, "recommendation_reason": "Renaissance modal counterpoint; recommended pair with MUTH 302"},
          {"subject": "MUTH", "catalog": "302", "title": "Modal Counterpoint 2",              "credits": 3, "is_required": False, "recommended": True,  "choose_from_group": "theory_counterpoint", "choose_n_credits": 6},
          {"subject": "MUTH", "catalog": "204", "title": "Tonal Counterpoint 1",              "credits": 3, "is_required": False, "recommended": False, "choose_from_group": "theory_counterpoint", "choose_n_credits": 6, "recommendation_reason": "18th-century tonal counterpoint; pair with MUTH 304"},
          {"subject": "MUTH", "catalog": "304", "title": "Tonal Counterpoint 2",              "credits": 3, "is_required": False, "recommended": False, "choose_from_group": "theory_counterpoint", "choose_n_credits": 6},
          # Advanced Analysis (choose two)
          {"subject": "MUTH", "catalog": "321", "title": "Topics in Tonal Analysis",          "credits": 3, "is_required": False, "recommended": True,  "choose_from_group": "theory_analysis", "choose_n_credits": 6, "recommendation_reason": "Advanced tonal analytical methods"},
          {"subject": "MUTH", "catalog": "322", "title": "Topics in Post-Tonal Analysis",     "credits": 3, "is_required": False, "recommended": True,  "choose_from_group": "theory_analysis", "choose_n_credits": 6, "recommendation_reason": "Set theory, twelve-tone, spectral analysis"},
          {"subject": "MUTH", "catalog": "426", "title": "Topics in Early Music Analysis",    "credits": 3, "is_required": False, "recommended": False, "choose_from_group": "theory_analysis", "choose_n_credits": 6},
          {"subject": "MUTH", "catalog": "541", "title": "Topics in Popular Music Analysis",  "credits": 3, "is_required": False, "recommended": False, "choose_from_group": "theory_analysis", "choose_n_credits": 6},
          # Methods & Special Topics (choose two)
          {"subject": "MUTH", "catalog": "526", "title": "Methods in Tonal Theory and Analysis","credits": 3, "is_required": False, "recommended": True, "choose_from_group": "theory_methods", "choose_n_credits": 6, "recommendation_reason": "Advanced analytical methodologies for tonal music"},
          {"subject": "MUTH", "catalog": "528", "title": "Schenkerian Theory and Analysis",   "credits": 3, "is_required": False, "recommended": True,  "choose_from_group": "theory_methods", "choose_n_credits": 6, "recommendation_reason": "Schenkerian voice-leading analysis; core upper-level theory method"},
          {"subject": "MUTH", "catalog": "529", "title": "Proseminar in Music Theory",        "credits": 3, "is_required": False, "recommended": True,  "choose_from_group": "theory_methods", "choose_n_credits": 6, "recommendation_reason": "Research methods and writing in music theory"},
          {"subject": "MUTH", "catalog": "538", "title": "Mathematical Models for Musical Analysis","credits": 3,"is_required": False,"recommended": False,"choose_from_group": "theory_methods","choose_n_credits": 6},
          # Additional electives
          {"subject": "MUCO", "catalog": "575", "title": "Topics in Composition",            "credits": 3, "is_required": False, "recommended": False, "choose_from_group": "theory_additional_electives"},
          {"subject": "MUTH", "catalog": "539", "title": "Topics in Advanced Writing Techniques","credits": 3,"is_required": False,"recommended": True,"choose_from_group": "theory_additional_electives","recommendation_reason": "Advanced academic writing in music theory"},
          {"subject": "MUSP", "catalog": "346", "title": "Post-Tonal Musicianship",          "credits": 2, "is_required": True, "recommended": True, "recommendation_reason": "Required: ear-training in post-tonal idioms; 2 credits within the required musicianship section"},
        ],
      },
      {
        "block_key": "theory_history",
        "title": "Music History (upper-level)",
        "block_type": "choose_credits",
        "credits_needed": 6,
        "courses_needed": None, "group_name": None,
        "notes": "6 credits from MUHL or MUPP at 300-level or above.",
        "sort_order": 3,
        "courses": [
          {"subject": "MUHL", "catalog": "370", "title": "Early 20th-Century Music", "credits": 3, "is_required": False, "recommended": True, "choose_from_group": "music_history_300", "choose_n_credits": 6},
          {"subject": "MUHL", "catalog": "371", "title": "Music since 1945",          "credits": 3, "is_required": False, "recommended": True, "choose_from_group": "music_history_300", "choose_n_credits": 6},
          {"subject": "MUHL", "catalog": "382", "title": "Baroque Music",             "credits": 3, "is_required": False, "recommended": False,"choose_from_group": "music_history_300", "choose_n_credits": 6},
          {"subject": "MUHL", "catalog": "383", "title": "Classical Music",           "credits": 3, "is_required": False, "recommended": False,"choose_from_group": "music_history_300", "choose_n_credits": 6},
        ],
      },
      {
        "block_key": "theory_ensembles",
        "title": "Ensembles",
        "block_type": "required",
        "credits_needed": 4,
        "courses_needed": None, "group_name": None,
        "notes": "4 credits of MUEN ensembles.",
        "sort_order": 4,
        "courses": [
          {"subject": "MUEN", "catalog": "597", "title": "McGill Symphony Orchestra",    "credits": 2, "is_required": False, "recommended": True, "choose_from_group": "ensembles"},
          {"subject": "MUEN", "catalog": "591", "title": "Contemporary Music Ensemble",  "credits": 1, "is_required": False, "recommended": True, "choose_from_group": "ensembles"},
          {"subject": "MUEN", "catalog": "593", "title": "Choral Ensembles",             "credits": 2, "is_required": False, "recommended": False,"choose_from_group": "ensembles"},
        ],
      },
    ],
  },

  # ══════════════════════════════════════════════════════════════════════════
  # 10. MUSIC STUDIES MAJOR – B.MUS. (123 credits) [Fall 2025+]
  # ══════════════════════════════════════════════════════════════════════════
  {
    "program_key":   "music_studies_major_bmus",
    "name":          "Music Studies – B.Mus. (Major) (123 credits)",
    "program_type":  "major",
    "faculty":       "Schulich School of Music",
    "total_credits": 123,
    "description": (
      "The B.Mus. in Music Studies (for students admitted Fall 2025 or later) is a dynamic, "
      "flexible curriculum for students who want to explore the many evolving career paths "
      "in music including arts administration, performance sciences, music technology, "
      "education, librarianship, and research. The program combines core music areas "
      "(theory, history, musicianship, professional development) with elective specialization "
      "tracks in Composition, Ensembles, Music History, Music Theory, Music Education, "
      "Music Technology, Music Entrepreneurship, or Performance."
    ),
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/music/programs/music-research/major-music-studies-bmus/",
    "blocks": [
      {
        "block_key": "music_studies_core",
        "title": "Core Music Requirements (all B.Mus. programs)",
        "block_type": "required",
        "credits_needed": None, "courses_needed": None, "group_name": None,
        "notes": "Shared foundation common to all BMus programs.",
        "sort_order": 1,
        "courses": BMUS_CORE,
      },
      {
        "block_key": "music_studies_pd",
        "title": "Professional Development",
        "block_type": "required",
        "credits_needed": None, "courses_needed": None, "group_name": None,
        "notes": None,
        "sort_order": 2,
        "courses": [
          {"subject": "MUPD", "catalog": "245", "title": "Exploring Interdisciplinary Music Studies 2", "credits": 2, "is_required": True, "recommended": True, "recommendation_reason": "Required professional development course for Music Studies major"},
          {"subject": "MUPD", "catalog": "350", "title": "Applied Projects for Musicians",             "credits": 3, "is_required": True, "recommended": True, "recommendation_reason": "Capstone applied project; Year 3 or 4"},
        ],
      },
      {
        "block_key": "music_studies_ensembles",
        "title": "Ensembles",
        "block_type": "required",
        "credits_needed": 6,
        "courses_needed": None, "group_name": None,
        "notes": "6 credits from MUEN-prefix ensemble courses.",
        "sort_order": 3,
        "courses": [
          {"subject": "MUEN", "catalog": "563", "title": "Jazz Vocal Workshop",           "credits": 1, "is_required": False, "recommended": False, "choose_from_group": "ensembles"},
          {"subject": "MUEN", "catalog": "584", "title": "Cappella Antica",               "credits": 1, "is_required": False, "recommended": False, "choose_from_group": "ensembles"},
          {"subject": "MUEN", "catalog": "585", "title": "Baroque Orchestra",             "credits": 1, "is_required": False, "recommended": False, "choose_from_group": "ensembles"},
          {"subject": "MUEN", "catalog": "586", "title": "Cappella McGill",               "credits": 1, "is_required": False, "recommended": False, "choose_from_group": "ensembles"},
          {"subject": "MUEN", "catalog": "590", "title": "McGill Wind Orchestra",         "credits": 2, "is_required": False, "recommended": True,  "choose_from_group": "ensembles"},
          {"subject": "MUEN", "catalog": "593", "title": "Choral Ensembles",              "credits": 2, "is_required": False, "recommended": True,  "choose_from_group": "ensembles"},
          {"subject": "MUEN", "catalog": "595", "title": "Jazz Ensembles",                "credits": 1, "is_required": False, "recommended": False, "choose_from_group": "ensembles"},
          {"subject": "MUEN", "catalog": "597", "title": "McGill Symphony Orchestra",     "credits": 2, "is_required": False, "recommended": True,  "choose_from_group": "ensembles"},
        ],
      },
      {
        "block_key": "music_studies_history",
        "title": "Music History (upper-level, 9 credits)",
        "block_type": "choose_credits",
        "credits_needed": 9,
        "courses_needed": None, "group_name": None,
        "notes": "9 credits from MUHL or MUPP at 300-level or above.",
        "sort_order": 4,
        "courses": [
          {"subject": "MUHL", "catalog": "370", "title": "Early 20th-Century Music",    "credits": 3, "is_required": False, "recommended": False, "choose_from_group": "music_history_300", "choose_n_credits": 9},
          {"subject": "MUHL", "catalog": "371", "title": "Music since 1945",             "credits": 3, "is_required": False, "recommended": False, "choose_from_group": "music_history_300", "choose_n_credits": 9},
          {"subject": "MUHL", "catalog": "375", "title": "Canadian Music",               "credits": 3, "is_required": False, "recommended": False, "choose_from_group": "music_history_300", "choose_n_credits": 9},
          {"subject": "MUHL", "catalog": "380", "title": "Medieval Music",               "credits": 3, "is_required": False, "recommended": False, "choose_from_group": "music_history_300", "choose_n_credits": 9},
          {"subject": "MUHL", "catalog": "381", "title": "Renaissance Music",            "credits": 3, "is_required": False, "recommended": False, "choose_from_group": "music_history_300", "choose_n_credits": 9},
          {"subject": "MUHL", "catalog": "382", "title": "Baroque Music",                "credits": 3, "is_required": False, "recommended": False, "choose_from_group": "music_history_300", "choose_n_credits": 9},
          {"subject": "MUHL", "catalog": "383", "title": "Classical Music",              "credits": 3, "is_required": False, "recommended": False, "choose_from_group": "music_history_300", "choose_n_credits": 9},
          {"subject": "MUHL", "catalog": "386", "title": "History of Jazz",              "credits": 3, "is_required": False, "recommended": False, "choose_from_group": "music_history_300", "choose_n_credits": 9},
          {"subject": "MUPP", "catalog": "381", "title": "Topics in Performance Practice","credits": 3, "is_required": False, "recommended": False, "choose_from_group": "music_history_300", "choose_n_credits": 9},
        ],
      },
      {
        "block_key": "music_studies_specialization",
        "title": "Specialization Track (choose one, 9 credits each)",
        "block_type": "choose_credits",
        "credits_needed": 9,
        "courses_needed": None, "group_name": None,
        "notes": "Choose one of: Music History (MUHL/MUPP), Music Theory (MUTH), Composition (MUCO), Music Education (MUGT/MUCT/MUIT), Music Technology (MUMT/MUSR), Music Entrepreneurship (MUPD 200+), or Performance. Minimum 9 credits in chosen track.",
        "sort_order": 5,
        "courses": [
          # Sample courses from each track
          {"subject": "MUTH", "catalog": "350",  "title": "Theory and Analysis 5",              "credits": 3, "is_required": False, "recommended": True,  "choose_from_group": "specialization", "recommendation_reason": "Theory track"},
          {"subject": "MUTH", "catalog": "430",  "title": "Schenkerian Theory and Analysis",    "credits": 3, "is_required": False, "recommended": False, "choose_from_group": "specialization"},
          {"subject": "MUCO", "catalog": "230",  "title": "The Art of Composition",             "credits": 3, "is_required": False, "recommended": True,  "choose_from_group": "specialization", "recommendation_reason": "Composition track"},
          {"subject": "MUCO", "catalog": "260",  "title": "Instruments of the Orchestra",       "credits": 3, "is_required": False, "recommended": False, "choose_from_group": "specialization"},
          {"subject": "MUMT", "catalog": "216",  "title": "Introduction to Sound Recording",    "credits": 3, "is_required": False, "recommended": True,  "choose_from_group": "specialization", "recommendation_reason": "Technology track"},
          {"subject": "MUMT", "catalog": "307",  "title": "Music and the Brain",                "credits": 3, "is_required": False, "recommended": False, "choose_from_group": "specialization"},
          {"subject": "MUPD", "catalog": "240",  "title": "Music Entrepreneurship 1",           "credits": 2, "is_required": False, "recommended": False, "choose_from_group": "specialization", "recommendation_reason": "Entrepreneurship track"},
          {"subject": "MUPD", "catalog": "350",  "title": "Applied Projects for Musicians",     "credits": 3, "is_required": False, "recommended": False, "choose_from_group": "specialization"},
        ],
      },
    ],
  },

  # ══════════════════════════════════════════════════════════════════════════
  # 11. FACULTY PROGRAM – GENERAL B.MUS. (123 credits) [pre-2025 / still active]
  # ══════════════════════════════════════════════════════════════════════════
  {
    "program_key":   "faculty_program_bmus",
    "name":          "Faculty Program – B.Mus. (Major) (123 credits)",
    "program_type":  "major",
    "faculty":       "Schulich School of Music",
    "total_credits": 123,
    "description": (
      "The B.Mus. Faculty Program (for students admitted Fall 2024 or prior) accommodates "
      "students who are undecided about a specialization, interested in a pattern not covered "
      "by established majors, or who wish to combine music with other disciplines. Students "
      "design their own program in consultation with a staff adviser. Free electives allow "
      "pursuit of a minor, double major, or cross-faculty combination."
    ),
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/music/programs/music-research/faculty-program-bmus/",
    "blocks": [
      {
        "block_key": "faculty_prog_core",
        "title": "Core Music Requirements (all B.Mus. programs)",
        "block_type": "required",
        "credits_needed": None, "courses_needed": None, "group_name": None,
        "notes": "Faculty Program requires MUTH 350 Theory and Analysis 5 in addition to the shared BMus core. Source: mcgill.ca/music/programs/bmus/faculty-program/requirements",
        "sort_order": 1,
        "courses": BMUS_CORE + [MUTH_350],
      },
      {
        "block_key": "faculty_prog_upper_history",
        "title": "Upper-Level Music History (6 credits)",
        "block_type": "choose_credits",
        "credits_needed": 6,
        "courses_needed": None, "group_name": None,
        "notes": "6 credits from MUHL or MUPP at 300-level or above.",
        "sort_order": 2,
        "courses": [
          {"subject": "MUHL", "catalog": "380", "title": "Medieval Music",       "credits": 3, "is_required": False, "recommended": False, "choose_from_group": "music_history_300", "choose_n_credits": 6},
          {"subject": "MUHL", "catalog": "382", "title": "Baroque Music",        "credits": 3, "is_required": False, "recommended": False, "choose_from_group": "music_history_300", "choose_n_credits": 6},
          {"subject": "MUHL", "catalog": "383", "title": "Classical Music",      "credits": 3, "is_required": False, "recommended": False, "choose_from_group": "music_history_300", "choose_n_credits": 6},
          {"subject": "MUHL", "catalog": "386", "title": "History of Jazz",      "credits": 3, "is_required": False, "recommended": False, "choose_from_group": "music_history_300", "choose_n_credits": 6},
          {"subject": "MUHL", "catalog": "371", "title": "Music since 1945",     "credits": 3, "is_required": False, "recommended": False, "choose_from_group": "music_history_300", "choose_n_credits": 6},
        ],
      },
      {
        "block_key": "faculty_prog_ensembles",
        "title": "Ensembles",
        "block_type": "required",
        "credits_needed": 4,
        "courses_needed": None, "group_name": None,
        "notes": "4 credits of MUEN ensembles.",
        "sort_order": 3,
        "courses": [
          {"subject": "MUEN", "catalog": "597", "title": "McGill Symphony Orchestra", "credits": 2, "is_required": False, "recommended": True, "choose_from_group": "ensembles"},
          {"subject": "MUEN", "catalog": "593", "title": "Choral Ensembles",          "credits": 2, "is_required": False, "recommended": True, "choose_from_group": "ensembles"},
          {"subject": "MUEN", "catalog": "590", "title": "McGill Wind Orchestra",     "credits": 2, "is_required": False, "recommended": False,"choose_from_group": "ensembles"},
        ],
      },
    ],
  },

  # ══════════════════════════════════════════════════════════════════════════
  # 12. FACULTY PROGRAM – JAZZ B.MUS. (123 credits)
  # ══════════════════════════════════════════════════════════════════════════
  {
    "program_key":   "faculty_program_jazz_bmus",
    "name":          "Faculty Program – Jazz – B.Mus. (Major) (123 credits)",
    "program_type":  "major",
    "faculty":       "Schulich School of Music",
    "total_credits": 123,
    "description": (
      "The B.Mus. Faculty Program – Jazz allows jazz-oriented students to combine jazz "
      "performance and theory with broader interdisciplinary music studies. The program "
      "includes the jazz-specific core (MUJZ theory, history, ear training, keyboard, "
      "improvisation, and arranging), jazz ensembles, and free electives allowing exploration "
      "of additional music areas or other faculties."
    ),
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/music/programs/music-research/faculty-music-jazz-bmus/",
    "blocks": [
      {
        "block_key": "fac_jazz_core",
        "title": "Core & Jazz Theory Requirements",
        "block_type": "required",
        "credits_needed": None, "courses_needed": None, "group_name": None,
        "notes": "Jazz-specific substitutions: MUJZ 170/171 replaces MUSP 170/171; MUJZ 160/161 and 186 replace some MUTH/MUHL core courses.",
        "sort_order": 1,
        "courses": [
          {"subject": "MUPD", "catalog": "135",  "title": "Music as a Profession 1",    "credits": 1, "is_required": True, "recommended": True},
          {"subject": "MUPD", "catalog": "235",  "title": "Music as a Profession 2",    "credits": 1, "is_required": True, "recommended": True},
          {"subject": "MUIN", "catalog": "180",  "title": "BMus Practical Lessons 1",   "credits": 3, "is_required": True, "recommended": True},
          {"subject": "MUIN", "catalog": "181",  "title": "BMus Practical Lessons 2",   "credits": 3, "is_required": True, "recommended": True},
          {"subject": "MUIN", "catalog": "280",  "title": "BMus Practical Lessons 3",   "credits": 2.5,"is_required": True,"recommended": True},
          {"subject": "MUIN", "catalog": "281",  "title": "BMus Practical Lessons 4",   "credits": 2.5,"is_required": True,"recommended": True},
          {"subject": "MUIN", "catalog": "283",  "title": "BMus Concentration Final Exam","credits": 1,"is_required": True,"recommended": True},
          {"subject": "MUHL", "catalog": "286",  "title": "Critical Thinking About Music","credits": 3,"is_required": True,"recommended": True},
          {"subject": "MUJZ", "catalog": "160",  "title": "Jazz Materials 1",           "credits": 3, "is_required": True, "recommended": True, "recommendation_reason": "Jazz theory foundation Year 1"},
          {"subject": "MUJZ", "catalog": "161",  "title": "Jazz Materials 2",           "credits": 3, "is_required": True, "recommended": True},
          {"subject": "MUJZ", "catalog": "170",  "title": "Jazz Keyboard Proficiency 1","credits": 1, "is_required": True, "recommended": True},
          {"subject": "MUJZ", "catalog": "171",  "title": "Jazz Keyboard Proficiency 2","credits": 1, "is_required": True, "recommended": True},
          {"subject": "MUJZ", "catalog": "186",  "title": "Jazz History Survey",        "credits": 3, "is_required": True, "recommended": True},
          {"subject": "MUJZ", "catalog": "223",  "title": "Jazz Ear Training 1",        "credits": 2, "is_required": True, "recommended": True},
          {"subject": "MUJZ", "catalog": "224",  "title": "Jazz Ear Training 2",        "credits": 2, "is_required": True, "recommended": True},
          {"subject": "MUJZ", "catalog": "260",  "title": "Jazz Arranging 1",           "credits": 2, "is_required": True, "recommended": True},
          {"subject": "MUJZ", "catalog": "261",  "title": "Jazz Arranging 2",           "credits": 2, "is_required": True, "recommended": True},
        ],
      },
      {
        "block_key": "fac_jazz_history",
        "title": "Music History Electives",
        "block_type": "choose_credits",
        "credits_needed": 6,
        "courses_needed": None, "group_name": None,
        "notes": "6 credits from MUHL or MUPP at any level.",
        "sort_order": 2,
        "courses": [
          {"subject": "MUHL", "catalog": "386", "title": "History of Jazz",     "credits": 3, "is_required": False, "recommended": True,  "choose_from_group": "music_history_any", "choose_n_credits": 6},
          {"subject": "MUHL", "catalog": "388", "title": "Popular Music",       "credits": 3, "is_required": False, "recommended": False, "choose_from_group": "music_history_any", "choose_n_credits": 6},
          {"subject": "MUHL", "catalog": "286", "title": "Critical Thinking About Music", "credits": 3, "is_required": False, "recommended": False, "choose_from_group": "music_history_any", "choose_n_credits": 6},
        ],
      },
      {
        "block_key": "fac_jazz_ensembles",
        "title": "Jazz Ensembles",
        "block_type": "required",
        "credits_needed": 6,
        "courses_needed": None, "group_name": None,
        "notes": "6 credits: MUEN 570 Jazz Combo required across multiple semesters; additional MUEN credits from large jazz ensembles.",
        "sort_order": 3,
        "courses": [
          {"subject": "MUEN", "catalog": "570", "title": "Jazz Combo",          "credits": 1, "is_required": True,  "recommended": True, "recommendation_reason": "Required for multiple semesters"},
          {"subject": "MUEN", "catalog": "595", "title": "Jazz Ensembles",      "credits": 2, "is_required": False, "recommended": True, "choose_from_group": "ensembles"},
          {"subject": "MUEN", "catalog": "563", "title": "Jazz Vocal Workshop", "credits": 1, "is_required": False, "recommended": False,"choose_from_group": "ensembles"},
        ],
      },
    ],
  },

  # ══════════════════════════════════════════════════════════════════════════
  # 13. CONCURRENT B.MUS. / B.ED. – MUSIC EDUCATION (170 credits)
  # ══════════════════════════════════════════════════════════════════════════
  {
    "program_key":   "bmus_bed_music_education",
    "name":          "Concurrent B.Mus. / B.Ed. – Music Education (170 credits)",
    "program_type":  "major",
    "faculty":       "Schulich School of Music",
    "total_credits": 170,
    "description": (
      "The concurrent B.Mus./B.Ed. is a 5-year, 170-credit program jointly administered by "
      "the Schulich School of Music and the Faculty of Education. The B.Mus. component "
      "focuses on the development of prospective music educators as musicians, through core "
      "music history, theory, musicianship, performance courses, and instrumental/vocal/conducting "
      "techniques. The B.Ed. Music Elementary and Secondary component covers educational "
      "foundations, music pedagogy, and four field-experience practica. CEGEP graduates with "
      "advanced standing may complete the program in 4 years. Graduates are eligible for "
      "Quebec teacher certification."
    ),
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/music/programs/music-research/concurrent-bmus-bed/",
    "blocks": [
      {
        "block_key": "bmus_bed_music_core",
        "title": "B.Mus. Music Core Requirements",
        "block_type": "required",
        "credits_needed": None, "courses_needed": None, "group_name": None,
        "notes": "Same core as all B.Mus. programs.",
        "sort_order": 1,
        "courses": BMUS_CORE,
      },
      {
        "block_key": "bmus_bed_music_ed_courses",
        "title": "Music Education Courses (B.Mus. component)",
        "block_type": "required",
        "credits_needed": None, "courses_needed": None, "group_name": None,
        "notes": "Instrumental and vocal techniques, conducting, and music education laboratory courses required in the B.Mus. Music Education component.",
        "sort_order": 2,
        "courses": [
          {"subject": "MUCO", "catalog": "260",  "title": "Instruments of the Orchestra",       "credits": 3, "is_required": True, "recommended": True, "recommendation_reason": "Required for developing pedagogy of orchestral instruments"},
          {"subject": "MUCT", "catalog": "310",  "title": "Choral Conducting 1",                "credits": 2, "is_required": True, "recommended": True, "recommendation_reason": "Conducting fundamentals required for music educators"},
          {"subject": "MUGT", "catalog": "211",  "title": "Guitar Techniques",                  "credits": 2, "is_required": False,"recommended": True, "recommendation_reason": "Class guitar for music educators"},
          {"subject": "MUIT", "catalog": "200",  "title": "Brass Techniques",                   "credits": 2, "is_required": False,"recommended": True, "recommendation_reason": "Required instrument technique courses"},
          {"subject": "MUIT", "catalog": "201",  "title": "Woodwind Techniques",                "credits": 2, "is_required": False,"recommended": True},
          {"subject": "MUIT", "catalog": "202",  "title": "String Techniques",                  "credits": 2, "is_required": False,"recommended": True},
          {"subject": "MUIT", "catalog": "203",  "title": "Percussion Techniques",              "credits": 2, "is_required": False,"recommended": True},
          {"subject": "MUGT", "catalog": "320",  "title": "Group Voice for Music Educators",    "credits": 2, "is_required": True, "recommended": True, "recommendation_reason": "Vocal techniques for music educators"},
        ],
      },
      {
        "block_key": "bmus_bed_education",
        "title": "B.Ed. Education Component",
        "block_type": "required",
        "credits_needed": None, "courses_needed": None, "group_name": None,
        "notes": "Education courses from the Faculty of Education: foundations, pedagogy, and four field-experience practica. Refer to the Faculty of Education for full course listings.",
        "sort_order": 3,
        "courses": [
          {"subject": "EDEE", "catalog": "280",  "title": "Music Education: Elementary",           "credits": 3, "is_required": True, "recommended": True, "recommendation_reason": "Elementary music teaching methods"},
          {"subject": "EDEE", "catalog": "380",  "title": "Music Education: Secondary",            "credits": 3, "is_required": True, "recommended": True, "recommendation_reason": "Secondary music teaching methods"},
          {"subject": "EDEE", "catalog": "310",  "title": "Foundations of Education",              "credits": 3, "is_required": True, "recommended": True, "recommendation_reason": "Educational theory required in B.Ed. component"},
          {"subject": "EDEE", "catalog": "420",  "title": "Field Experience Practicum 1",          "credits": 3, "is_required": True, "recommended": True, "recommendation_reason": "First supervised teaching practicum"},
          {"subject": "EDEE", "catalog": "421",  "title": "Field Experience Practicum 2",          "credits": 6, "is_required": True, "recommended": True, "recommendation_reason": "Second supervised teaching practicum"},
          {"subject": "EDEE", "catalog": "422",  "title": "Field Experience Practicum 3",          "credits": 6, "is_required": True, "recommended": True, "recommendation_reason": "Third supervised teaching practicum"},
          {"subject": "EDEE", "catalog": "490",  "title": "Student Teaching",                      "credits": 9, "is_required": True, "recommended": True, "recommendation_reason": "Final full-time student teaching placement; Year 5"},
        ],
      },
      {
        "block_key": "bmus_bed_ensembles",
        "title": "Ensembles",
        "block_type": "required",
        "credits_needed": 6,
        "courses_needed": None, "group_name": None,
        "notes": "6 credits of MUEN ensembles across the program.",
        "sort_order": 4,
        "courses": [
          {"subject": "MUEN", "catalog": "597", "title": "McGill Symphony Orchestra", "credits": 2, "is_required": False, "recommended": True, "choose_from_group": "ensembles"},
          {"subject": "MUEN", "catalog": "593", "title": "Choral Ensembles",          "credits": 2, "is_required": False, "recommended": True, "choose_from_group": "ensembles"},
          {"subject": "MUEN", "catalog": "590", "title": "McGill Wind Orchestra",     "credits": 2, "is_required": False, "recommended": True, "choose_from_group": "ensembles"},
        ],
      },
    ],
  },

]  # end MUSIC_PROGRAMS


# ─────────────────────────────────────────────────────────────────────────────
#  DB helper functions (identical pattern to other faculty seeds)
# ─────────────────────────────────────────────────────────────────────────────

def _upsert_program(supabase, prog: dict) -> str:
    key = prog["program_key"]
    existing = (
        supabase.table("degree_programs")
        .select("id")
        .eq("program_key", key)
        .limit(1)
        .execute()
    )
    payload = {
        "program_key":   key,
        "name":          prog["name"],
        "program_type":  prog["program_type"],
        "faculty":       prog["faculty"],
        "total_credits": prog["total_credits"],
        "description":   prog.get("description", ""),
        "ecalendar_url": prog.get("ecalendar_url", ""),
    }
    if existing.data:
        prog_id = existing.data[0]["id"]
        supabase.table("degree_programs").update(payload).eq("id", prog_id).execute()
    else:
        result = supabase.table("degree_programs").insert(payload).execute()
        prog_id = result.data[0]["id"]
    return prog_id


def _upsert_block(supabase, prog_id: str, block: dict, sort_order: int) -> str:
    key = block["block_key"]
    existing = (
        supabase.table("requirement_blocks")
        .select("id")
        .eq("block_key", key)
        .limit(1)
        .execute()
    )
    payload = {
        "program_id":     prog_id,
        "block_key":      key,
        "title":          block["title"],
        "block_type":     block["block_type"],
        "credits_needed": block.get("credits_needed"),
        "courses_needed": block.get("courses_needed"),
        "group_name":     block.get("group_name"),
        "notes":          block.get("notes", ""),
        "sort_order":     sort_order,
    }
    if existing.data:
        block_id = existing.data[0]["id"]
        supabase.table("requirement_blocks").update(payload).eq("id", block_id).execute()
    else:
        result = supabase.table("requirement_blocks").insert(payload).execute()
        block_id = result.data[0]["id"]
    return block_id


def _upsert_courses(supabase, block_id: str, courses: list) -> None:
    supabase.table("requirement_courses").delete().eq("block_id", block_id).execute()
    for i, c in enumerate(courses):
        supabase.table("requirement_courses").insert({
            "block_id":              block_id,
            "subject":               c["subject"],
            "catalog":               c["catalog"],
            "title":                 c.get("title", ""),
            "credits":               c.get("credits", 3),
            "is_required":           c.get("is_required", False),
            "recommended":           c.get("recommended", False),
            "recommendation_reason": c.get("recommendation_reason", ""),
            "choose_from_group":     c.get("choose_from_group"),
            "choose_n_credits":      c.get("choose_n_credits"),
            "notes":                 c.get("notes", ""),
            "sort_order":            i,
        }).execute()


def seed_degree_requirements(supabase) -> dict:
    """Seed all Schulich School of Music degree programs into the database."""
    stats = {"programs": 0, "blocks": 0, "courses": 0, "errors": []}

    for prog in MUSIC_PROGRAMS:
        try:
            prog_id = _upsert_program(supabase, prog)
            stats["programs"] += 1

            for i, block in enumerate(prog.get("blocks", [])):
                try:
                    block_id = _upsert_block(supabase, prog_id, block, i)
                    stats["blocks"] += 1
                    courses = block.get("courses", [])
                    _upsert_courses(supabase, block_id, courses)
                    stats["courses"] += len(courses)
                except Exception as e:
                    msg = f"Block error [{prog['program_key']} / {block.get('block_key')}]: {e}"
                    logger.error(msg)
                    stats["errors"].append(msg)

        except Exception as e:
            msg = f"Program error [{prog.get('program_key')}]: {e}"
            logger.error(msg)
            stats["errors"].append(msg)

    logger.info(f"Music seed complete: {stats}")
    return stats


if __name__ == "__main__":
    import os, sys
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
    from api.utils.supabase_client import get_supabase
    supabase = get_supabase()
    stats = seed_degree_requirements(supabase)
    print(f"Seeded: {stats['programs']} programs, {stats['blocks']} blocks, {stats['courses']} courses")
    if stats.get("errors"):
        print(f"Errors: {stats['errors']}")
