"""
McGill Faculty of Dental Medicine and Oral Health Sciences – Degree Requirements Seed Data
Source: McGill eCalendar 2024-2025 & Course Catalogue
https://coursecatalogue.mcgill.ca/en/undergraduate/dentistry/
https://www.mcgill.ca/study/2024-2025/faculties/dentistry/

This file covers the two undergraduate dentistry programs:
  1. Doctor of Dental Medicine (D.M.D.) – Four-Year Program  (221 credits)
  2. Dental Preparatory Year (Dent-P) – B.Sc. year          ( 30 credits)

Accuracy notes:
  - The DMD curriculum is under constant revision (official eCalendar disclaimer).
  - Year 1 courses are shared with the Faculty of Medicine and Health Sciences
    (INDS 111–119 are the Fundamentals of Medicine and Dentistry block).
  - The 2024-2025 curriculum introduced new DENT 1xx course numbers
    (DENT 111, 112, 114) that replace older DENT 101 series for incoming Y1 students.
  - Clinical Years 3–4 involve rotations at external sites:
      • Oral & Maxillofacial Surgery – Montreal General Hospital
      • Paediatric Dentistry – Montreal Children's Hospital
      • Jim Lund Dental Clinic – Welcome Hall Mission (St. Henri)
      • Alan Edwards Pain Management Unit – Montreal General Hospital
  - Dent-P students must maintain CGPA ≥ 3.5 with all required-course grades ≥ B
    to be promoted into Year 1 of the D.M.D. program.
  - French language proficiency equivalent to B2 intermediate is required by the
    start of Year 3 clinical practice courses.
  - All D.M.D. students must purchase a McGill Instrument Kit from the Faculty.
  - CPR/AED certification (level C+ or C) must be current throughout the program.
  - DAT (Dental Aptitude Test) is NOT required for Fall 2023 or Fall 2024 entry;
    future cycles are under review.
  - CASPer test is mandatory for all applicants.
"""

import logging
logger = logging.getLogger(__name__)

DENTISTRY_PROGRAMS = [

  # ══════════════════════════════════════════════════════════════════════
  #  DOCTOR OF DENTAL MEDICINE (D.M.D.) – FOUR-YEAR PROGRAM (221 credits)
  # ══════════════════════════════════════════════════════════════════════
  {
    "program_key":   "dmd_dentistry",
    "name":          "Doctor of Dental Medicine (D.M.D.) Dentistry – Four-Year Program (221 credits)",
    "program_type":  "major",   # professional degree – mapped to "major" (DB constraint)
    "faculty":       "Faculty of Dental Medicine and Oral Health Sciences",
    "total_credits": 221,
    "description": (
      "The D.M.D. program is an innovative four-year professional degree focused on "
      "evidence-based oral health practice, social justice, and leadership. Years 1–2 "
      "include the Fundamentals of Medicine and Dentistry (FMD) taught jointly with the "
      "Faculty of Medicine and Health Sciences (INDS courses), plus DENT-specific "
      "pre-clinical simulation labs. Year 2 transitions to advanced pre-clinical skills. "
      "Years 3–4 are predominantly clinical practice in the state-of-the-art undergraduate "
      "teaching clinic, with hospital rotations at the Montreal General, Montreal Children's, "
      "and community clinics. Graduates are eligible for licensure by the Ordre des dentistes "
      "du Québec and by other provincial bodies across Canada. Admission requires a completed "
      "120-credit bachelor's degree (any discipline), science prerequisites, and CASPer test. "
      "French B2 proficiency is required by the start of Year 3 clinical courses."
    ),
    "ecalendar_url": (
      "https://www.mcgill.ca/study/2024-2025/faculties/dentistry/undergraduate/programs/"
      "doctor-dental-medicine-dmd-dentistry-four-year-program"
    ),
    "blocks": [

      # ── Year 1: Fundamentals of Medicine & Dentistry (FMD) ─────────────
      {
        "block_key":      "dmd_year1_fmd",
        "title":          "Year 1 – Fundamentals of Medicine and Dentistry (FMD)",
        "block_type":     "required",
        "credits_needed": None,
        "courses_needed": None,
        "group_name":     None,
        "notes": (
          "All Year 1 courses are required. INDS courses (111–119) are taught jointly with "
          "MD,CM students and cover organ systems from the molecular to the global level. "
          "DENT 111J1/J2/J3 runs across Fall, Winter, and Summer terms as a J-series "
          "(must all be completed in consecutive terms). "
          "IPEA 500 and 501 are non-credit interprofessional workshops. "
          "DENT 113D1/D2 (Community Oral Health Services) may not be offered every year – "
          "confirm scheduling on Minerva."
        ),
        "sort_order": 1,
        "courses": [
          # --- FMD shared (INDS) ---
          {"subject": "INDS", "catalog": "111", "title": "Molecules to Global Health",
           "credits": 6, "is_required": True, "recommended": True,
           "recommendation_reason": "First FMD block – molecular biology, pathology pharmacology, and health care systems; opens Year 1 Fall"},
          {"subject": "INDS", "catalog": "112", "title": "Respiration",
           "credits": 6, "is_required": True, "recommended": True,
           "recommendation_reason": "Respiratory system anatomy, physiology, pathology; Year 1 Fall"},
          {"subject": "INDS", "catalog": "113", "title": "Circulation",
           "credits": 8, "is_required": True, "recommended": True,
           "recommendation_reason": "Cardiovascular anatomy, physiology, and pathology; Year 1 Fall"},
          {"subject": "INDS", "catalog": "114", "title": "Digestion and Metabolism",
           "credits": 8, "is_required": True, "recommended": True,
           "recommendation_reason": "GI and hepatobiliary systems, metabolic disorders; Year 1 Winter"},
          {"subject": "INDS", "catalog": "115", "title": "Renal",
           "credits": 6, "is_required": True, "recommended": True,
           "recommendation_reason": "Renal physiology, electrolytes, and renal pathology; Year 1 Winter"},
          {"subject": "INDS", "catalog": "116", "title": "Defense",
           "credits": 6, "is_required": True, "recommended": True,
           "recommendation_reason": "Infectious diseases, immunology, dermatology; Year 1 Summer"},
          {"subject": "INDS", "catalog": "117", "title": "Infection",
           "credits": 6, "is_required": True, "recommended": True,
           "recommendation_reason": "Endocrine disorders; Year 1 Summer"},
          {"subject": "INDS", "catalog": "119J1", "title": "Clinical Method 1",
           "credits": 1, "is_required": True, "recommended": True,
           "recommendation_reason": "Medical interviewing, physical exam, and case history writing; Fall"},
          {"subject": "INDS", "catalog": "119J2", "title": "Clinical Method 1",
           "credits": 1, "is_required": True, "recommended": True,
           "recommendation_reason": "Continuation; Winter"},
          {"subject": "INDS", "catalog": "119J3", "title": "Clinical Method 1",
           "credits": 1, "is_required": True, "recommended": True,
           "recommendation_reason": "Continuation; Summer"},
          # --- DENT Year 1 ---
          {"subject": "DENT", "catalog": "111J1", "title": "Introduction to Dentistry",
           "credits": 2, "is_required": True, "recommended": True,
           "recommendation_reason": "Foundations of dentistry, oral biology, dental public health; Year 1 Fall"},
          {"subject": "DENT", "catalog": "111J2", "title": "Introduction to Dentistry",
           "credits": 2, "is_required": True, "recommended": True,
           "recommendation_reason": "Continuation; Year 1 Winter"},
          {"subject": "DENT", "catalog": "111J3", "title": "Introduction to Dentistry",
           "credits": 2, "is_required": True, "recommended": True,
           "recommendation_reason": "Continuation; Year 1 Summer"},
          {"subject": "DENT", "catalog": "112",   "title": "Oral Medicine and Manifestation of Systemic Diseases",
           "credits": 4, "is_required": True, "recommended": True,
           "recommendation_reason": "Oral manifestations of systemic diseases, diagnosis and management; Year 1 Winter"},
          {"subject": "DENT", "catalog": "113D1", "title": "Community Oral Health Services 1",
           "credits": 0.5, "is_required": True, "recommended": True,
           "recommendation_reason": "Reducing oral health disparities in underserved communities; confirm scheduling on Minerva"},
          {"subject": "DENT", "catalog": "113D2", "title": "Community Oral Health Services 1",
           "credits": 0.5, "is_required": True, "recommended": False,
           "notes": "Continuation of DENT 113D1; must be taken consecutively"},
          {"subject": "DENT", "catalog": "114D1", "title": "Head and Neck Anatomy and Histology",
           "credits": 3, "is_required": True, "recommended": True,
           "recommendation_reason": "Head and neck dissection, histology, pain pathways; Year 1 Winter"},
          {"subject": "DENT", "catalog": "114D2", "title": "Head and Neck Anatomy and Histology",
           "credits": 3, "is_required": True, "recommended": True,
           "recommendation_reason": "Continuation; Year 1 Summer"},
          {"subject": "DENT", "catalog": "125D1", "title": "Oral Health Research 1",
           "credits": 0.5, "is_required": True, "recommended": True,
           "recommendation_reason": "Introduction to research fundamentals and activities at the faculty"},
          {"subject": "DENT", "catalog": "125D2", "title": "Oral Health Research 1",
           "credits": 0.5, "is_required": True, "recommended": False,
           "notes": "Continuation of DENT 125D1"},
          {"subject": "DENT", "catalog": "210",   "title": "Introduction to Oral Medicine and Oral Diagnosis",
           "credits": 1, "is_required": True, "recommended": True,
           "recommendation_reason": "Patient workup, differential diagnosis, treatment planning; prereq: DENT 101J1/J2/J3 or DENT 111J1/J2/J3"},
          # --- Interprofessional (non-credit) ---
          {"subject": "IPEA", "catalog": "500",   "title": "Roles in Interprofessional Teams",
           "credits": 0, "is_required": True, "recommended": True,
           "recommendation_reason": "Non-credit half-day workshop on interprofessional team roles; Year 1 Fall"},
          {"subject": "IPEA", "catalog": "501",   "title": "Communication in Interprofessional Teams",
           "credits": 0, "is_required": True, "recommended": True,
           "recommendation_reason": "Non-credit workshop on communication in healthcare teams; Year 1 Winter"},
        ],
      },

      # ── Year 2 FMD (continued) ──────────────────────────────────────────
      {
        "block_key":      "dmd_year2_fmd",
        "title":          "Year 2 – Fundamentals of Medicine (continued)",
        "block_type":     "required",
        "credits_needed": None,
        "courses_needed": None,
        "group_name":     None,
        "notes": (
          "INDS 211 and 212 complete the FMD shared curriculum. Both require successful "
          "completion of all Promotion Period I courses (Year 1 block) before enrolment."
        ),
        "sort_order": 2,
        "courses": [
          {"subject": "INDS", "catalog": "211", "title": "Reproduction and Sexuality",
           "credits": 6, "is_required": True, "recommended": True,
           "recommendation_reason": "Reproductive anatomy, physiology, pathology; Year 2 Fall"},
          {"subject": "INDS", "catalog": "212", "title": "Human Behaviour",
           "credits": 12, "is_required": True, "recommended": True,
           "recommendation_reason": "Psychiatry, neurology, and CNS pathology; Year 2 Fall"},
        ],
      },

      # ── Year 2 DENT-specific ────────────────────────────────────────────
      {
        "block_key":      "dmd_year2_dent",
        "title":          "Year 2 – Dental Sciences and Pre-Clinical Skills",
        "block_type":     "required",
        "credits_needed": None,
        "courses_needed": None,
        "group_name":     None,
        "notes": (
          "Year 2 builds dental science knowledge and begins simulation lab training. "
          "DENT 242J1/J2/J3 (Restorative Dentistry Operative) covers tooth preparation "
          "and direct restorations. DENT 243 (Endodontics A) covers root canal fundamentals. "
          "DENT 244D1/D2 (Pediatric Dentistry A) includes rotation at Montreal Children's Hospital. "
          "DENT 245D1/D2 (Fixed Prosthodontics), DENT 246D1/D2 (Partial Edentulism), "
          "DENT 247D1/D2 (Complete Edentulism), DENT 249D1/D2 (Orthodontics intro), and "
          "DENT 250D1/D2 (Introduction to Clinical Care) complete the pre-clinical skill set. "
          "Verified from 2024-2025 eCalendar."
        ),
        "sort_order": 3,
        "courses": [
          {"subject": "DENT", "catalog": "213D1", "title": "Community Oral Health Services 2",
           "credits": 0.5, "is_required": True, "recommended": True,
           "recommendation_reason": "Community clinic program continuation; Year 2"},
          {"subject": "DENT", "catalog": "213D2", "title": "Community Oral Health Services 2",
           "credits": 0.5, "is_required": True, "recommended": False,
           "notes": "Continuation of DENT 213D1"},
          {"subject": "DENT", "catalog": "222D1", "title": "Radiology",
           "credits": 1.5, "is_required": True, "recommended": True,
           "recommendation_reason": "Radiation physics, imaging, caries/perio/periapical radiographic interpretation; Year 2"},
          {"subject": "DENT", "catalog": "222D2", "title": "Radiology",
           "credits": 1.5, "is_required": True, "recommended": False,
           "notes": "Continuation of DENT 222D1"},
          {"subject": "DENT", "catalog": "225D1", "title": "Oral Health Research 2",
           "credits": 1, "is_required": True, "recommended": True,
           "recommendation_reason": "Research design and hands-on research experience; prereq: DENT 125D1/D2"},
          {"subject": "DENT", "catalog": "225D2", "title": "Oral Health Research 2",
           "credits": 1, "is_required": True, "recommended": False,
           "notes": "Continuation of DENT 225D1"},
          {"subject": "DENT", "catalog": "231",   "title": "Professional Identity Development",
           "credits": 2, "is_required": True, "recommended": True,
           "recommendation_reason": "Social justice, equity, diversity, interprofessional relations; Year 2"},
          {"subject": "DENT", "catalog": "232",   "title": "Dental Public Health A",
           "credits": 3, "is_required": True, "recommended": True,
           "recommendation_reason": "Oral health, sustainable dentistry, patient-centred care; Year 2"},
          {"subject": "DENT", "catalog": "240",   "title": "Dental Anatomy and Occlusion",
           "credits": 3, "is_required": True, "recommended": True,
           "recommendation_reason": "Tooth anatomy, occlusal principles; foundational for all restorative work; Year 2"},
          {"subject": "DENT", "catalog": "241",   "title": "Cariology",
           "credits": 3, "is_required": True, "recommended": True,
           "recommendation_reason": "Evidence-based caries diagnosis, risk assessment, minimal intervention; Year 2"},
          {"subject": "DENT", "catalog": "242J1", "title": "Restorative Dentistry (Operative)",
           "credits": 2, "is_required": True, "recommended": True,
           "recommendation_reason": "Psychomotor simulation lab – tooth prep, direct restorations, biomaterials; Year 2"},
          {"subject": "DENT", "catalog": "242J2", "title": "Restorative Dentistry (Operative)",
           "credits": 2, "is_required": True, "recommended": False,
           "notes": "Continuation of DENT 242J1"},
          {"subject": "DENT", "catalog": "242J3", "title": "Restorative Dentistry (Operative)",
           "credits": 2, "is_required": True, "recommended": False,
           "notes": "Continuation of DENT 242J2"},
          {"subject": "DENT", "catalog": "243",   "title": "Endodontics A",
           "credits": 4, "is_required": True, "recommended": True,
           "recommendation_reason": "Fundamental endodontic therapy concepts and psychomotor skill development; Year 2"},
          {"subject": "DENT", "catalog": "244D1", "title": "Pediatric Dentistry A",
           "credits": 2, "is_required": True, "recommended": True,
           "recommendation_reason": "Pediatric oral health and clinical dentistry; includes rotation at Montreal Children's Hospital; Year 2"},
          {"subject": "DENT", "catalog": "244D2", "title": "Pediatric Dentistry A",
           "credits": 2, "is_required": True, "recommended": False,
           "notes": "Continuation of DENT 244D1"},
          {"subject": "DENT", "catalog": "245D1", "title": "Restorative Dentistry (Fixed Prosthodontics)",
           "credits": 2, "is_required": True, "recommended": True,
           "recommendation_reason": "Fixed prosthodontics: crown and bridge pre-clinical simulation; Year 2"},
          {"subject": "DENT", "catalog": "245D2", "title": "Restorative Dentistry (Fixed Prosthodontics)",
           "credits": 2, "is_required": True, "recommended": False,
           "notes": "Continuation of DENT 245D1"},
          {"subject": "DENT", "catalog": "246D1", "title": "Management of Partial Edentulism",
           "credits": 1.5, "is_required": True, "recommended": True,
           "recommendation_reason": "Removable partial dentures – design, fabrication, clinical skills; Year 2"},
          {"subject": "DENT", "catalog": "246D2", "title": "Management of Partial Edentulism",
           "credits": 1.5, "is_required": True, "recommended": False,
           "notes": "Continuation of DENT 246D1"},
          {"subject": "DENT", "catalog": "247D1", "title": "Management of Complete Edentulism",
           "credits": 1.5, "is_required": True, "recommended": True,
           "recommendation_reason": "Complete dentures – diagnosis, design, and fabrication; Year 2"},
          {"subject": "DENT", "catalog": "247D2", "title": "Management of Complete Edentulism",
           "credits": 1.5, "is_required": True, "recommended": False,
           "notes": "Continuation of DENT 247D1"},
          {"subject": "DENT", "catalog": "248",   "title": "Periodontics",
           "credits": 3, "is_required": True, "recommended": True,
           "recommendation_reason": "Periodontal anatomy, disease, non-surgical therapy, and clinical skills; Year 2"},
          {"subject": "DENT", "catalog": "249D1", "title": "Introduction to Development and Orthodontics",
           "credits": 2, "is_required": True, "recommended": True,
           "recommendation_reason": "Craniofacial development, malocclusion, orthodontic principles; Year 2"},
          {"subject": "DENT", "catalog": "249D2", "title": "Introduction to Development and Orthodontics",
           "credits": 2, "is_required": True, "recommended": False,
           "notes": "Continuation of DENT 249D1"},
          {"subject": "DENT", "catalog": "250D1", "title": "Introduction to Clinical Care",
           "credits": 3, "is_required": True, "recommended": True,
           "recommendation_reason": "Patient assessment, treatment planning, and first clinical patient encounters; Year 2"},
          {"subject": "DENT", "catalog": "250D2", "title": "Introduction to Clinical Care",
           "credits": 3, "is_required": True, "recommended": False,
           "notes": "Continuation of DENT 250D1"},
        ],
      },

      # ── Year 3: Clinical Practice ───────────────────────────────────────
      {
        "block_key":      "dmd_year3_clinical",
        "title":          "Year 3 – Clinical Practice",
        "block_type":     "required",
        "credits_needed": None,
        "courses_needed": None,
        "group_name":     None,
        "notes": (
          "Year 3 transitions fully into clinical practice in the undergraduate teaching clinic "
          "and hospital rotations. French B2 proficiency is required by the start of Year 3. "
          "DENT 315J1/J2/J3 (Orthodontics 1), DENT 318J1/J2/J3 (Periodontology), "
          "DENT 320J1/J2/J3 (Restorative Dentistry), DENT 323J1/J2/J3 (Oral and Maxillofacial Surgery) "
          "are J-series courses spanning the full year. "
          "Verified from 2024-2025 eCalendar."
        ),
        "sort_order": 4,
        "courses": [
          {"subject": "DENT", "catalog": "307D1", "title": "Business Aspects of Dentistry",
           "credits": 1, "is_required": True, "recommended": True,
           "recommendation_reason": "Practice management, ethics, and business skills for dental practice; Year 3"},
          {"subject": "DENT", "catalog": "307D2", "title": "Business Aspects of Dentistry",
           "credits": 1, "is_required": True, "recommended": False,
           "notes": "Continuation of DENT 307D1"},
          {"subject": "DENT", "catalog": "309J1", "title": "Implantology",
           "credits": 1.67, "is_required": True, "recommended": True,
           "recommendation_reason": "Dental implant fundamentals and clinical application; Year 3"},
          {"subject": "DENT", "catalog": "309J2", "title": "Implantology",
           "credits": 1.67, "is_required": True, "recommended": False,
           "notes": "Continuation of DENT 309J1"},
          {"subject": "DENT", "catalog": "309J3", "title": "Implantology",
           "credits": 1.66, "is_required": True, "recommended": False,
           "notes": "Continuation of DENT 309J2"},
          {"subject": "DENT", "catalog": "313D1", "title": "Community Oral Health Services 3",
           "credits": 1.5, "is_required": True, "recommended": True,
           "recommendation_reason": "Community clinical rotations including Welcome Hall Mission; Year 3"},
          {"subject": "DENT", "catalog": "313D2", "title": "Community Oral Health Services 3",
           "credits": 1.5, "is_required": True, "recommended": False,
           "notes": "Continuation of DENT 313D1"},
          {"subject": "DENT", "catalog": "315J1", "title": "Orthodontics 1",
           "credits": 2, "is_required": True, "recommended": True,
           "recommendation_reason": "Clinical orthodontics including tooth movement and case management; Year 3"},
          {"subject": "DENT", "catalog": "315J2", "title": "Orthodontics 1",
           "credits": 2, "is_required": True, "recommended": False,
           "notes": "Continuation of DENT 315J1"},
          {"subject": "DENT", "catalog": "315J3", "title": "Orthodontics 1",
           "credits": 2, "is_required": True, "recommended": False,
           "notes": "Continuation of DENT 315J2"},
          {"subject": "DENT", "catalog": "317D1", "title": "Oral Pathology and Medicine",
           "credits": 1.5, "is_required": True, "recommended": True,
           "recommendation_reason": "Diagnosis of oral diseases and lesions; Year 3"},
          {"subject": "DENT", "catalog": "317D2", "title": "Oral Pathology and Medicine",
           "credits": 1.5, "is_required": True, "recommended": False,
           "notes": "Continuation of DENT 317D1"},
          {"subject": "DENT", "catalog": "318J1", "title": "Periodontology",
           "credits": 1.33, "is_required": True, "recommended": True,
           "recommendation_reason": "Advanced periodontal therapy in clinical setting; Year 3"},
          {"subject": "DENT", "catalog": "318J2", "title": "Periodontology",
           "credits": 1.33, "is_required": True, "recommended": False,
           "notes": "Continuation of DENT 318J1"},
          {"subject": "DENT", "catalog": "318J3", "title": "Periodontology",
           "credits": 1.34, "is_required": True, "recommended": False,
           "notes": "Continuation of DENT 318J2"},
          {"subject": "DENT", "catalog": "319D1", "title": "Dental Pharmacology",
           "credits": 1.5, "is_required": True, "recommended": True,
           "recommendation_reason": "Pharmacology of drugs used in dental practice including local anaesthetics; Year 3"},
          {"subject": "DENT", "catalog": "319D2", "title": "Dental Pharmacology",
           "credits": 1.5, "is_required": True, "recommended": False,
           "notes": "Continuation of DENT 319D1"},
          {"subject": "DENT", "catalog": "320J1", "title": "Restorative Dentistry",
           "credits": 2, "is_required": True, "recommended": True,
           "recommendation_reason": "Advanced restorative dentistry in clinical setting; Year 3"},
          {"subject": "DENT", "catalog": "320J2", "title": "Restorative Dentistry",
           "credits": 2, "is_required": True, "recommended": False,
           "notes": "Continuation of DENT 320J1"},
          {"subject": "DENT", "catalog": "320J3", "title": "Restorative Dentistry",
           "credits": 2, "is_required": True, "recommended": False,
           "notes": "Continuation of DENT 320J2"},
          {"subject": "DENT", "catalog": "322J1", "title": "Image Interpretation",
           "credits": 0.67, "is_required": True, "recommended": True,
           "recommendation_reason": "Advanced radiographic and digital image interpretation; Year 3"},
          {"subject": "DENT", "catalog": "322J2", "title": "Image Interpretation",
           "credits": 0.67, "is_required": True, "recommended": False,
           "notes": "Continuation of DENT 322J1"},
          {"subject": "DENT", "catalog": "322J3", "title": "Image Interpretation",
           "credits": 0.66, "is_required": True, "recommended": False,
           "notes": "Continuation of DENT 322J2"},
          {"subject": "DENT", "catalog": "323J1", "title": "Oral and Maxillofacial Surgery",
           "credits": 0.7, "is_required": True, "recommended": True,
           "recommendation_reason": "Oral surgery clinic rotation including Montreal General Hospital; Year 3"},
          {"subject": "DENT", "catalog": "323J2", "title": "Oral and Maxillofacial Surgery",
           "credits": 0.7, "is_required": True, "recommended": False,
           "notes": "Continuation of DENT 323J1"},
          {"subject": "DENT", "catalog": "323J3", "title": "Oral and Maxillofacial Surgery",
           "credits": 0.6, "is_required": True, "recommended": False,
           "notes": "Continuation of DENT 323J2"},
          {"subject": "DENT", "catalog": "325D1", "title": "Oral Health Research 3",
           "credits": 1, "is_required": True, "recommended": True,
           "recommendation_reason": "Advanced research project; Year 3"},
          {"subject": "DENT", "catalog": "325D2", "title": "Oral Health Research 3",
           "credits": 1, "is_required": True, "recommended": False,
           "notes": "Continuation of DENT 325D1"},
        ],
      },

      # ── Year 4: Senior Clinical Practice ───────────────────────────────
      {
        "block_key":      "dmd_year4_clinical",
        "title":          "Year 4 – Senior Clinical Practice",
        "block_type":     "required",
        "credits_needed": None,
        "courses_needed": None,
        "group_name":     None,
        "notes": (
          "Year 4 is predominantly clinical clerkship in the undergraduate teaching clinic "
          "and hospital rotations. DENT 450D1/D2 (Clinical Practice/Senior Clerkship) is the "
          "primary clinical component. DENT 415D1/D2 (Orthodontics 2) and DENT 423D1/D2 "
          "(Oral Maxillofacial Surgery & Pathology) are major clinical courses. "
          "Year 4 Fall totals 22.5 credits and Winter totals 13.5 credits (36 credits total for Year 4). "
          "Verified from 2024-2025 eCalendar and Faculty curriculum page."
        ),
        "sort_order": 5,
        "courses": [
          {"subject": "DENT", "catalog": "407D1", "title": "Practice Management",
           "credits": 1, "is_required": True, "recommended": True,
           "recommendation_reason": "Advanced practice management and business aspects of running a dental office; Year 4 Fall"},
          {"subject": "DENT", "catalog": "407D2", "title": "Practice Management",
           "credits": 1, "is_required": True, "recommended": False,
           "notes": "Continuation of DENT 407D1"},
          {"subject": "DENT", "catalog": "413",   "title": "Community Oral Health Services 4",
           "credits": 1, "is_required": True, "recommended": True,
           "recommendation_reason": "Final community oral health rotation; Year 4 Fall"},
          {"subject": "DENT", "catalog": "415D1", "title": "Orthodontics 2",
           "credits": 3.5, "is_required": True, "recommended": True,
           "recommendation_reason": "Advanced clinical orthodontics; Year 4 Fall"},
          {"subject": "DENT", "catalog": "415D2", "title": "Orthodontics 2",
           "credits": 3.5, "is_required": True, "recommended": False,
           "notes": "Continuation of DENT 415D1"},
          {"subject": "DENT", "catalog": "418D1", "title": "Periodontology Seminar",
           "credits": 1, "is_required": True, "recommended": True,
           "recommendation_reason": "Advanced periodontal seminars and case presentations; Year 4 Fall"},
          {"subject": "DENT", "catalog": "418D2", "title": "Periodontology Seminar",
           "credits": 1, "is_required": True, "recommended": False,
           "notes": "Continuation of DENT 418D1; must be taken consecutively"},
          {"subject": "DENT", "catalog": "420",   "title": "Restorative Dentistry Seminars",
           "credits": 3, "is_required": True, "recommended": True,
           "recommendation_reason": "Senior restorative dentistry seminars and clinical cases; Year 4 Fall"},
          {"subject": "DENT", "catalog": "423D1", "title": "Oral Maxillofacial Surgery and Pathology",
           "credits": 2, "is_required": True, "recommended": True,
           "recommendation_reason": "Advanced oral surgery and pathology clinical rotation; Year 4 Fall"},
          {"subject": "DENT", "catalog": "423D2", "title": "Oral Maxillofacial Surgery and Pathology",
           "credits": 2, "is_required": True, "recommended": False,
           "notes": "Continuation of DENT 423D1"},
          {"subject": "DENT", "catalog": "437",   "title": "Clinical Decision Making",
           "credits": 3, "is_required": True, "recommended": True,
           "recommendation_reason": "Integrated clinical decision making across all dental disciplines; Year 4 Fall"},
          {"subject": "DENT", "catalog": "438D1", "title": "Management of Orofacial Pain",
           "credits": 1.5, "is_required": True, "recommended": True,
           "recommendation_reason": "Diagnosis and management of temporomandibular disorders and orofacial pain; Year 4 Fall"},
          {"subject": "DENT", "catalog": "438D2", "title": "Management of Orofacial Pain",
           "credits": 1.5, "is_required": True, "recommended": False,
           "notes": "Continuation of DENT 438D1"},
          {"subject": "DENT", "catalog": "443D1", "title": "Endodontics C",
           "credits": 0.5, "is_required": True, "recommended": True,
           "recommendation_reason": "Advanced endodontic clinical seminars; Year 4 Fall"},
          {"subject": "DENT", "catalog": "443D2", "title": "Endodontics C",
           "credits": 0.5, "is_required": True, "recommended": False,
           "notes": "Continuation of DENT 443D1"},
          {"subject": "DENT", "catalog": "444D1", "title": "Pediatric Dentistry C",
           "credits": 0.5, "is_required": True, "recommended": True,
           "recommendation_reason": "Advanced pediatric dentistry seminars; Year 4 Fall"},
          {"subject": "DENT", "catalog": "444D2", "title": "Pediatric Dentistry C",
           "credits": 0.5, "is_required": True, "recommended": False,
           "notes": "Continuation of DENT 444D1"},
          {"subject": "DENT", "catalog": "446D1", "title": "Ethics and Jurisprudence",
           "credits": 0.5, "is_required": True, "recommended": True,
           "recommendation_reason": "Dental ethics, law, professional regulation, and Quebec dental legislation; Year 4 Fall"},
          {"subject": "DENT", "catalog": "446D2", "title": "Ethics and Jurisprudence",
           "credits": 0.5, "is_required": True, "recommended": False,
           "notes": "Continuation of DENT 446D1"},
          {"subject": "DENT", "catalog": "450D1", "title": "Clinical Practice 2",
           "credits": 3.5, "is_required": True, "recommended": True,
           "recommendation_reason": "Primary senior clinical clerkship in undergraduate teaching clinic; Year 4 Fall"},
          {"subject": "DENT", "catalog": "450D2", "title": "Clinical Practice 2",
           "credits": 3.5, "is_required": True, "recommended": False,
           "notes": "Continuation of DENT 450D1"},
          {"subject": "DENT", "catalog": "451D1", "title": "Focused Clinical Training",
           "credits": 0.5, "is_required": True, "recommended": True,
           "recommendation_reason": "Targeted clinical training for identified competency gaps; Year 4 Fall"},
          {"subject": "DENT", "catalog": "451D2", "title": "Focused Clinical Training",
           "credits": 0.5, "is_required": True, "recommended": False,
           "notes": "Continuation of DENT 451D1"},
        ],
      },

    ],
  },

  # ══════════════════════════════════════════════════════════════════════
  #  DENTAL PREPARATORY YEAR (DENT-P) – B.Sc. (30 credits)
  # ══════════════════════════════════════════════════════════════════════
  {
    "program_key":   "dentp_bsc",
    "name":          "Dental Preparatory Year (Dent-P) – B.Sc. (30 credits)",
    "program_type":  "diploma",  # preparatory year – mapped to "diploma" (DB constraint)
    "faculty":       "Faculty of Dental Medicine and Oral Health Sciences",
    "total_credits": 30,
    "description": (
      "The Dent-P Year is a one-year preparatory program for direct CEGEP graduates "
      "(Quebec residents only) who wish to enter the four-year D.M.D. program. "
      "Students are registered in the Faculty of Science during the preparatory year "
      "and must complete 30 credits: 18 credits of required sciences + 12 credits of "
      "humanities/electives. Students must maintain a CGPA of ≥ 3.5 with all individual "
      "grades ≥ B in required courses and passing grades in complementary courses to be "
      "promoted into D.M.D. Year 1. Application deadline is March 1 (vs November 1 "
      "for the direct 4-year D.M.D.). Dent-P is open only to current final-year CEGEP "
      "Sciences Profile students who are Quebec residents. University-level students and "
      "students outside Quebec are NOT eligible for this program. CASPer test is required. "
      "Students who do not meet promotion criteria may transfer into a B.Sc. and reapply "
      "to the D.M.D. after completing their undergraduate degree."
    ),
    "ecalendar_url": (
      "https://www.mcgill.ca/study/2024-2025/faculties/dentistry/undergraduate/programs/"
      "bachelor-science-bsc-dental-preparatory-dent-p"
    ),
    "blocks": [

      {
        "block_key":      "dentp_sciences",
        "title":          "Required Science Courses (18 credits)",
        "block_type":     "required",
        "credits_needed": 18,
        "courses_needed": None,
        "group_name":     None,
        "notes": (
          "18 credits of required science courses (BIOL 200, 201, 202; PHGY 209, 210; MATH 203). "
          "All required courses must be passed with a grade of B or higher for promotion to DMD Year 1. "
          "These are the same required courses as the Med-P program. "
          "These credits count toward a B.Sc. if the student does not proceed to DMD."
        ),
        "sort_order": 1,
        "courses": [
          {"subject": "BIOL",  "catalog": "200",  "title": "Molecular Biology",
           "credits": 3, "is_required": True, "recommended": True,
           "recommendation_reason": "Core molecular biology; required with minimum grade B for Dent-P promotion"},
          {"subject": "BIOL",  "catalog": "201",  "title": "Cell Biology and Metabolism",
           "credits": 3, "is_required": True, "recommended": True,
           "recommendation_reason": "Cell biology and metabolism; required with minimum grade B"},
          {"subject": "BIOL",  "catalog": "202",  "title": "Basic Genetics",
           "credits": 3, "is_required": True, "recommended": True,
           "recommendation_reason": "Genetics; required with minimum grade B"},
          {"subject": "PHGY",  "catalog": "209",  "title": "Mammalian Physiology 1",
           "credits": 3, "is_required": True, "recommended": True,
           "recommendation_reason": "Physiology 1; required with minimum grade B"},
          {"subject": "PHGY",  "catalog": "210",  "title": "Mammalian Physiology 2",
           "credits": 3, "is_required": True, "recommended": True,
           "recommendation_reason": "Physiology 2; required with minimum grade B"},
          {"subject": "MATH",  "catalog": "203",  "title": "Principles of Statistics 1",
           "credits": 3, "is_required": True, "recommended": True,
           "recommendation_reason": "Statistics; required with minimum grade B"},
        ],
      },

      {
        "block_key":      "dentp_humanities",
        "title":          "Complementary Humanities / Elective Courses (12 credits)",
        "block_type":     "choose_credits",
        "credits_needed": 12,
        "courses_needed": None,
        "group_name":     None,
        "notes": (
          "12 credits of humanities, social sciences, or elective courses are required "
          "to round out the 30-credit Dent-P year. Passing grades are required (B not "
          "mandatory). Courses are selected to broaden education in preparation for a "
          "patient-facing professional career. The Faculty of Dentistry encourages "
          "courses that develop interpersonal skills, active listening, empathy, and "
          "cultural competence. Examples include psychology, sociology, ethics, "
          "communication, or language courses. "
          "Confirm specific approved electives with the Dent-P program coordinator."
        ),
        "sort_order": 2,
        "courses": [
          {"subject": "PSYC",  "catalog": "100",  "title": "Introduction to Psychology",
           "credits": 3, "is_required": False, "recommended": True,
           "recommendation_reason": "Strongly recommended – develops understanding of human behaviour and patient communication skills"},
          {"subject": "SOCI",  "catalog": "210",  "title": "Sociological Perspectives",
           "credits": 3, "is_required": False, "recommended": True,
           "recommendation_reason": "Understanding social determinants of health; relevant to dentistry's social justice mission"},
          {"subject": "PHIL",  "catalog": "343",  "title": "Biomedical Ethics",
           "credits": 3, "is_required": False, "recommended": True,
           "recommendation_reason": "Biomedical ethics; excellent preparation for professional practice"},
          {"subject": "FRSL",  "catalog": "215",  "title": "Oral and Written French 1 - Intensive",
           "credits": 6, "is_required": False, "recommended": True,
           "recommendation_reason": "French proficiency is required by Year 3 DMD; starting early is highly recommended"},
        ],
      },

    ],
  },

]


# ═══════════════════════════════════════════════════════════════════════════════
#  Seed helper – same upsert pattern as all other seed files
# ═══════════════════════════════════════════════════════════════════════════════

def _upsert_program(supabase, prog: dict) -> str:
    """Insert or update one program record, returning its DB id."""
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
        logger.info(f"Updated program: {key}")
    else:
        result = supabase.table("degree_programs").insert(payload).execute()
        prog_id = result.data[0]["id"]
        logger.info(f"Inserted program: {key}")

    return prog_id


def _upsert_block(supabase, prog_id: str, block: dict, sort_order: int) -> str:
    """Insert or update one requirement block, returning its DB id."""
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
    """Delete existing courses for a block and re-insert fresh."""
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
            "choose_from_group":     c.get("choose_from_group", None),
            "choose_n_credits":      c.get("choose_n_credits", None),
            "notes":                 c.get("notes", ""),
            "sort_order":            i,
        }).execute()


def seed_degree_requirements(supabase) -> dict:
    """Seed all Dentistry degree programs into the database."""
    stats = {"programs": 0, "blocks": 0, "courses": 0, "errors": []}

    for prog in DENTISTRY_PROGRAMS:
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

    logger.info(f"Dentistry seed complete: {stats}")
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
