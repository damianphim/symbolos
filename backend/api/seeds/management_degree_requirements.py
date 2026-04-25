"""
McGill Desautels Faculty of Management – BCom Degree Requirements Seed Data
Source: McGill Course Catalogue 2024-2025 / 2025-2026
https://coursecatalogue.mcgill.ca/en/undergraduate/management/
https://www.mcgill.ca/desautels/programs/bcom/academics/programstructure

Run this script directly to populate the database, or import MANAGEMENT_PROGRAMS
and use it in the API route.

Accuracy notes:
  - Core curriculum and Accounting/Finance/Marketing majors verified from
    official McGill Course Catalogue PDFs (accounting-major-bcom.pdf,
    finance-major-bcom.pdf) and Desautels program pages.
  - Concentration courses verified from marketing-concentration-bcom.pdf,
    2024-2025 eCalendar, and McGill course pages.
  - Always cross-check with current catalogue before academic decisions:
    https://coursecatalogue.mcgill.ca/en/undergraduate/management/programs/

Program structure overview:
  - BCom is 90 credits (CEGEP entry) or 120 credits (out-of-province/international).
  - All students complete 42 credits of Management Core (Fall 2024+ intake;
    39 credits for students admitted prior to Fall 2024 — no MGCR 233).
  - Students then pursue either:
      * Two Concentrations (15 credits each) — General Management path
      * One Concentration + one non-management Minor
      * One Major (30 credits)
      * Honours in Investment Management (45 credits)
  - Plus 18 credits of electives (non-management or management).
  - Fall 2024+ students also require 3 credits of Experiential Learning.
"""

MANAGEMENT_PROGRAMS = [

  # ══════════════════════════════════════════════════════════════════
  # BCom MANAGEMENT CORE (42 credits — Fall 2024+ intake)
  # ══════════════════════════════════════════════════════════════════
  {
    "program_key": "bcom_core",
    "name": "BCom Management Core Curriculum",
    "program_type": "core",
    "faculty": "Desautels Faculty of Management",
    "total_credits": 42,
    "description": (
      "All BCom students (admitted Fall 2024 and after) must complete 42 credits "
      "of Management Core courses. Students admitted prior to Fall 2024 complete "
      "39 credits (same courses but without MGCR 233). A grade of C or better is "
      "required for all core courses; a D requires repeating the course."
    ),
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/management/programs/management-core/",
    "blocks": [
      {
        "block_key": "bcom_core_required",
        "title": "Management Core Courses",
        "block_type": "required",
        "credits_needed": 42,
        "courses_needed": None,
        "group_name": None,
        "notes": (
          "A grade of C or better is required. If a D is obtained, the course must "
          "be repeated. MGCR 233 is only required for students admitted Fall 2024 "
          "and after. Students pursuing an Economics Major replace MGCR 293 with "
          "ECON 230D1/D2, and MGCR 294 with ECON 332 + ECON 333."
        ),
        "sort_order": 1,
        "courses": [
          {"subject": "MGCR", "catalog": "211", "title": "Introduction to Financial Accounting",       "credits": 3, "is_required": True},
          {"subject": "MGCR", "catalog": "222", "title": "Introduction to Organizational Behaviour",  "credits": 3, "is_required": True},
          {"subject": "MGCR", "catalog": "233", "title": "Data Programming for Business",              "credits": 3, "is_required": True},
          {"subject": "MGCR", "catalog": "250", "title": "Expressive Analysis for Management",        "credits": 3, "is_required": True},
          {"subject": "MGCR", "catalog": "271", "title": "Business Statistics",                       "credits": 3, "is_required": True},
          {"subject": "MGCR", "catalog": "293", "title": "Managerial Economics",                      "credits": 3, "is_required": True},
          {"subject": "MGCR", "catalog": "294", "title": "The Firm in the Macroeconomy",              "credits": 3, "is_required": True},
          {"subject": "MGCR", "catalog": "331", "title": "Information Technology Management",         "credits": 3, "is_required": True},
          {"subject": "MGCR", "catalog": "341", "title": "Introduction to Finance",                   "credits": 3, "is_required": True},
          {"subject": "MGCR", "catalog": "352", "title": "Principles of Marketing",                   "credits": 3, "is_required": True},
          {"subject": "MGCR", "catalog": "372", "title": "Operations Management",                     "credits": 3, "is_required": True},
          {"subject": "MGCR", "catalog": "382", "title": "International Business",                    "credits": 3, "is_required": True},
          {"subject": "MGCR", "catalog": "423", "title": "Strategic Management",                      "credits": 3, "is_required": True},
          {"subject": "MGCR", "catalog": "460", "title": "Social Context of Business",                "credits": 3, "is_required": True},
        ],
      },
    ],
  },


  # ══════════════════════════════════════════════════════════════════
  # ACCOUNTING
  # ══════════════════════════════════════════════════════════════════
  {
    "program_key": "accounting_major_bcom",
    "name": "Accounting – Major (B.Com.)",
    "program_type": "major",
    "faculty": "Desautels Faculty of Management",
    "total_credits": 30,
    "description": (
      "The B.Com. Major in Accounting focuses on preparing, interpreting, and "
      "utilizing the financial and managerial information of an organization. "
      "The program includes financial and managerial accounting, auditing, and "
      "taxation. Students typically pursue the CPA designation after graduation."
    ),
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/management/programs/majors/accounting-major-bcom/",
    "blocks": [
      {
        "block_key": "acct_major_required",
        "title": "Required Major Courses",
        "block_type": "required",
        "credits_needed": 18,
        "courses_needed": None,
        "group_name": None,
        "notes": "All 6 courses (18 credits) are required. Minimum grade of C in each.",
        "sort_order": 1,
        "courses": [
          {"subject": "ACCT", "catalog": "351", "title": "Intermediate Financial Accounting 1",  "credits": 3, "is_required": True},
          {"subject": "ACCT", "catalog": "352", "title": "Intermediate Financial Accounting 2",  "credits": 3, "is_required": True},
          {"subject": "ACCT", "catalog": "361", "title": "Management Accounting",                "credits": 3, "is_required": True},
          {"subject": "ACCT", "catalog": "362", "title": "Cost Accounting",                     "credits": 3, "is_required": True},
          {"subject": "ACCT", "catalog": "385", "title": "Principles of Taxation",              "credits": 3, "is_required": True},
          {"subject": "ACCT", "catalog": "455", "title": "Development of Accounting Thought",   "credits": 3, "is_required": True},
        ],
      },
      {
        "block_key": "acct_major_complementary",
        "title": "Complementary Courses",
        "block_type": "group",
        "credits_needed": 12,
        "courses_needed": None,
        "group_name": "12 credits from Complementary Accounting Courses",
        "notes": "12 credits selected from the following list.",
        "sort_order": 2,
        "courses": [
          {"subject": "ACCT", "catalog": "354", "title": "Financial Statement Analysis",          "credits": 3, "is_required": False},
          {"subject": "ACCT", "catalog": "401", "title": "Sustainability and Environmental Accounting", "credits": 3, "is_required": False},
          {"subject": "ACCT", "catalog": "434", "title": "Topics in Accounting 1",               "credits": 3, "is_required": False},
          {"subject": "ACCT", "catalog": "451", "title": "Data Analytics in Capital Market",     "credits": 3, "is_required": False},
          {"subject": "ACCT", "catalog": "452", "title": "Financial Reporting Valuation",        "credits": 3, "is_required": False},
          {"subject": "ACCT", "catalog": "453", "title": "Advanced Financial Accounting",        "credits": 3, "is_required": False},
          {"subject": "ACCT", "catalog": "463", "title": "Management Control",                   "credits": 3, "is_required": False},
          {"subject": "ACCT", "catalog": "475", "title": "Principles of Auditing",               "credits": 3, "is_required": False},
          {"subject": "ACCT", "catalog": "486", "title": "Business Taxation 2",                  "credits": 3, "is_required": False},
        ],
      },
    ],
  },

  {
    "program_key": "accounting_concentration_bcom",
    "name": "Accounting – Concentration (B.Com.)",
    "program_type": "concentration",
    "faculty": "Desautels Faculty of Management",
    "total_credits": 15,
    "description": (
      "The Accounting concentration is designed for Management students who want "
      "a solid basic understanding of accounting but do not intend to become "
      "professional accountants. It is oriented toward users of financial information "
      "and emphasizes breadth of knowledge in a coherent selection of courses. "
      "Consists of 5 courses (15 credits)."
    ),
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/management/programs/concentrations/accounting-concentration-bcom/",
    "blocks": [
      {
        "block_key": "acct_conc_required",
        "title": "Required Accounting Courses",
        "block_type": "required",
        "credits_needed": 6,
        "courses_needed": None,
        "group_name": None,
        "notes": "Core accounting courses required for the concentration.",
        "sort_order": 1,
        "courses": [
          {"subject": "ACCT", "catalog": "351", "title": "Intermediate Financial Accounting 1",  "credits": 3, "is_required": True},
          {"subject": "ACCT", "catalog": "361", "title": "Management Accounting",                "credits": 3, "is_required": True},
        ],
      },
      {
        "block_key": "acct_conc_complementary",
        "title": "Complementary Accounting Courses",
        "block_type": "group",
        "credits_needed": 9,
        "courses_needed": None,
        "group_name": "9 credits from Accounting Complementary Courses",
        "notes": "Select 3 courses (9 credits) from the following list to complete the concentration.",
        "sort_order": 2,
        "courses": [
          {"subject": "ACCT", "catalog": "352", "title": "Intermediate Financial Accounting 2",  "credits": 3, "is_required": False},
          {"subject": "ACCT", "catalog": "354", "title": "Financial Statement Analysis",         "credits": 3, "is_required": False},
          {"subject": "ACCT", "catalog": "362", "title": "Cost Accounting",                     "credits": 3, "is_required": False},
          {"subject": "ACCT", "catalog": "385", "title": "Principles of Taxation",              "credits": 3, "is_required": False},
          {"subject": "ACCT", "catalog": "401", "title": "Sustainability and Environmental Accounting", "credits": 3, "is_required": False},
          {"subject": "ACCT", "catalog": "434", "title": "Topics in Accounting 1",              "credits": 3, "is_required": False},
          {"subject": "ACCT", "catalog": "451", "title": "Data Analytics in Capital Market",    "credits": 3, "is_required": False},
          {"subject": "ACCT", "catalog": "452", "title": "Financial Reporting Valuation",       "credits": 3, "is_required": False},
          {"subject": "ACCT", "catalog": "453", "title": "Advanced Financial Accounting",       "credits": 3, "is_required": False},
          {"subject": "ACCT", "catalog": "463", "title": "Management Control",                  "credits": 3, "is_required": False},
          {"subject": "ACCT", "catalog": "475", "title": "Principles of Auditing",              "credits": 3, "is_required": False},
          {"subject": "ACCT", "catalog": "486", "title": "Business Taxation 2",                 "credits": 3, "is_required": False},
        ],
      },
    ],
  },


  # ══════════════════════════════════════════════════════════════════
  # FINANCE
  # ══════════════════════════════════════════════════════════════════
  {
    "program_key": "finance_major_bcom",
    "name": "Finance – Major (B.Com.)",
    "program_type": "major",
    "faculty": "Desautels Faculty of Management",
    "total_credits": 30,
    "description": (
      "The 30-credit Finance Major provides in-depth knowledge of finance theory, "
      "financial institutions, investment analysis, risk management, and applied "
      "techniques. Graduates typically pursue careers in investment and commercial "
      "banking, manufacturing and service firms, non-profit organizations, and "
      "non-financial firms."
    ),
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/management/programs/majors/finance-major-bcom/",
    "blocks": [
      {
        "block_key": "fine_major_required",
        "title": "Required Finance Courses",
        "block_type": "required",
        "credits_needed": 18,
        "courses_needed": None,
        "group_name": None,
        "notes": "All 6 courses (18 credits) are required.",
        "sort_order": 1,
        "courses": [
          {"subject": "FINE", "catalog": "342", "title": "Corporate Finance",         "credits": 3, "is_required": True},
          {"subject": "FINE", "catalog": "441", "title": "Investment Management",     "credits": 3, "is_required": True},
          {"subject": "FINE", "catalog": "443", "title": "Applied Corporate Finance", "credits": 3, "is_required": True},
          {"subject": "FINE", "catalog": "448", "title": "Financial Derivatives",     "credits": 3, "is_required": True},
          {"subject": "FINE", "catalog": "482", "title": "International Finance 1",   "credits": 3, "is_required": True},
          {"subject": "MGSC", "catalog": "372", "title": "Advanced Business Statistics", "credits": 3, "is_required": True},
        ],
      },
      {
        "block_key": "fine_major_complementary_fine",
        "title": "Complementary Finance Courses",
        "block_type": "group",
        "credits_needed": 12,
        "courses_needed": None,
        "group_name": "9–12 credits from undergraduate FINE courses + 0–3 credits from ACCT",
        "notes": (
          "9–12 credits from any undergraduate FINE courses. "
          "0–3 credits may come from the following ACCT courses."
        ),
        "sort_order": 2,
        "courses": [
          {"subject": "ACCT", "catalog": "351", "title": "Intermediate Financial Accounting 1",  "credits": 3, "is_required": False},
          {"subject": "ACCT", "catalog": "352", "title": "Intermediate Financial Accounting 2",  "credits": 3, "is_required": False},
          {"subject": "ACCT", "catalog": "354", "title": "Financial Statement Analysis",         "credits": 3, "is_required": False},
          {"subject": "ACCT", "catalog": "385", "title": "Principles of Taxation",               "credits": 3, "is_required": False},
        ],
      },
    ],
  },

  {
    "program_key": "finance_concentration_bcom",
    "name": "Finance – Concentration (B.Com.)",
    "program_type": "concentration",
    "faculty": "Desautels Faculty of Management",
    "total_credits": 15,
    "description": (
      "The Finance concentration provides an understanding of key concepts in finance "
      "theory, financial institutions, investment analysis, risk management, and "
      "applied techniques. Consists of 5 courses (15 credits) selected from "
      "undergraduate FINE offerings."
    ),
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/management/programs/concentrations/finance-concentration-bcom/",
    "blocks": [
      {
        "block_key": "fine_conc_required",
        "title": "Required Finance Courses",
        "block_type": "required",
        "credits_needed": 6,
        "courses_needed": None,
        "group_name": None,
        "notes": "Core required courses for the Finance concentration.",
        "sort_order": 1,
        "courses": [
          {"subject": "FINE", "catalog": "342", "title": "Corporate Finance",     "credits": 3, "is_required": True},
          {"subject": "FINE", "catalog": "441", "title": "Investment Management", "credits": 3, "is_required": True},
        ],
      },
      {
        "block_key": "fine_conc_complementary",
        "title": "Complementary Finance Courses",
        "block_type": "group",
        "credits_needed": 9,
        "courses_needed": None,
        "group_name": "9 credits from undergraduate FINE courses",
        "notes": "Select 3 additional courses (9 credits) from any undergraduate FINE courses.",
        "sort_order": 2,
        "courses": [
          {"subject": "FINE", "catalog": "443", "title": "Applied Corporate Finance",     "credits": 3, "is_required": False},
          {"subject": "FINE", "catalog": "448", "title": "Financial Derivatives",         "credits": 3, "is_required": False},
          {"subject": "FINE", "catalog": "451", "title": "Fixed Income Analysis",          "credits": 3, "is_required": False},
          {"subject": "FINE", "catalog": "460", "title": "Financial Analytics",            "credits": 3, "is_required": False},
          {"subject": "FINE", "catalog": "462", "title": "Real Estate Finance",           "credits": 3, "is_required": False},
          {"subject": "FINE", "catalog": "472", "title": "Fixed Income Securities",       "credits": 3, "is_required": False},
          {"subject": "FINE", "catalog": "482", "title": "International Finance 1",       "credits": 3, "is_required": False},
          {"subject": "FINE", "catalog": "484", "title": "International Finance 2",       "credits": 3, "is_required": False},
          {"subject": "FINE", "catalog": "488", "title": "Advanced Investment Analysis",  "credits": 3, "is_required": False},
        ],
      },
    ],
  },


  # ══════════════════════════════════════════════════════════════════
  # INVESTMENT MANAGEMENT HONOURS
  # ══════════════════════════════════════════════════════════════════
  {
    "program_key": "investment_management_honours_bcom",
    "name": "Investment Management – Honours (B.Com.)",
    "program_type": "honours",
    "faculty": "Desautels Faculty of Management",
    "total_credits": 45,
    "description": (
      "The Honours in Investment Management is a limited enrolment program by "
      "application only for students entering their U2 year. A minimum CGPA of "
      "3.3 is required to apply. To graduate, students must maintain a CGPA of "
      "3.00, a program GPA of 3.00, and earn a minimum grade of B- in all "
      "Honours courses. Students who do not satisfy Honours requirements may "
      "still receive a Major in Finance if the major requirements are met."
    ),
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/management/programs/honours/investment-management-honours-bcom/",
    "blocks": [
      {
        "block_key": "him_required",
        "title": "Required Honours Courses",
        "block_type": "required",
        "credits_needed": 27,
        "courses_needed": None,
        "group_name": None,
        "notes": (
          "All 9 courses (27 credits) are required. Minimum grade of B- in each. "
          "MGSC 372 (Advanced Business Statistics) is part of the expanded Management Core for this program."
        ),
        "sort_order": 1,
        "courses": [
          {"subject": "ACCT", "catalog": "354",  "title": "Financial Statement Analysis",                   "credits": 3, "is_required": True},
          {"subject": "FINE", "catalog": "342",  "title": "Corporate Finance",                              "credits": 3, "is_required": True},
          {"subject": "FINE", "catalog": "440D1","title": "Honours Investment Management Research Project 1","credits": 3, "is_required": True},
          {"subject": "FINE", "catalog": "441",  "title": "Investment Management",                          "credits": 3, "is_required": True},
          {"subject": "FINE", "catalog": "443",  "title": "Applied Corporate Finance",                      "credits": 3, "is_required": True},
          {"subject": "FINE", "catalog": "448",  "title": "Financial Derivatives",                          "credits": 3, "is_required": True},
          {"subject": "FINE", "catalog": "450D1","title": "Honours Investment Management Research Project 2","credits": 3, "is_required": True},
          {"subject": "FINE", "catalog": "451",  "title": "Fixed Income Analysis",                          "credits": 3, "is_required": True},
          {"subject": "FINE", "catalog": "482",  "title": "International Finance 1",                        "credits": 3, "is_required": True},
        ],
      },
      {
        "block_key": "him_quantitative",
        "title": "Quantitative Complementary Courses (6–9 credits)",
        "block_type": "group",
        "credits_needed": 9,
        "courses_needed": None,
        "group_name": "6–9 credits from Quantitative Courses",
        "notes": "Select 6–9 credits from this list.",
        "sort_order": 2,
        "courses": [
          {"subject": "ACCT", "catalog": "451", "title": "Data Analytics in Capital Market", "credits": 3, "is_required": False},
          {"subject": "ACCT", "catalog": "452", "title": "Financial Reporting Valuation",    "credits": 3, "is_required": False},
          {"subject": "FINE", "catalog": "449", "title": "Risk Management in Finance",       "credits": 3, "is_required": False},
          {"subject": "FINE", "catalog": "452", "title": "Applied Quantitative Finance",     "credits": 3, "is_required": False},
        ],
      },
      {
        "block_key": "him_industry_specialization",
        "title": "Industry Specialization Complementary Courses (6–9 credits)",
        "block_type": "group",
        "credits_needed": 9,
        "courses_needed": None,
        "group_name": "6–9 credits from Industry Specialization Courses",
        "notes": "Select 6–9 credits to complete 15 complementary credits total.",
        "sort_order": 3,
        "courses": [
          {"subject": "FINE", "catalog": "442", "title": "Capital Markets and Institutions",        "credits": 3, "is_required": False},
          {"subject": "FINE", "catalog": "444", "title": "Security Trading and Market Making",      "credits": 3, "is_required": False},
          {"subject": "FINE", "catalog": "445", "title": "Real Estate Finance",                     "credits": 3, "is_required": False},
          {"subject": "FINE", "catalog": "446", "title": "Behavioural Finance",                     "credits": 3, "is_required": False},
          {"subject": "FINE", "catalog": "447", "title": "Venture Capital and Entrepreneurial Finance","credits": 3, "is_required": False},
          {"subject": "FINE", "catalog": "456", "title": "Hedge Fund Strategies and Trading",       "credits": 3, "is_required": False},
          {"subject": "FINE", "catalog": "464", "title": "Pension Funds and Retirement Systems",    "credits": 3, "is_required": False},
          {"subject": "FINE", "catalog": "465", "title": "Sustainable Finance",                     "credits": 3, "is_required": False},
          {"subject": "FINE", "catalog": "477", "title": "Fintech for Business and Finance",        "credits": 3, "is_required": False},
          {"subject": "FINE", "catalog": "490", "title": "Mergers and Corporate Reorganizations",   "credits": 3, "is_required": False},
        ],
      },
    ],
  },


  # ══════════════════════════════════════════════════════════════════
  # MARKETING
  # ══════════════════════════════════════════════════════════════════
  {
    "program_key": "marketing_major_bcom",
    "name": "Marketing – Major (B.Com.)",
    "program_type": "major",
    "faculty": "Desautels Faculty of Management",
    "total_credits": 30,
    "description": (
      "The B.Com. Major in Marketing provides a strong background in marketing "
      "suitable for a wide variety of careers. The program emphasizes digital "
      "marketing, marketing analytics, brand management, advertising, innovation, "
      "and sales management."
    ),
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/management/programs/majors/marketing-major-bcom/",
    "blocks": [
      {
        "block_key": "mrkt_major_required",
        "title": "Required Marketing Courses",
        "block_type": "required",
        "credits_needed": 9,
        "courses_needed": None,
        "group_name": None,
        "notes": "All 3 courses (9 credits) are required.",
        "sort_order": 1,
        "courses": [
          {"subject": "MRKT", "catalog": "354", "title": "Marketing Strategy",     "credits": 3, "is_required": True},
          {"subject": "MRKT", "catalog": "451", "title": "Marketing Research",     "credits": 3, "is_required": True},
          {"subject": "MRKT", "catalog": "452", "title": "Consumer Behaviour",     "credits": 3, "is_required": True},
        ],
      },
      {
        "block_key": "mrkt_major_complementary",
        "title": "Complementary Marketing Courses",
        "block_type": "group",
        "credits_needed": 21,
        "courses_needed": None,
        "group_name": "21 credits from Complementary Marketing Courses",
        "notes": "Select 7 courses (21 credits) from the following list.",
        "sort_order": 2,
        "courses": [
          {"subject": "MRKT", "catalog": "351", "title": "Marketing and Society",               "credits": 3, "is_required": False},
          {"subject": "MRKT", "catalog": "355", "title": "Services Marketing",                  "credits": 3, "is_required": False},
          {"subject": "MRKT", "catalog": "357", "title": "Marketing Planning 1",                "credits": 3, "is_required": False},
          {"subject": "MRKT", "catalog": "365", "title": "New Products",                        "credits": 3, "is_required": False},
          {"subject": "MRKT", "catalog": "438", "title": "Brand Management",                    "credits": 3, "is_required": False},
          {"subject": "MRKT", "catalog": "440", "title": "Marketing Analytics",                 "credits": 3, "is_required": False},
          {"subject": "MRKT", "catalog": "453", "title": "Advertising and Media",               "credits": 3, "is_required": False},
          {"subject": "MRKT", "catalog": "459", "title": "Retail Management",                   "credits": 3, "is_required": False},
          {"subject": "MRKT", "catalog": "483", "title": "International Marketing Management",  "credits": 3, "is_required": False},
        ],
      },
    ],
  },

  {
    "program_key": "marketing_concentration_bcom",
    "name": "Marketing – Concentration (B.Com.)",
    "program_type": "concentration",
    "faculty": "Desautels Faculty of Management",
    "total_credits": 15,
    "description": (
      "The Marketing concentration prepares students for a wide variety of career "
      "opportunities in product management, advertising, sales management, "
      "marketing management, pricing, marketing research, distribution, and "
      "retailing. It balances theoretical fundamentals with practical application."
    ),
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/management/programs/concentrations/marketing-concentration-bcom/",
    "blocks": [
      {
        "block_key": "mrkt_conc_required",
        "title": "Required Marketing Courses",
        "block_type": "required",
        "credits_needed": 9,
        "courses_needed": None,
        "group_name": None,
        "notes": "All 3 courses (9 credits) are required.",
        "sort_order": 1,
        "courses": [
          {"subject": "MRKT", "catalog": "354", "title": "Marketing Strategy",  "credits": 3, "is_required": True},
          {"subject": "MRKT", "catalog": "451", "title": "Marketing Research",  "credits": 3, "is_required": True},
          {"subject": "MRKT", "catalog": "452", "title": "Consumer Behaviour",  "credits": 3, "is_required": True},
        ],
      },
      {
        "block_key": "mrkt_conc_complementary",
        "title": "Complementary Marketing Courses",
        "block_type": "group",
        "credits_needed": 6,
        "courses_needed": None,
        "group_name": "6 credits from Complementary Marketing Courses",
        "notes": "Select 2 courses (6 credits) from the following list.",
        "sort_order": 2,
        "courses": [
          {"subject": "MRKT", "catalog": "351", "title": "Marketing and Society",               "credits": 3, "is_required": False},
          {"subject": "MRKT", "catalog": "355", "title": "Services Marketing",                  "credits": 3, "is_required": False},
          {"subject": "MRKT", "catalog": "357", "title": "Marketing Planning 1",                "credits": 3, "is_required": False},
          {"subject": "MRKT", "catalog": "365", "title": "New Products",                        "credits": 3, "is_required": False},
          {"subject": "MRKT", "catalog": "434", "title": "Topics in Marketing 1",               "credits": 3, "is_required": False},
          {"subject": "MRKT", "catalog": "438", "title": "Brand Management",                    "credits": 3, "is_required": False},
          {"subject": "MRKT", "catalog": "440", "title": "Marketing Analytics",                 "credits": 3, "is_required": False},
          {"subject": "MRKT", "catalog": "453", "title": "Advertising and Media",               "credits": 3, "is_required": False},
          {"subject": "MRKT", "catalog": "455", "title": "Sales Management",                    "credits": 3, "is_required": False},
          {"subject": "MRKT", "catalog": "459", "title": "Retail Management",                   "credits": 3, "is_required": False},
          {"subject": "MRKT", "catalog": "483", "title": "International Marketing Management",  "credits": 3, "is_required": False},
        ],
      },
    ],
  },


  # ══════════════════════════════════════════════════════════════════
  # BUSINESS ANALYTICS
  # ══════════════════════════════════════════════════════════════════
  {
    "program_key": "business_analytics_major_bcom",
    "name": "Business Analytics – Major (B.Com.)",
    "program_type": "major",
    "faculty": "Desautels Faculty of Management",
    "total_credits": 30,
    "description": (
      "The Major in Business Analytics offers an interdisciplinary approach to "
      "the evolving field of management analytics with a strong emphasis on "
      "experiential learning. Designed to address the growing needs of "
      "organizations for business analytics, data science, and artificial "
      "intelligence, with a focus on managerial applications and state-of-the-art "
      "data analytics tools."
    ),
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/management/programs/majors/business-analytics-major-bcom/",
    "blocks": [
      {
        "block_key": "bana_major_required",
        "title": "Required Business Analytics Courses",
        "block_type": "required",
        "credits_needed": 9,
        "courses_needed": None,
        "group_name": None,
        "notes": "All 3 courses are required for the major.",
        "sort_order": 1,
        "courses": [
          {"subject": "INSY", "catalog": "336", "title": "Data Handling and Coding for Analytics",  "credits": 3, "is_required": True},
          {"subject": "INSY", "catalog": "446", "title": "Data Mining for Business Analytics",      "credits": 3, "is_required": True},
          {"subject": "MGSC", "catalog": "404", "title": "Foundations of Decision Analytics",       "credits": 3, "is_required": True},
        ],
      },
      {
        "block_key": "bana_major_el",
        "title": "Experiential Learning (3 credits)",
        "block_type": "group",
        "credits_needed": 3,
        "courses_needed": None,
        "group_name": "Experiential Learning — choose one",
        "notes": "3 credits of experiential learning (meets BCom EL requirement).",
        "sort_order": 2,
        "courses": [
          {"subject": "MGSC", "catalog": "483", "title": "Analytics-Based Community Project", "credits": 3, "is_required": False},
          {"subject": "RETL", "catalog": "407", "title": "Retail Management Project",         "credits": 3, "is_required": False},
        ],
      },
      {
        "block_key": "bana_major_analytics_stats",
        "title": "Analytics/Statistics Component (3–6 credits)",
        "block_type": "group",
        "credits_needed": 6,
        "courses_needed": None,
        "group_name": "3–6 credits from Analytics/Statistics Courses",
        "notes": "Select 3–6 credits from the following.",
        "sort_order": 3,
        "courses": [
          {"subject": "MGSC", "catalog": "401", "title": "Statistical Foundations of Data Analytics",   "credits": 3, "is_required": False},
          {"subject": "MGSC", "catalog": "416", "title": "Data-Driven Models for Operations Analytics", "credits": 3, "is_required": False},
        ],
      },
      {
        "block_key": "bana_major_technical",
        "title": "Technical Component (6–9 credits)",
        "block_type": "group",
        "credits_needed": 9,
        "courses_needed": None,
        "group_name": "6–9 credits from Technical Component",
        "notes": "Select 6–9 credits from INSY advanced courses.",
        "sort_order": 4,
        "courses": [
          {"subject": "INSY", "catalog": "437", "title": "Managing Data and Databases",          "credits": 3, "is_required": False},
          {"subject": "INSY", "catalog": "442", "title": "Data Analysis and Visualization",      "credits": 3, "is_required": False},
          {"subject": "INSY", "catalog": "463", "title": "Deep Learning for Business Analytics", "credits": 3, "is_required": False},
        ],
      },
      {
        "block_key": "bana_major_applied",
        "title": "Applied Analytics Component (3–9 credits)",
        "block_type": "group",
        "credits_needed": 9,
        "courses_needed": None,
        "group_name": "3–9 credits from Applied Analytics Electives",
        "notes": "Select from the following to complete 18 complementary credits total.",
        "sort_order": 5,
        "courses": [
          {"subject": "ACCT", "catalog": "451", "title": "Data Analytics in Capital Market",     "credits": 3, "is_required": False},
          {"subject": "BUSA", "catalog": "471", "title": "Artificial Intelligence Ethics for Business", "credits": 3, "is_required": False},
          {"subject": "FINE", "catalog": "460", "title": "Financial Analytics",                  "credits": 3, "is_required": False},
          {"subject": "INSY", "catalog": "448", "title": "Text and Social Media Analytics",      "credits": 3, "is_required": False},
          {"subject": "MRKT", "catalog": "440", "title": "Marketing Analytics",                  "credits": 3, "is_required": False},
          {"subject": "MRKT", "catalog": "442", "title": "Customer Analytics",                   "credits": 3, "is_required": False},
          {"subject": "ORGB", "catalog": "330", "title": "People Analytics",                     "credits": 3, "is_required": False},
        ],
      },
    ],
  },

  {
    "program_key": "business_analytics_concentration_bcom",
    "name": "Business Analytics – Concentration (B.Com.)",
    "program_type": "concentration",
    "faculty": "Desautels Faculty of Management",
    "total_credits": 15,
    "description": (
      "The Business Analytics concentration provides a foundation in management "
      "analytics, data science, and AI tools for business decision-making. "
      "Consists of 5 courses (15 credits) covering data preparation, analysis, "
      "visualization, and quantitative methods."
    ),
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/management/programs/concentrations/business-analytics-concentration-bcom/",
    "blocks": [
      {
        "block_key": "bana_conc_required",
        "title": "Required Business Analytics Course",
        "block_type": "required",
        "credits_needed": 3,
        "courses_needed": None,
        "group_name": None,
        "notes": "1 required course (3 credits).",
        "sort_order": 1,
        "courses": [
          {"subject": "INSY", "catalog": "336", "title": "Data Handling and Coding for Analytics", "credits": 3, "is_required": True},
        ],
      },
      {
        "block_key": "bana_conc_analytics_stats",
        "title": "Analytics/Statistics Component (3–6 credits)",
        "block_type": "group",
        "credits_needed": 6,
        "courses_needed": None,
        "group_name": "3–6 credits from Analytics/Statistics Courses",
        "notes": "Select 3–6 credits from MGSC 401 and MGSC 416.",
        "sort_order": 2,
        "courses": [
          {"subject": "MGSC", "catalog": "401", "title": "Statistical Foundations of Data Analytics",     "credits": 3, "is_required": False},
          {"subject": "MGSC", "catalog": "416", "title": "Data-Driven Models for Operations Analytics",   "credits": 3, "is_required": False},
        ],
      },
      {
        "block_key": "bana_conc_technical",
        "title": "Technical Analytics Component (3–6 credits)",
        "block_type": "group",
        "credits_needed": 6,
        "courses_needed": None,
        "group_name": "3–6 credits from Technical Component",
        "notes": "Select 3–6 credits from INSY 446 and MGSC 404.",
        "sort_order": 3,
        "courses": [
          {"subject": "INSY", "catalog": "446", "title": "Data Mining for Business Analytics",    "credits": 3, "is_required": False},
          {"subject": "MGSC", "catalog": "404", "title": "Foundations of Decision Analytics",     "credits": 3, "is_required": False},
        ],
      },
      {
        "block_key": "bana_conc_applied",
        "title": "Applied Analytics Electives (0–6 credits)",
        "block_type": "group",
        "credits_needed": 6,
        "courses_needed": None,
        "group_name": "0–6 credits from Applied Analytics Electives",
        "notes": (
          "Select 0–6 credits from the following list to reach 15 credits total. "
          "Total across all blocks must equal 15 credits."
        ),
        "sort_order": 4,
        "courses": [
          {"subject": "ACCT", "catalog": "451", "title": "Data Analytics in Capital Market",     "credits": 3, "is_required": False},
          {"subject": "BUSA", "catalog": "471", "title": "Artificial Intelligence Ethics for Business", "credits": 3, "is_required": False},
          {"subject": "FINE", "catalog": "460", "title": "Financial Analytics",                  "credits": 3, "is_required": False},
          {"subject": "INSY", "catalog": "442", "title": "Data Analysis and Visualization",      "credits": 3, "is_required": False},
          {"subject": "INSY", "catalog": "448", "title": "Text and Social Media Analytics",      "credits": 3, "is_required": False},
          {"subject": "INSY", "catalog": "463", "title": "Deep Learning for Business Analytics", "credits": 3, "is_required": False},
          {"subject": "MGSC", "catalog": "483", "title": "Analytics-Based Community Project",    "credits": 3, "is_required": False},
          {"subject": "MRKT", "catalog": "440", "title": "Marketing Analytics",                  "credits": 3, "is_required": False},
          {"subject": "MRKT", "catalog": "442", "title": "Customer Analytics",                   "credits": 3, "is_required": False},
          {"subject": "ORGB", "catalog": "330", "title": "People Analytics",                     "credits": 3, "is_required": False},
        ],
      },
    ],
  },


  # ══════════════════════════════════════════════════════════════════
  # STRATEGIC MANAGEMENT
  # ══════════════════════════════════════════════════════════════════
  {
    "program_key": "strategic_management_major_bcom",
    "name": "Strategic Management – Major (B.Com.)",
    "program_type": "major",
    "faculty": "Desautels Faculty of Management",
    "total_credits": 30,
    "description": (
      "The Strategic Management Major combines traditional topics in strategic "
      "management — competition and globalization — with attention to pressing "
      "social and environmental challenges. Students are encouraged to consider "
      "strategy formation for large corporations, small businesses, and social "
      "enterprises. Anticipated careers include management consulting, business "
      "development, strategic planning in multinationals, NGOs, and governments."
    ),
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/management/programs/majors/strategic-management-major-bcom/",
    "blocks": [
      {
        "block_key": "stra_major_pool1",
        "title": "Pool 1: Global Strategy Courses (9–15 credits)",
        "block_type": "group",
        "credits_needed": 15,
        "courses_needed": None,
        "group_name": "9–15 credits from Pool 1: Global Strategy MGPO Courses",
        "notes": (
          "No fixed required courses beyond the Management Core. "
          "Select 9–15 credits from this pool and 9–15 from Pool 2, with 0–12 from Pool 3, "
          "to total 30 credits."
        ),
        "sort_order": 1,
        "courses": [
          {"subject": "MGPO", "catalog": "383", "title": "International Business Policy",            "credits": 3, "is_required": False},
          {"subject": "MGPO", "catalog": "445", "title": "Industry Analysis and Competitive Strategy","credits": 3, "is_required": False},
          {"subject": "MGPO", "catalog": "460", "title": "Managing Innovation",                      "credits": 3, "is_required": False},
          {"subject": "MGPO", "catalog": "469", "title": "Managing Globalization",                   "credits": 3, "is_required": False},
          {"subject": "MGPO", "catalog": "470", "title": "Strategy and Organization",                "credits": 3, "is_required": False},
        ],
      },
      {
        "block_key": "stra_major_pool2",
        "title": "Pool 2: Society & Sustainability Courses (9–15 credits)",
        "block_type": "group",
        "credits_needed": 15,
        "courses_needed": None,
        "group_name": "9–15 credits from Pool 2: Society & Sustainability MGPO Courses",
        "notes": "Select 9–15 credits from this pool to complement Pool 1 selections.",
        "sort_order": 2,
        "courses": [
          {"subject": "MGPO", "catalog": "365", "title": "Business-Government Relations",           "credits": 3, "is_required": False},
          {"subject": "MGPO", "catalog": "438", "title": "Social Entrepreneurship and Innovation",  "credits": 3, "is_required": False},
          {"subject": "MGPO", "catalog": "440", "title": "Strategies for Sustainability",           "credits": 3, "is_required": False},
          {"subject": "MGPO", "catalog": "450", "title": "Ethics in Management",                    "credits": 3, "is_required": False},
          {"subject": "MGPO", "catalog": "475", "title": "Strategies for Developing Countries",     "credits": 3, "is_required": False},
          {"subject": "MGPO", "catalog": "485", "title": "Emerging Technologies: Organizing and Societal Stakes", "credits": 3, "is_required": False},
        ],
      },
      {
        "block_key": "stra_major_pool3",
        "title": "Pool 3: Interdisciplinary Electives (0–12 credits)",
        "block_type": "group",
        "credits_needed": 12,
        "courses_needed": None,
        "group_name": "0–12 credits from Pool 3: Approved Electives",
        "notes": "Select 0–12 credits from approved courses in other disciplines.",
        "sort_order": 3,
        "courses": [
          {"subject": "AGRI", "catalog": "411",   "title": "Global Issues on Development, Food and Agriculture", "credits": 3, "is_required": False},
          {"subject": "ANTH", "catalog": "212",   "title": "Anthropology of Development",          "credits": 3, "is_required": False},
          {"subject": "BUSA", "catalog": "300",   "title": "Case Analysis and Presentation",        "credits": 3, "is_required": False},
          {"subject": "BUSA", "catalog": "391",   "title": "International Business Law",            "credits": 3, "is_required": False},
          {"subject": "ECON", "catalog": "305",   "title": "Industrial Organization",               "credits": 3, "is_required": False},
          {"subject": "ECON", "catalog": "313",   "title": "Economic Development 1",                "credits": 3, "is_required": False},
          {"subject": "ECON", "catalog": "314",   "title": "Economic Development 2",                "credits": 3, "is_required": False},
          {"subject": "INTD", "catalog": "200",   "title": "Introduction to International Development", "credits": 3, "is_required": False},
          {"subject": "MGPO", "catalog": "362",   "title": "Fundamentals of Entrepreneurship",      "credits": 3, "is_required": False},
          {"subject": "MGPO", "catalog": "430",   "title": "Practicum in Not for Profit Consulting","credits": 3, "is_required": False},
          {"subject": "MGPO", "catalog": "433",   "title": "Topics in Social Business and Enterprise","credits": 3, "is_required": False},
          {"subject": "MGPO", "catalog": "434",   "title": "Topics in Policy 1",                    "credits": 3, "is_required": False},
          {"subject": "MGPO", "catalog": "435",   "title": "The Origins of Capitalism",             "credits": 3, "is_required": False},
          {"subject": "ORGB", "catalog": "380",   "title": "Cross Cultural Management",             "credits": 3, "is_required": False},
        ],
      },
    ],
  },

  {
    "program_key": "strategic_management_global_concentration_bcom",
    "name": "Strategic Management – Global Strategy Concentration (B.Com.)",
    "program_type": "concentration",
    "faculty": "Desautels Faculty of Management",
    "total_credits": 15,
    "description": (
      "One of two options in the Strategic Management Concentration. The Global "
      "Strategy option provides skills to understand contemporary businesses in a "
      "global context and to explore the implications of business decisions for "
      "society and the environment. Conveys tools to understand industry structures "
      "and competitive dynamics globally."
    ),
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/management/programs/concentrations/strategic-management-global-concentration-bcom/",
    "blocks": [
      {
        "block_key": "stra_global_primary",
        "title": "Primary Global Strategy Courses (9–15 credits)",
        "block_type": "group",
        "credits_needed": 15,
        "courses_needed": None,
        "group_name": "9–15 credits from Primary MGPO Courses",
        "notes": (
          "No single required course. Select 9–15 credits from this list and 0–6 credits "
          "from the electives list below to total 15 credits."
        ),
        "sort_order": 1,
        "courses": [
          {"subject": "MGPO", "catalog": "383", "title": "International Business Policy",            "credits": 3, "is_required": False},
          {"subject": "MGPO", "catalog": "445", "title": "Industry Analysis and Competitive Strategy","credits": 3, "is_required": False},
          {"subject": "MGPO", "catalog": "460", "title": "Managing Innovation",                      "credits": 3, "is_required": False},
          {"subject": "MGPO", "catalog": "469", "title": "Managing Globalization",                   "credits": 3, "is_required": False},
          {"subject": "MGPO", "catalog": "470", "title": "Strategy and Organization",                "credits": 3, "is_required": False},
        ],
      },
      {
        "block_key": "stra_global_electives",
        "title": "Elective Courses (0–6 credits)",
        "block_type": "group",
        "credits_needed": 6,
        "courses_needed": None,
        "group_name": "0–6 credits from Approved Electives",
        "notes": "Select 0–6 credits from this list to reach 15 credits total.",
        "sort_order": 2,
        "courses": [
          {"subject": "BUSA", "catalog": "300", "title": "Case Analysis and Presentation",           "credits": 3, "is_required": False},
          {"subject": "BUSA", "catalog": "391", "title": "International Business Law",               "credits": 3, "is_required": False},
          {"subject": "ECON", "catalog": "305", "title": "Industrial Organization",                  "credits": 3, "is_required": False},
          {"subject": "MGPO", "catalog": "362", "title": "Fundamentals of Entrepreneurship",         "credits": 3, "is_required": False},
          {"subject": "MGPO", "catalog": "434", "title": "Topics in Policy 1",                       "credits": 3, "is_required": False},
          {"subject": "MGPO", "catalog": "435", "title": "The Origins of Capitalism",                "credits": 3, "is_required": False},
          {"subject": "MGPO", "catalog": "438", "title": "Social Entrepreneurship and Innovation",   "credits": 3, "is_required": False},
          {"subject": "MGPO", "catalog": "440", "title": "Strategies for Sustainability",            "credits": 3, "is_required": False},
          {"subject": "MGPO", "catalog": "450", "title": "Ethics in Management",                     "credits": 3, "is_required": False},
          {"subject": "MGPO", "catalog": "475", "title": "Strategies for Developing Countries",      "credits": 3, "is_required": False},
          {"subject": "MGPO", "catalog": "485", "title": "Emerging Technologies: Organizing and Societal Stakes", "credits": 3, "is_required": False},
          {"subject": "ORGB", "catalog": "380", "title": "Cross Cultural Management",                "credits": 3, "is_required": False},
        ],
      },
    ],
  },

  {
    "program_key": "strategic_management_social_concentration_bcom",
    "name": "Strategic Management – Social Business & Enterprise Concentration (B.Com.)",
    "program_type": "concentration",
    "faculty": "Desautels Faculty of Management",
    "total_credits": 15,
    "description": (
      "One of two options in the Strategic Management Concentration. The Social "
      "Business & Enterprise option focuses on concepts related to social "
      "entrepreneurship, social innovation, and sustainability. Students explore "
      "how market systems can be leveraged to create social value."
    ),
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/management/programs/concentrations/strategic-management-social-business-enterprise-concentration-bcom/",
    "blocks": [
      {
        "block_key": "stra_social_primary",
        "title": "Primary Courses (9–15 credits)",
        "block_type": "group",
        "credits_needed": 15,
        "courses_needed": None,
        "group_name": "Primary MGPO Courses (9–15 credits)",
        "notes": (
          "No fixed required courses. Select 9–15 credits from this list and 0–6 credits "
          "from the secondary list to total 15 credits. Max 3 credits at the 200 level overall."
        ),
        "sort_order": 1,
        "courses": [
          {"subject": "MGPO", "catalog": "365", "title": "Business-Government Relations",              "credits": 3, "is_required": False},
          {"subject": "MGPO", "catalog": "438", "title": "Social Entrepreneurship and Innovation",     "credits": 3, "is_required": False},
          {"subject": "MGPO", "catalog": "440", "title": "Strategies for Sustainability",              "credits": 3, "is_required": False},
          {"subject": "MGPO", "catalog": "450", "title": "Ethics in Management",                       "credits": 3, "is_required": False},
          {"subject": "MGPO", "catalog": "475", "title": "Strategies for Developing Countries",        "credits": 3, "is_required": False},
          {"subject": "MGPO", "catalog": "485", "title": "Emerging Technologies: Organizing and Societal Stakes", "credits": 3, "is_required": False},
        ],
      },
      {
        "block_key": "stra_social_secondary",
        "title": "Secondary / Interdisciplinary Courses (0–6 credits)",
        "block_type": "group",
        "credits_needed": None,
        "courses_needed": None,
        "group_name": "Secondary Interdisciplinary Courses (0–6 credits)",
        "notes": "Select 0–6 credits from this list (max 3 credits at the 200 level across the full concentration).",
        "sort_order": 2,
        "courses": [
          {"subject": "AGRI", "catalog": "411", "title": "Global Issues on Development, Food and Agriculture", "credits": 3, "is_required": False},
          {"subject": "ANTH", "catalog": "212", "title": "Anthropology of Development",               "credits": 3, "is_required": False},
          {"subject": "BUSA", "catalog": "300", "title": "Case Analysis and Presentation",            "credits": 3, "is_required": False},
          {"subject": "ECON", "catalog": "313", "title": "Economic Development 1",                    "credits": 3, "is_required": False},
          {"subject": "ECON", "catalog": "314", "title": "Economic Development 2",                    "credits": 3, "is_required": False},
          {"subject": "INTD", "catalog": "200", "title": "Introduction to International Development", "credits": 3, "is_required": False},
          {"subject": "MGPO", "catalog": "430", "title": "Practicum in Not for Profit Consulting",    "credits": 3, "is_required": False},
          {"subject": "MGPO", "catalog": "433", "title": "Topics in Social Business and Enterprise",  "credits": 3, "is_required": False},
          {"subject": "MGPO", "catalog": "435", "title": "The Origins of Capitalism",                 "credits": 3, "is_required": False},
          {"subject": "MGPO", "catalog": "460", "title": "Managing Innovation",                       "credits": 3, "is_required": False},
        ],
      },
    ],
  },


  # ══════════════════════════════════════════════════════════════════
  # INFORMATION TECHNOLOGY MANAGEMENT
  # ══════════════════════════════════════════════════════════════════
  {
    "program_key": "it_management_major_bcom",
    "name": "Information Technology Management – Major (B.Com.)",
    "program_type": "major",
    "faculty": "Desautels Faculty of Management",
    "total_credits": 30,
    "description": (
      "The BCom Major in Information Technology Management combines theoretical "
      "concepts, hands-on tools, and case studies to identify business problems, "
      "analyze business processes, and develop/implement information systems. "
      "Covers strategic planning in IT, systems analysis and design, web-based "
      "businesses, and managing organizational resistance to IT-driven change."
    ),
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/management/programs/majors/information-technology-management-major-bcom/",
    "blocks": [
      {
        "block_key": "itm_major_required",
        "title": "Required IT Management Courses",
        "block_type": "required",
        "credits_needed": 21,
        "courses_needed": None,
        "group_name": None,
        "notes": "7 required courses (21 credits). U2/U3 restrictions apply to some courses.",
        "sort_order": 1,
        "courses": [
          {"subject": "INSY", "catalog": "331", "title": "Managing and Organizing Digital Technology",   "credits": 3, "is_required": True},
          {"subject": "INSY", "catalog": "333", "title": "Systems Analysis and Modeling",                "credits": 3, "is_required": True},
          {"subject": "INSY", "catalog": "334", "title": "Design Thinking for User Experience",          "credits": 3, "is_required": True},
          {"subject": "INSY", "catalog": "341", "title": "Developing Business Applications",             "credits": 3, "is_required": True},
          {"subject": "INSY", "catalog": "431", "title": "IT Implementation Management",                 "credits": 3, "is_required": True},
          {"subject": "INSY", "catalog": "437", "title": "Managing Data and Databases",                  "credits": 3, "is_required": True},
          {"subject": "INSY", "catalog": "450", "title": "Information Systems Project Management",       "credits": 3, "is_required": True},
        ],
      },
      {
        "block_key": "itm_major_primary_complementary",
        "title": "Primary Complementary IT Courses (3–9 credits)",
        "block_type": "group",
        "credits_needed": 9,
        "courses_needed": None,
        "group_name": "3–9 credits from Primary Complementary Courses",
        "notes": "Select 3–9 credits from this list.",
        "sort_order": 2,
        "courses": [
          {"subject": "INSY", "catalog": "339", "title": "Digital Consulting",             "credits": 3, "is_required": False},
          {"subject": "INSY", "catalog": "432", "title": "Digital Business Models",        "credits": 3, "is_required": False},
          {"subject": "INSY", "catalog": "434", "title": "Topics in Information Systems 1","credits": 3, "is_required": False},
          {"subject": "INSY", "catalog": "440", "title": "E-Business",                     "credits": 3, "is_required": False},
          {"subject": "INSY", "catalog": "442", "title": "Data Analysis and Visualization","credits": 3, "is_required": False},
          {"subject": "INSY", "catalog": "455", "title": "Technology and Innovation for Sustainability", "credits": 3, "is_required": False},
        ],
      },
      {
        "block_key": "itm_major_analytics_complementary",
        "title": "Analytics Complementary Courses (0–6 credits)",
        "block_type": "group",
        "credits_needed": 6,
        "courses_needed": None,
        "group_name": "0–6 credits from Analytics Electives",
        "notes": "Select 0–6 credits from this list to reach 9 total complementary credits.",
        "sort_order": 3,
        "courses": [
          {"subject": "INSY", "catalog": "336", "title": "Data Handling and Coding for Analytics",  "credits": 3, "is_required": False},
          {"subject": "INSY", "catalog": "446", "title": "Data Mining for Business Analytics",      "credits": 3, "is_required": False},
          {"subject": "INSY", "catalog": "448", "title": "Text and Social Media Analytics",         "credits": 3, "is_required": False},
          {"subject": "INSY", "catalog": "463", "title": "Deep Learning for Business Analytics",    "credits": 3, "is_required": False},
        ],
      },
    ],
  },

  {
    "program_key": "it_management_concentration_bcom",
    "name": "Information Technology Management – Concentration (B.Com.)",
    "program_type": "concentration",
    "faculty": "Desautels Faculty of Management",
    "total_credits": 15,
    "description": (
      "The IT Management concentration focuses on how organizations leverage "
      "the power of IT: navigating the digital economy, analyzing and selecting "
      "technology solutions, and handling and analyzing data. 5 courses (15 credits)."
    ),
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/management/programs/concentrations/information-technology-management-concentration-bcom/",
    "blocks": [
      {
        "block_key": "itm_conc_required",
        "title": "Required IT Management Course",
        "block_type": "required",
        "credits_needed": 3,
        "courses_needed": None,
        "group_name": None,
        "notes": "1 required course (3 credits). Prerequisite: MGCR 331.",
        "sort_order": 1,
        "courses": [
          {"subject": "INSY", "catalog": "333", "title": "Systems Analysis and Modeling", "credits": 3, "is_required": True},
        ],
      },
      {
        "block_key": "itm_conc_primary",
        "title": "Primary IT Electives (6–12 credits)",
        "block_type": "group",
        "credits_needed": 12,
        "courses_needed": None,
        "group_name": "6–12 credits from Primary IT Electives",
        "notes": "Select 6–12 credits from this list (U2/U3 restrictions apply to some).",
        "sort_order": 2,
        "courses": [
          {"subject": "INSY", "catalog": "331", "title": "Managing and Organizing Digital Technology", "credits": 3, "is_required": False},
          {"subject": "INSY", "catalog": "334", "title": "Design Thinking for User Experience",        "credits": 3, "is_required": False},
          {"subject": "INSY", "catalog": "339", "title": "Digital Consulting",                         "credits": 3, "is_required": False},
          {"subject": "INSY", "catalog": "341", "title": "Developing Business Applications",           "credits": 3, "is_required": False},
          {"subject": "INSY", "catalog": "431", "title": "IT Implementation Management",               "credits": 3, "is_required": False},
          {"subject": "INSY", "catalog": "432", "title": "Digital Business Models",                    "credits": 3, "is_required": False},
          {"subject": "INSY", "catalog": "434", "title": "Topics in Information Systems 1",            "credits": 3, "is_required": False},
          {"subject": "INSY", "catalog": "437", "title": "Managing Data and Databases",                "credits": 3, "is_required": False},
          {"subject": "INSY", "catalog": "440", "title": "E-Business",                                 "credits": 3, "is_required": False},
          {"subject": "INSY", "catalog": "442", "title": "Data Analysis and Visualization",            "credits": 3, "is_required": False},
          {"subject": "INSY", "catalog": "450", "title": "Information Systems Project Management",     "credits": 3, "is_required": False},
          {"subject": "INSY", "catalog": "455", "title": "Technology and Innovation for Sustainability","credits": 3, "is_required": False},
        ],
      },
      {
        "block_key": "itm_conc_analytics",
        "title": "Analytics Electives (0–6 credits)",
        "block_type": "group",
        "credits_needed": 6,
        "courses_needed": None,
        "group_name": "0–6 credits from Analytics Electives",
        "notes": "Select 0–6 credits from this list to total 15 credits across all blocks.",
        "sort_order": 3,
        "courses": [
          {"subject": "INSY", "catalog": "336", "title": "Data Handling and Coding for Analytics",  "credits": 3, "is_required": False},
          {"subject": "INSY", "catalog": "446", "title": "Data Mining for Business Analytics",      "credits": 3, "is_required": False},
          {"subject": "INSY", "catalog": "448", "title": "Text and Social Media Analytics",         "credits": 3, "is_required": False},
          {"subject": "INSY", "catalog": "463", "title": "Deep Learning for Business Analytics",    "credits": 3, "is_required": False},
        ],
      },
    ],
  },


  # ══════════════════════════════════════════════════════════════════
  # ORGANIZATIONAL BEHAVIOUR & HUMAN RESOURCES
  # ══════════════════════════════════════════════════════════════════
  {
    "program_key": "organizational_behaviour_hr_major_bcom",
    "name": "Organizational Behaviour and Human Resources – Major (B.Com.)",
    "program_type": "major",
    "faculty": "Desautels Faculty of Management",
    "total_credits": 30,
    "description": (
      "The OB & HR Major enables students to analyze and influence patterns of "
      "action in groups and organizations. Required courses in leadership, human "
      "resource management, and team management introduce management concepts at "
      "multiple organizational levels. Students also specialize in one social "
      "science discipline: psychology, sociology, or anthropology."
    ),
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/management/programs/majors/organizational-behaviour-human-resources-major-bcom/",
    "blocks": [
      {
        "block_key": "obhr_major_required",
        "title": "Required OB & HR Course (in Management Core)",
        "block_type": "required",
        "credits_needed": 3,
        "courses_needed": None,
        "group_name": None,
        "notes": (
          "ORGB 423 is counted as part of the expanded Management Core for this major "
          "(15 core courses = 45 credits). Students complete it in the core."
        ),
        "sort_order": 1,
        "courses": [
          {"subject": "ORGB", "catalog": "423", "title": "Human Resources Management", "credits": 3, "is_required": True},
        ],
      },
      {
        "block_key": "obhr_major_orgb_complementary",
        "title": "Complementary ORGB Courses (18 credits)",
        "block_type": "group",
        "credits_needed": 18,
        "courses_needed": None,
        "group_name": "18 credits from Complementary Organizational Behaviour Courses",
        "notes": "Select 18 credits from the following ORGB electives.",
        "sort_order": 2,
        "courses": [
          {"subject": "ORGB", "catalog": "321", "title": "Leadership",                               "credits": 3, "is_required": False},
          {"subject": "ORGB", "catalog": "325", "title": "Negotiations and Conflict Resolution",      "credits": 3, "is_required": False},
          {"subject": "ORGB", "catalog": "330", "title": "People Analytics",                          "credits": 3, "is_required": False},
          {"subject": "ORGB", "catalog": "380", "title": "Cross Cultural Management",                 "credits": 3, "is_required": False},
          {"subject": "ORGB", "catalog": "401", "title": "Leadership Practicum in Social Sector",     "credits": 3, "is_required": False},
          {"subject": "ORGB", "catalog": "409", "title": "Organizational Research Methods",           "credits": 3, "is_required": False},
          {"subject": "ORGB", "catalog": "420", "title": "Managing Organizational Teams",             "credits": 3, "is_required": False},
          {"subject": "ORGB", "catalog": "421", "title": "Managing Organizational Change",            "credits": 3, "is_required": False},
          {"subject": "ORGB", "catalog": "434", "title": "Topics in Organizational Behaviour 1",      "credits": 3, "is_required": False},
          {"subject": "ORGB", "catalog": "440", "title": "Career Theory and Development",             "credits": 3, "is_required": False},
          {"subject": "ORGB", "catalog": "525", "title": "Compensation Management",                   "credits": 3, "is_required": False},
        ],
      },
      {
        "block_key": "obhr_major_social_science",
        "title": "Social Science Discipline Component",
        "block_type": "group",
        "credits_needed": 9,
        "courses_needed": None,
        "group_name": "9 credits from PSYC, SOCI, ANTH, or INDR (300–400 level)",
        "notes": (
          "9 credits at the 300 or 400 level of PSYC, SOCI, ANTH, or INDR courses "
          "with permission of the offering unit. Focusing on one discipline is "
          "encouraged but not required."
        ),
        "sort_order": 3,
        "courses": [
          {"subject": "PSYC", "catalog": "305", "title": "Human Learning",                           "credits": 3, "is_required": False},
          {"subject": "PSYC", "catalog": "307", "title": "Personality",                              "credits": 3, "is_required": False},
          {"subject": "PSYC", "catalog": "315", "title": "Computational Psychology",                 "credits": 3, "is_required": False},
          {"subject": "SOCI", "catalog": "350", "title": "Work and Organizations",                   "credits": 3, "is_required": False},
          {"subject": "SOCI", "catalog": "361", "title": "Sociology of Organizations",               "credits": 3, "is_required": False},
          {"subject": "ANTH", "catalog": "320", "title": "Culture and Organization",                 "credits": 3, "is_required": False},
          {"subject": "INDR", "catalog": "294", "title": "Introduction to Labour-Management Relations", "credits": 3, "is_required": False},
        ],
      },
    ],
  },

  {
    "program_key": "organizational_behaviour_concentration_bcom",
    "name": "Organizational Behaviour – Concentration (B.Com.)",
    "program_type": "concentration",
    "faculty": "Desautels Faculty of Management",
    "total_credits": 15,
    "description": (
      "The OB concentration increases students' awareness of behavioural issues in "
      "job and organizational settings, and prepares them for graduate study in "
      "the behavioural sciences or careers in general management or human resource "
      "management. 5 courses (15 credits)."
    ),
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/management/programs/concentrations/organizational-behaviour-concentration-bcom/",
    "blocks": [
      {
        "block_key": "ob_conc_required",
        "title": "Required OB Courses",
        "block_type": "required",
        "credits_needed": 9,
        "courses_needed": None,
        "group_name": None,
        "notes": "3 required courses (9 credits).",
        "sort_order": 1,
        "courses": [
          {"subject": "ORGB", "catalog": "321", "title": "Leadership",                    "credits": 3, "is_required": True},
          {"subject": "ORGB", "catalog": "420", "title": "Managing Organizational Teams", "credits": 3, "is_required": True},
          {"subject": "ORGB", "catalog": "423", "title": "Human Resources Management",   "credits": 3, "is_required": True},
        ],
      },
      {
        "block_key": "ob_conc_complementary",
        "title": "Complementary OB Courses",
        "block_type": "group",
        "credits_needed": 6,
        "courses_needed": None,
        "group_name": "6 credits from Complementary ORGB Courses",
        "notes": "Select 2 courses (6 credits) from the following list.",
        "sort_order": 2,
        "courses": [
          {"subject": "ORGB", "catalog": "325", "title": "Negotiations and Conflict Resolution",   "credits": 3, "is_required": False},
          {"subject": "ORGB", "catalog": "330", "title": "People Analytics",                       "credits": 3, "is_required": False},
          {"subject": "ORGB", "catalog": "380", "title": "Cross Cultural Management",              "credits": 3, "is_required": False},
          {"subject": "ORGB", "catalog": "401", "title": "Leadership Practicum in Social Sector",  "credits": 3, "is_required": False},
          {"subject": "ORGB", "catalog": "409", "title": "Organizational Research Methods",        "credits": 3, "is_required": False},
          {"subject": "ORGB", "catalog": "421", "title": "Managing Organizational Change",         "credits": 3, "is_required": False},
          {"subject": "ORGB", "catalog": "434", "title": "Topics in Organizational Behaviour 1",   "credits": 3, "is_required": False},
          {"subject": "ORGB", "catalog": "440", "title": "Career Theory and Development",          "credits": 3, "is_required": False},
          {"subject": "ORGB", "catalog": "525", "title": "Compensation Management",                "credits": 3, "is_required": False},
        ],
      },
    ],
  },


  # ══════════════════════════════════════════════════════════════════
  # LABOUR-MANAGEMENT RELATIONS & HUMAN RESOURCES
  # ══════════════════════════════════════════════════════════════════
  {
    "program_key": "labour_management_concentration_bcom",
    "name": "Labour-Management Relations and Human Resources – Concentration (B.Com.)",
    "program_type": "concentration",
    "faculty": "Desautels Faculty of Management",
    "total_credits": 15,
    "description": (
      "The Labour-Management Relations & HR concentration introduces the theory "
      "and practice of labour relations, employment law, and human resource "
      "management in Canadian and comparative contexts. 5 courses (15 credits)."
    ),
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/management/programs/concentrations/labour-management-relations-human-resources-concentration-bcom/",
    "blocks": [
      {
        "block_key": "lmhr_conc_required",
        "title": "Required Labour-Management Courses",
        "block_type": "required",
        "credits_needed": 9,
        "courses_needed": None,
        "group_name": None,
        "notes": "3 required courses (9 credits).",
        "sort_order": 1,
        "courses": [
          {"subject": "INDR", "catalog": "294", "title": "Introduction to Labour-Management Relations", "credits": 3, "is_required": True},
          {"subject": "INDR", "catalog": "496", "title": "Collective Bargaining",                       "credits": 3, "is_required": True},
          {"subject": "ORGB", "catalog": "423", "title": "Human Resources Management",                  "credits": 3, "is_required": True},
        ],
      },
      {
        "block_key": "lmhr_conc_complementary",
        "title": "Complementary Labour-Management Courses",
        "block_type": "group",
        "credits_needed": 6,
        "courses_needed": None,
        "group_name": "6 credits from Complementary INDR/ORGB Courses",
        "notes": "Select 2 courses (6 credits) from the following list.",
        "sort_order": 2,
        "courses": [
          {"subject": "INDR", "catalog": "459", "title": "Comparative Employment Relations",           "credits": 3, "is_required": False},
          {"subject": "INDR", "catalog": "492", "title": "Globalization and Labour Policy",            "credits": 3, "is_required": False},
          {"subject": "INDR", "catalog": "494", "title": "Labour Law",                                 "credits": 3, "is_required": False},
          {"subject": "ORGB", "catalog": "321", "title": "Leadership",                                 "credits": 3, "is_required": False},
          {"subject": "ORGB", "catalog": "325", "title": "Negotiations and Conflict Resolution",       "credits": 3, "is_required": False},
          {"subject": "ORGB", "catalog": "330", "title": "People Analytics",                           "credits": 3, "is_required": False},
          {"subject": "ORGB", "catalog": "401", "title": "Leadership Practicum in Social Sector",      "credits": 3, "is_required": False},
          {"subject": "ORGB", "catalog": "409", "title": "Organizational Research Methods",            "credits": 3, "is_required": False},
          {"subject": "ORGB", "catalog": "421", "title": "Managing Organizational Change",             "credits": 3, "is_required": False},
          {"subject": "ORGB", "catalog": "440", "title": "Career Theory and Development",              "credits": 3, "is_required": False},
          {"subject": "ORGB", "catalog": "525", "title": "Compensation Management",                    "credits": 3, "is_required": False},
        ],
      },
    ],
  },


  # ══════════════════════════════════════════════════════════════════
  # LABOUR-MANAGEMENT RELATIONS & HUMAN RESOURCES – MAJOR
  # ══════════════════════════════════════════════════════════════════
  {
    "program_key": "labour_management_major_bcom",
    "name": "Labour-Management Relations and Human Resources – Major (B.Com.)",
    "program_type": "major",
    "faculty": "Desautels Faculty of Management",
    "total_credits": 30,
    "description": (
      "The BCom Major in Labour-Management Relations and Human Resources provides "
      "an in-depth understanding of the theory and practice of labour relations, "
      "employment law, collective bargaining, and human resource management in "
      "Canadian and comparative contexts. Students complete required INDR and ORGB "
      "courses plus complementary electives for a total of 30 credits."
    ),
    "ecalendar_url": "https://www.mcgill.ca/study/2024-2025/faculties/desautels/undergraduate/programs/bachelor-commerce-bcom-major-labour-management-relations-and-human-resources",
    "blocks": [
      {
        "block_key": "lmhr_major_required",
        "title": "Required Labour-Management Courses",
        "block_type": "required",
        "credits_needed": 12,
        "courses_needed": None,
        "group_name": None,
        "notes": "4 required courses (12 credits).",
        "sort_order": 1,
        "courses": [
          {"subject": "INDR", "catalog": "294", "title": "Introduction to Labour-Management Relations", "credits": 3, "is_required": True},
          {"subject": "INDR", "catalog": "494", "title": "Labour Law",                                  "credits": 3, "is_required": True},
          {"subject": "INDR", "catalog": "496", "title": "Collective Bargaining",                       "credits": 3, "is_required": True},
          {"subject": "ORGB", "catalog": "423", "title": "Human Resources Management",                  "credits": 3, "is_required": True},
        ],
      },
      {
        "block_key": "lmhr_major_complementary",
        "title": "Complementary Labour-Management Courses",
        "block_type": "group",
        "credits_needed": 18,
        "courses_needed": None,
        "group_name": "18 credits from Complementary INDR/ORGB Courses",
        "notes": "Select 6 courses (18 credits) from the following list.",
        "sort_order": 2,
        "courses": [
          {"subject": "INDR", "catalog": "459", "title": "Comparative Employment Relations",            "credits": 3, "is_required": False},
          {"subject": "INDR", "catalog": "492", "title": "Globalization and Labour Policy",             "credits": 3, "is_required": False},
          {"subject": "ORGB", "catalog": "321", "title": "Leadership",                                  "credits": 3, "is_required": False},
          {"subject": "ORGB", "catalog": "325", "title": "Negotiations and Conflict Resolution",        "credits": 3, "is_required": False},
          {"subject": "ORGB", "catalog": "380", "title": "Cross Cultural Management",                   "credits": 3, "is_required": False},
          {"subject": "ORGB", "catalog": "420", "title": "Managing Organizational Teams",               "credits": 3, "is_required": False},
          {"subject": "ORGB", "catalog": "421", "title": "Managing Organizational Change",              "credits": 3, "is_required": False},
          {"subject": "ORGB", "catalog": "525", "title": "Compensation Management",                     "credits": 3, "is_required": False},
        ],
      },
    ],
  },


  # ══════════════════════════════════════════════════════════════════
  # OPERATIONS MANAGEMENT
  # ══════════════════════════════════════════════════════════════════
  {
    "program_key": "operations_management_concentration_bcom",
    "name": "Operations Management – Concentration (B.Com.)",
    "program_type": "concentration",
    "faculty": "Desautels Faculty of Management",
    "total_credits": 15,
    "description": (
      "Operations Management is concerned with the design, planning, control, "
      "coordination, and improvement of business processes integral to creating "
      "a firm's products and services. Emphasizes quantitative analysis and "
      "cross-functional thinking. Graduates find careers in consulting, "
      "manufacturing, distribution, retail, transportation, and health care."
    ),
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/management/programs/concentrations/operations-management-concentration-bcom/",
    "blocks": [
      {
        "block_key": "om_conc_required",
        "title": "Required Operations Management Courses",
        "block_type": "required",
        "credits_needed": 6,
        "courses_needed": None,
        "group_name": None,
        "notes": "2 required courses (6 credits).",
        "sort_order": 1,
        "courses": [
          {"subject": "MGSC", "catalog": "373", "title": "Operations Research 1",                  "credits": 3, "is_required": True},
          {"subject": "MGSC", "catalog": "431", "title": "Operations and Supply Chain Analysis",   "credits": 3, "is_required": True},
        ],
      },
      {
        "block_key": "om_conc_complementary",
        "title": "Complementary Operations Courses",
        "block_type": "group",
        "credits_needed": 9,
        "courses_needed": None,
        "group_name": "9 credits from Complementary MGSC Courses",
        "notes": "Select 3 courses (9 credits) from the following list.",
        "sort_order": 2,
        "courses": [
          {"subject": "MGSC", "catalog": "372", "title": "Advanced Business Statistics",                 "credits": 3, "is_required": False},
          {"subject": "MGSC", "catalog": "403", "title": "Introduction to Logistics Management",         "credits": 3, "is_required": False},
          {"subject": "MGSC", "catalog": "404", "title": "Foundations of Decision Analytics",            "credits": 3, "is_required": False},
          {"subject": "MGSC", "catalog": "416", "title": "Data-Driven Models for Operations Analytics",  "credits": 3, "is_required": False},
          {"subject": "MGSC", "catalog": "417", "title": "Project Operations and Risk Management",       "credits": 3, "is_required": False},
          {"subject": "MGSC", "catalog": "434", "title": "Topics in Operations Management 1",            "credits": 3, "is_required": False},
          {"subject": "MGSC", "catalog": "488", "title": "Sustainability and Operations",                "credits": 3, "is_required": False},
        ],
      },
    ],
  },


  # ══════════════════════════════════════════════════════════════════
  # INTERNATIONAL MANAGEMENT / INTERNATIONAL BUSINESS
  # ══════════════════════════════════════════════════════════════════
  {
    "program_key": "international_management_major_bcom",
    "name": "International Management – Major (B.Com.)",
    "program_type": "major",
    "faculty": "Desautels Faculty of Management",
    "total_credits": 30,
    "description": (
      "The International Management Major prepares students to understand and "
      "operate in global business environments, examining economic foundations "
      "of international trade, cross-cultural management, and the strategies of "
      "multinational enterprises. Careers include international trade, consulting, "
      "global operations, and diplomacy-adjacent roles."
    ),
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/management/programs/majors/international-management-major-bcom/",
    "blocks": [
      {
        "block_key": "intl_major_required",
        "title": "Required International Management Courses",
        "block_type": "required",
        "credits_needed": 3,
        "courses_needed": None,
        "group_name": None,
        "notes": "1 required course (3 credits). Corequisite: MGCR 382.",
        "sort_order": 1,
        "courses": [
          {"subject": "BUSA", "catalog": "356", "title": "Management in Global Context",          "credits": 3, "is_required": True},
        ],
      },
      {
        "block_key": "intl_major_complementary",
        "title": "Complementary International Management Courses",
        "block_type": "group",
        "credits_needed": 27,
        "courses_needed": None,
        "group_name": "Complementary International Management Courses",
        "notes": (
          "Select from approved BUSA, FINE, INDR, MGPO, MRKT, ORGB and interdisciplinary "
          "courses to complete 30 credits total. Major also includes language (9–12 cr) and "
          "experiential learning components; consult BCom Student Affairs for details."
        ),
        "sort_order": 2,
        "courses": [
          {"subject": "BUSA", "catalog": "391", "title": "International Business Law",                    "credits": 3, "is_required": False},
          {"subject": "BUSA", "catalog": "394", "title": "Managing in Asia",                              "credits": 3, "is_required": False},
          {"subject": "BUSA", "catalog": "395", "title": "Managing in Europe",                            "credits": 3, "is_required": False},
          {"subject": "BUSA", "catalog": "396", "title": "Managing Internationally in Quebec",            "credits": 3, "is_required": False},
          {"subject": "BUSA", "catalog": "430", "title": "Business Climate in Developing Countries",      "credits": 3, "is_required": False},
          {"subject": "BUSA", "catalog": "433", "title": "Topics in International Business 1",            "credits": 3, "is_required": False},
          {"subject": "BUSA", "catalog": "435", "title": "Topics in International Business 2",            "credits": 3, "is_required": False},
          {"subject": "BUSA", "catalog": "481", "title": "Managing in North America",                     "credits": 3, "is_required": False},
          {"subject": "FINE", "catalog": "482", "title": "International Finance 1",                       "credits": 3, "is_required": False},
          {"subject": "FINE", "catalog": "492", "title": "International Corporate Finance",               "credits": 3, "is_required": False},
          {"subject": "INDR", "catalog": "459", "title": "Comparative Employment Relations",              "credits": 3, "is_required": False},
          {"subject": "MGPO", "catalog": "383", "title": "International Business Policy",                 "credits": 3, "is_required": False},
          {"subject": "MGPO", "catalog": "435", "title": "The Origins of Capitalism",                     "credits": 3, "is_required": False},
          {"subject": "MGPO", "catalog": "469", "title": "Managing Globalization",                        "credits": 3, "is_required": False},
          {"subject": "MGPO", "catalog": "475", "title": "Strategies for Developing Countries",           "credits": 3, "is_required": False},
          {"subject": "MRKT", "catalog": "483", "title": "International Marketing Management",            "credits": 3, "is_required": False},
          {"subject": "ORGB", "catalog": "380", "title": "Cross Cultural Management",                     "credits": 3, "is_required": False},
        ],
      },
    ],
  },

  {
    "program_key": "international_business_concentration_bcom",
    "name": "International Business – Concentration (B.Com.)",
    "program_type": "concentration",
    "faculty": "Desautels Faculty of Management",
    "total_credits": 15,
    "description": (
      "The International Business concentration provides students with the skills "
      "to understand the global context of business, including international trade, "
      "cross-cultural management, and the strategies of multinational enterprises. "
      "5 courses (15 credits)."
    ),
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/management/programs/concentrations/international-business-concentration-bcom/",
    "blocks": [
      {
        "block_key": "intb_conc_required",
        "title": "Required International Business Courses",
        "block_type": "required",
        "credits_needed": 3,
        "courses_needed": None,
        "group_name": None,
        "notes": "1 required course (3 credits). Corequisite: MGCR 382.",
        "sort_order": 1,
        "courses": [
          {"subject": "BUSA", "catalog": "356", "title": "Management in Global Context",          "credits": 3, "is_required": True},
        ],
      },
      {
        "block_key": "intb_conc_complementary",
        "title": "Complementary International Business Courses",
        "block_type": "group",
        "credits_needed": 12,
        "courses_needed": None,
        "group_name": "12 credits from Complementary International Business Courses",
        "notes": "Select 4 courses (12 credits) from approved BUSA, FINE, INDR, MGPO, MRKT, ORGB courses.",
        "sort_order": 2,
        "courses": [
          {"subject": "BUSA", "catalog": "391", "title": "International Business Law",                    "credits": 3, "is_required": False},
          {"subject": "BUSA", "catalog": "394", "title": "Managing in Asia",                              "credits": 3, "is_required": False},
          {"subject": "BUSA", "catalog": "395", "title": "Managing in Europe",                            "credits": 3, "is_required": False},
          {"subject": "BUSA", "catalog": "396", "title": "Managing Internationally in Quebec",            "credits": 3, "is_required": False},
          {"subject": "BUSA", "catalog": "430", "title": "Business Climate in Developing Countries",      "credits": 3, "is_required": False},
          {"subject": "BUSA", "catalog": "433", "title": "Topics in International Business 1",            "credits": 3, "is_required": False},
          {"subject": "BUSA", "catalog": "435", "title": "Topics in International Business 2",            "credits": 3, "is_required": False},
          {"subject": "BUSA", "catalog": "481", "title": "Managing in North America",                     "credits": 3, "is_required": False},
          {"subject": "FINE", "catalog": "482", "title": "International Finance 1",                       "credits": 3, "is_required": False},
          {"subject": "FINE", "catalog": "492", "title": "International Corporate Finance",               "credits": 3, "is_required": False},
          {"subject": "INDR", "catalog": "459", "title": "Comparative Employment Relations",              "credits": 3, "is_required": False},
          {"subject": "MGPO", "catalog": "383", "title": "International Business Policy",                 "credits": 3, "is_required": False},
          {"subject": "MGPO", "catalog": "435", "title": "The Origins of Capitalism",                     "credits": 3, "is_required": False},
          {"subject": "MGPO", "catalog": "469", "title": "Managing Globalization",                        "credits": 3, "is_required": False},
          {"subject": "MGPO", "catalog": "475", "title": "Strategies for Developing Countries",           "credits": 3, "is_required": False},
          {"subject": "MRKT", "catalog": "451", "title": "Marketing Research",                            "credits": 3, "is_required": False},
          {"subject": "MRKT", "catalog": "483", "title": "International Marketing Management",            "credits": 3, "is_required": False},
          {"subject": "ORGB", "catalog": "380", "title": "Cross Cultural Management",                     "credits": 3, "is_required": False},
        ],
      },
    ],
  },


  # ══════════════════════════════════════════════════════════════════
  # MANAGING FOR SUSTAINABILITY
  # ══════════════════════════════════════════════════════════════════
  {
    "program_key": "managing_sustainability_major_bcom",
    "name": "Managing for Sustainability – Major (B.Com.)",
    "program_type": "major",
    "faculty": "Desautels Faculty of Management",
    "total_credits": 30,
    "description": (
      "The Managing for Sustainability Major prepares students to address the "
      "relationship between economic activity, management, and environmental and "
      "social challenges. Combines management courses with interdisciplinary "
      "studies in sustainability, CSR, and social enterprise. Includes an "
      "experiential learning component. This major satisfies the BCom EL requirement."
    ),
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/management/programs/majors/managing-sustainability-major-bcom/",
    "blocks": [
      {
        "block_key": "sust_major_required",
        "title": "Required Sustainability Courses",
        "block_type": "required",
        "credits_needed": 6,
        "courses_needed": None,
        "group_name": None,
        "notes": "2 required courses (6 credits).",
        "sort_order": 1,
        "courses": [
          {"subject": "MGPO", "catalog": "440", "title": "Strategies for Sustainability",       "credits": 3, "is_required": True},
          {"subject": "MSUS", "catalog": "402", "title": "Systems Thinking and Sustainability", "credits": 3, "is_required": True},
        ],
      },
      {
        "block_key": "sust_major_complementary_mgmt",
        "title": "Complementary Sustainability-Focused Electives",
        "block_type": "group",
        "credits_needed": 9,
        "courses_needed": None,
        "group_name": "Complementary Sustainability-Focused Courses (3–9 credits)",
        "notes": "Select 3–9 credits from these sustainability-focused courses.",
        "sort_order": 2,
        "courses": [
          {"subject": "ACCT", "catalog": "401", "title": "Sustainability and Environmental Accounting", "credits": 3, "is_required": False},
          {"subject": "FINE", "catalog": "465", "title": "Sustainable Finance",                         "credits": 3, "is_required": False},
          {"subject": "INSY", "catalog": "455", "title": "Technology and Innovation for Sustainability","credits": 3, "is_required": False},
          {"subject": "MGPO", "catalog": "438", "title": "Social Entrepreneurship and Innovation",      "credits": 3, "is_required": False},
          {"subject": "MGSC", "catalog": "488", "title": "Sustainability and Operations",               "credits": 3, "is_required": False},
          {"subject": "MRKT", "catalog": "351", "title": "Marketing and Society",                       "credits": 3, "is_required": False},
        ],
      },
      {
        "block_key": "sust_major_envr",
        "title": "Experiential Learning, Policy & Environmental Courses",
        "block_type": "group",
        "credits_needed": 15,
        "courses_needed": None,
        "group_name": "Experiential Learning, Policy & Environmental Sciences Courses",
        "notes": (
          "Remaining credits (to reach 30) from: Experiential Learning (BUSA 451D1/D2, "
          "MGPO 430, MGSC 483, MSUS 400/401/497, RETL 410), Policy & Context (INDR 294/492, "
          "MGPO 365/435/450/469/475, MSUS 434, ORGB 321/325/421), and Environmental Sciences "
          "(ENVR 200, 201, 202, 203, 400 plus others). ENVR courses have limited enrolment."
        ),
        "sort_order": 3,
        "courses": [
          {"subject": "MGPO", "catalog": "430", "title": "Practicum in Not for Profit Consulting",    "credits": 3, "is_required": False},
          {"subject": "MSUS", "catalog": "401", "title": "Sustainability Consulting",                  "credits": 3, "is_required": False},
          {"subject": "RETL", "catalog": "410", "title": "Sustainable Retail and Entrepreneurship",   "credits": 3, "is_required": False},
          {"subject": "MGPO", "catalog": "469", "title": "Managing Globalization",                     "credits": 3, "is_required": False},
          {"subject": "MGPO", "catalog": "475", "title": "Strategies for Developing Countries",        "credits": 3, "is_required": False},
          {"subject": "ORGB", "catalog": "325", "title": "Negotiations and Conflict Resolution",       "credits": 3, "is_required": False},
          {"subject": "ENVR", "catalog": "200", "title": "The Global Environment",                     "credits": 3, "is_required": False},
          {"subject": "ENVR", "catalog": "201", "title": "Society, Environment and Sustainability",    "credits": 3, "is_required": False},
          {"subject": "ENVR", "catalog": "202", "title": "The Evolving Earth",                         "credits": 3, "is_required": False},
          {"subject": "ENVR", "catalog": "203", "title": "Knowledge, Ethics and Environment",          "credits": 3, "is_required": False},
          {"subject": "ENVR", "catalog": "400", "title": "Environmental Thought",                      "credits": 3, "is_required": False},
        ],
      },
    ],
  },

  {
    "program_key": "managing_sustainability_concentration_bcom",
    "name": "Managing for Sustainability – Concentration (B.Com.)",
    "program_type": "concentration",
    "faculty": "Desautels Faculty of Management",
    "total_credits": 15,
    "description": (
      "The Managing for Sustainability concentration introduces students to the "
      "relationship between economic activity and environmental and social "
      "responsibility, developing tools for sustainable business strategy. "
      "5 courses (15 credits)."
    ),
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/management/programs/concentrations/managing-sustainability-concentration-bcom/",
    "blocks": [
      {
        "block_key": "sust_conc_required",
        "title": "Required Sustainability Courses",
        "block_type": "required",
        "credits_needed": 6,
        "courses_needed": None,
        "group_name": None,
        "notes": "2 required courses (6 credits).",
        "sort_order": 1,
        "courses": [
          {"subject": "MGPO", "catalog": "440", "title": "Strategies for Sustainability",       "credits": 3, "is_required": True},
          {"subject": "MSUS", "catalog": "402", "title": "Systems Thinking and Sustainability", "credits": 3, "is_required": True},
        ],
      },
      {
        "block_key": "sust_conc_primary_complementary",
        "title": "Primary Complementary Courses (3–9 credits)",
        "block_type": "group",
        "credits_needed": 9,
        "courses_needed": None,
        "group_name": "3–9 credits from Primary Complementary Courses",
        "notes": "Select 3–9 credits from this list.",
        "sort_order": 2,
        "courses": [
          {"subject": "ACCT", "catalog": "401", "title": "Sustainability and Environmental Accounting", "credits": 3, "is_required": False},
          {"subject": "FINE", "catalog": "465", "title": "Sustainable Finance",                         "credits": 3, "is_required": False},
          {"subject": "INSY", "catalog": "455", "title": "Technology and Innovation for Sustainability","credits": 3, "is_required": False},
          {"subject": "MGPO", "catalog": "438", "title": "Social Entrepreneurship and Innovation",      "credits": 3, "is_required": False},
          {"subject": "MGSC", "catalog": "488", "title": "Sustainability and Operations",               "credits": 3, "is_required": False},
          {"subject": "MRKT", "catalog": "351", "title": "Marketing and Society",                       "credits": 3, "is_required": False},
        ],
      },
      {
        "block_key": "sust_conc_secondary_complementary",
        "title": "Secondary Complementary Courses (0–6 credits)",
        "block_type": "group",
        "credits_needed": 6,
        "courses_needed": None,
        "group_name": "0–6 credits from Secondary Complementary Courses",
        "notes": "Select 0–6 credits from this list to reach 15 credits total.",
        "sort_order": 3,
        "courses": [
          {"subject": "BUSA", "catalog": "451D1", "title": "Creating Impact Through Research 1",    "credits": 3, "is_required": False},
          {"subject": "BUSA", "catalog": "451D2", "title": "Creating Impact Through Research 2",    "credits": 3, "is_required": False},
          {"subject": "INDR", "catalog": "294",   "title": "Introduction to Labour-Management Relations", "credits": 3, "is_required": False},
          {"subject": "MGPO", "catalog": "435",   "title": "The Origins of Capitalism",             "credits": 3, "is_required": False},
          {"subject": "MGPO", "catalog": "450",   "title": "Ethics in Management",                  "credits": 3, "is_required": False},
          {"subject": "MGPO", "catalog": "469",   "title": "Managing Globalization",                 "credits": 3, "is_required": False},
          {"subject": "MSUS", "catalog": "401",   "title": "Sustainability Consulting",              "credits": 3, "is_required": False},
          {"subject": "ORGB", "catalog": "321",   "title": "Leadership",                             "credits": 3, "is_required": False},
          {"subject": "ORGB", "catalog": "325",   "title": "Negotiations and Conflict Resolution",   "credits": 3, "is_required": False},
          {"subject": "RETL", "catalog": "410",   "title": "Sustainable Retail and Entrepreneurship","credits": 3, "is_required": False},
        ],
      },
    ],
  },


  # ══════════════════════════════════════════════════════════════════
  # RETAIL MANAGEMENT
  # ══════════════════════════════════════════════════════════════════
  {
    "program_key": "retail_management_major_bcom",
    "name": "Retail Management – Major (B.Com.)",
    "program_type": "major",
    "faculty": "Desautels Faculty of Management",
    "total_credits": 30,
    "description": (
      "The Retail Management Major prepares students for leadership in the "
      "multi-channel retail industry, combining marketing, operations, analytics, "
      "and organizational behaviour with a focus on the unique challenges of "
      "retail environments. Satisfies the BCom EL requirement."
    ),
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/management/programs/majors/retail-management-major-bcom/",
    "blocks": [
      {
        "block_key": "retl_major_core_extension",
        "title": "Extended Management Core Course",
        "block_type": "required",
        "credits_needed": 3,
        "courses_needed": None,
        "group_name": None,
        "notes": "MRKT 459 counts as part of the extended Management Core for this major (15 core courses).",
        "sort_order": 1,
        "courses": [
          {"subject": "MRKT", "catalog": "459", "title": "Retail Management", "credits": 3, "is_required": True},
        ],
      },
      {
        "block_key": "retl_major_required",
        "title": "Required Major Courses (12 credits)",
        "block_type": "group",
        "credits_needed": 12,
        "courses_needed": None,
        "group_name": "12 credits from RETL Major Courses",
        "notes": "Select 12 credits from the 4 RETL courses listed below (all are RETL-coded).",
        "sort_order": 2,
        "courses": [
          {"subject": "RETL", "catalog": "402", "title": "Innovations in Retailing",                "credits": 3, "is_required": False},
          {"subject": "RETL", "catalog": "407", "title": "Retail Management Project",               "credits": 3, "is_required": False},
          {"subject": "RETL", "catalog": "408", "title": "Omni-Channel Retailing",                  "credits": 3, "is_required": False},
          {"subject": "RETL", "catalog": "410", "title": "Sustainable Retail and Entrepreneurship", "credits": 3, "is_required": False},
        ],
      },
      {
        "block_key": "retl_major_complementary",
        "title": "Complementary Retail Courses (12 credits)",
        "block_type": "group",
        "credits_needed": 12,
        "courses_needed": None,
        "group_name": "12 credits from Approved Complementary Courses",
        "notes": "Select 12 credits from approved marketing, finance, supply chain, and operations courses.",
        "sort_order": 3,
        "courses": [
          {"subject": "INDR", "catalog": "294",  "title": "Introduction to Labour-Management Relations", "credits": 3, "is_required": False},
          {"subject": "INSY", "catalog": "440",  "title": "E-Business",                                 "credits": 3, "is_required": False},
          {"subject": "INSY", "catalog": "442",  "title": "Data Analysis and Visualization",            "credits": 3, "is_required": False},
          {"subject": "MGSC", "catalog": "403",  "title": "Introduction to Logistics Management",       "credits": 3, "is_required": False},
          {"subject": "MGSC", "catalog": "431",  "title": "Operations and Supply Chain Analysis",       "credits": 3, "is_required": False},
          {"subject": "MRKT", "catalog": "355",  "title": "Services Marketing",                         "credits": 3, "is_required": False},
          {"subject": "MRKT", "catalog": "438",  "title": "Brand Management",                           "credits": 3, "is_required": False},
          {"subject": "MRKT", "catalog": "440",  "title": "Marketing Analytics",                        "credits": 3, "is_required": False},
          {"subject": "MRKT", "catalog": "451",  "title": "Marketing Research",                         "credits": 3, "is_required": False},
          {"subject": "MRKT", "catalog": "452",  "title": "Consumer Behaviour",                         "credits": 3, "is_required": False},
          {"subject": "MRKT", "catalog": "455",  "title": "Sales Management",                           "credits": 3, "is_required": False},
          {"subject": "ORGB", "catalog": "423",  "title": "Human Resources Management",                 "credits": 3, "is_required": False},
          {"subject": "RETL", "catalog": "409",  "title": "Digitization of Retailing",                  "credits": 3, "is_required": False},
          {"subject": "RETL", "catalog": "434",  "title": "Topics in Retail Management 1",              "credits": 3, "is_required": False},
        ],
      },
    ],
  },

  {
    "program_key": "retail_management_concentration_bcom",
    "name": "Retail Management – Concentration (B.Com.)",
    "program_type": "concentration",
    "faculty": "Desautels Faculty of Management",
    "total_credits": 15,
    "description": (
      "The Retail Management concentration introduces students to the principles "
      "and strategic challenges of managing retail operations in a multi-channel "
      "environment. 5 courses (15 credits)."
    ),
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/management/programs/concentrations/retail-management-concentration-bcom/",
    "blocks": [
      {
        "block_key": "retl_conc_required",
        "title": "Required Retail Management Courses",
        "block_type": "required",
        "credits_needed": 9,
        "courses_needed": None,
        "group_name": None,
        "notes": "3 required courses (9 credits).",
        "sort_order": 1,
        "courses": [
          {"subject": "MRKT", "catalog": "459", "title": "Retail Management",         "credits": 3, "is_required": True},
          {"subject": "RETL", "catalog": "402", "title": "Innovations in Retailing",  "credits": 3, "is_required": True},
          {"subject": "RETL", "catalog": "407", "title": "Retail Management Project", "credits": 3, "is_required": True},
        ],
      },
      {
        "block_key": "retl_conc_complementary",
        "title": "Complementary Retail Courses",
        "block_type": "group",
        "credits_needed": 6,
        "courses_needed": None,
        "group_name": "6 credits from Complementary Retail Courses",
        "notes": "Select 2 courses (6 credits) from the following list.",
        "sort_order": 2,
        "courses": [
          {"subject": "INDR", "catalog": "294",  "title": "Introduction to Labour-Management Relations", "credits": 3, "is_required": False},
          {"subject": "INSY", "catalog": "440",  "title": "E-Business",                                 "credits": 3, "is_required": False},
          {"subject": "INSY", "catalog": "442",  "title": "Data Analysis and Visualization",            "credits": 3, "is_required": False},
          {"subject": "MGSC", "catalog": "403",  "title": "Introduction to Logistics Management",       "credits": 3, "is_required": False},
          {"subject": "MGSC", "catalog": "431",  "title": "Operations and Supply Chain Analysis",       "credits": 3, "is_required": False},
          {"subject": "MRKT", "catalog": "355",  "title": "Services Marketing",                         "credits": 3, "is_required": False},
          {"subject": "MRKT", "catalog": "451",  "title": "Marketing Research",                         "credits": 3, "is_required": False},
          {"subject": "MRKT", "catalog": "452",  "title": "Consumer Behaviour",                         "credits": 3, "is_required": False},
          {"subject": "MRKT", "catalog": "455",  "title": "Sales Management",                           "credits": 3, "is_required": False},
          {"subject": "ORGB", "catalog": "423",  "title": "Human Resources Management",                 "credits": 3, "is_required": False},
          {"subject": "RETL", "catalog": "408",  "title": "Omni-Channel Retailing",                     "credits": 3, "is_required": False},
          {"subject": "RETL", "catalog": "409",  "title": "Digitization of Retailing",                  "credits": 3, "is_required": False},
          {"subject": "RETL", "catalog": "410",  "title": "Sustainable Retail and Entrepreneurship",    "credits": 3, "is_required": False},
          {"subject": "RETL", "catalog": "434",  "title": "Topics in Retail Management 1",              "credits": 3, "is_required": False},
        ],
      },
    ],
  },


  # ══════════════════════════════════════════════════════════════════
  # ENTREPRENEURSHIP
  # ══════════════════════════════════════════════════════════════════
  {
    "program_key": "entrepreneurship_concentration_bcom",
    "name": "Entrepreneurship – Concentration (B.Com.)",
    "program_type": "concentration",
    "faculty": "Desautels Faculty of Management",
    "total_credits": 15,
    "description": (
      "The Entrepreneurship concentration prepares students to identify business "
      "opportunities, develop business plans, and launch ventures. Focuses on "
      "new venture creation, venture capital, innovation, and small business "
      "management. 5 courses (15 credits)."
    ),
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/management/programs/concentrations/entrepreneurship-concentration-bcom/",
    "blocks": [
      {
        "block_key": "entr_conc_required",
        "title": "Required Entrepreneurship Courses",
        "block_type": "required",
        "credits_needed": 6,
        "courses_needed": None,
        "group_name": None,
        "notes": "2 required courses (6 credits).",
        "sort_order": 1,
        "courses": [
          {"subject": "MGPO", "catalog": "362", "title": "Fundamentals of Entrepreneurship",  "credits": 3, "is_required": True},
          {"subject": "MGPO", "catalog": "364", "title": "Entrepreneurship in Practice",       "credits": 3, "is_required": True},
        ],
      },
      {
        "block_key": "entr_conc_complementary",
        "title": "Complementary Entrepreneurship Courses",
        "block_type": "group",
        "credits_needed": 9,
        "courses_needed": None,
        "group_name": "9 credits from Complementary Courses",
        "notes": "Select 3 courses (9 credits) from approved entrepreneurship-related courses.",
        "sort_order": 2,
        "courses": [
          {"subject": "ACCT", "catalog": "361",  "title": "Management Accounting",                           "credits": 3, "is_required": False},
          {"subject": "BUSA", "catalog": "300",  "title": "Case Analysis and Presentation",                  "credits": 3, "is_required": False},
          {"subject": "BUSA", "catalog": "364",  "title": "Business Law 1",                                  "credits": 3, "is_required": False},
          {"subject": "BUSA", "catalog": "451D1","title": "Creating Impact Through Research 1",              "credits": 3, "is_required": False},
          {"subject": "BUSA", "catalog": "451D2","title": "Creating Impact Through Research 2",              "credits": 3, "is_required": False},
          {"subject": "BUSA", "catalog": "465",  "title": "Technological Entrepreneurship",                  "credits": 3, "is_required": False},
          {"subject": "FINE", "catalog": "447",  "title": "Venture Capital and Entrepreneurial Finance",     "credits": 3, "is_required": False},
          {"subject": "FINE", "catalog": "477",  "title": "Fintech for Business and Finance",                "credits": 3, "is_required": False},
          {"subject": "INSY", "catalog": "331",  "title": "Managing and Organizing Digital Technology",      "credits": 3, "is_required": False},
          {"subject": "INSY", "catalog": "334",  "title": "Design Thinking for User Experience",             "credits": 3, "is_required": False},
          {"subject": "INSY", "catalog": "341",  "title": "Developing Business Applications",                "credits": 3, "is_required": False},
          {"subject": "INSY", "catalog": "432",  "title": "Digital Business Models",                         "credits": 3, "is_required": False},
          {"subject": "INSY", "catalog": "440",  "title": "E-Business",                                      "credits": 3, "is_required": False},
          {"subject": "INSY", "catalog": "455",  "title": "Technology and Innovation for Sustainability",    "credits": 3, "is_required": False},
          {"subject": "MGPO", "catalog": "365",  "title": "Business-Government Relations",                   "credits": 3, "is_required": False},
          {"subject": "MGPO", "catalog": "432",  "title": "Topics in Entrepreneurship",                      "credits": 3, "is_required": False},
          {"subject": "MGPO", "catalog": "438",  "title": "Social Entrepreneurship and Innovation",          "credits": 3, "is_required": False},
          {"subject": "MGPO", "catalog": "440",  "title": "Strategies for Sustainability",                   "credits": 3, "is_required": False},
          {"subject": "MGPO", "catalog": "445",  "title": "Industry Analysis and Competitive Strategy",      "credits": 3, "is_required": False},
          {"subject": "MGPO", "catalog": "460",  "title": "Managing Innovation",                             "credits": 3, "is_required": False},
          {"subject": "MGPO", "catalog": "485",  "title": "Emerging Technologies: Organizing and Societal Stakes", "credits": 3, "is_required": False},
          {"subject": "MRKT", "catalog": "354",  "title": "Marketing Strategy",                              "credits": 3, "is_required": False},
          {"subject": "MRKT", "catalog": "365",  "title": "New Products",                                    "credits": 3, "is_required": False},
          {"subject": "MRKT", "catalog": "451",  "title": "Marketing Research",                              "credits": 3, "is_required": False},
          {"subject": "MRKT", "catalog": "455",  "title": "Sales Management",                                "credits": 3, "is_required": False},
          {"subject": "MRKT", "catalog": "459",  "title": "Retail Management",                               "credits": 3, "is_required": False},
          {"subject": "ORGB", "catalog": "321",  "title": "Leadership",                                      "credits": 3, "is_required": False},
          {"subject": "ORGB", "catalog": "325",  "title": "Negotiations and Conflict Resolution",            "credits": 3, "is_required": False},
          {"subject": "RETL", "catalog": "402",  "title": "Innovations in Retailing",                        "credits": 3, "is_required": False},
          {"subject": "RETL", "catalog": "410",  "title": "Sustainable Retail and Entrepreneurship",         "credits": 3, "is_required": False},
        ],
      },
    ],
  },


  # ══════════════════════════════════════════════════════════════════
  # ETHICS
  # ══════════════════════════════════════════════════════════════════
  {
    "program_key": "ethics_concentration_bcom",
    "name": "Ethics – Concentration (B.Com.)",
    "program_type": "concentration",
    "faculty": "Desautels Faculty of Management",
    "total_credits": 15,
    "description": (
      "The Ethics concentration examines the moral dimensions of business "
      "decisions, including corporate social responsibility, ethical leadership, "
      "and the interplay between business and society. 5 courses (15 credits)."
    ),
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/management/programs/concentrations/ethics-concentration-bcom/",
    "blocks": [
      {
        "block_key": "ethc_conc_courses",
        "title": "Ethics Concentration Courses (15 credits)",
        "block_type": "group",
        "credits_needed": 15,
        "courses_needed": None,
        "group_name": "Ethics Concentration Courses",
        "notes": (
          "Select 15 credits from approved ethics and social responsibility courses. "
          "Consult the BCom Student Affairs Office for the current required/complementary split. "
          "MGPO 450 Ethics in Management is the central ethics course. "
          "MGCR 460 is part of the Management Core and counts toward this concentration."
        ),
        "sort_order": 1,
        "courses": [
          {"subject": "MGCR", "catalog": "460", "title": "Social Context of Business",              "credits": 3, "is_required": False},
          {"subject": "MGPO", "catalog": "438", "title": "Social Entrepreneurship and Innovation",   "credits": 3, "is_required": False},
          {"subject": "MGPO", "catalog": "450", "title": "Ethics in Management",                    "credits": 3, "is_required": False},
          {"subject": "MGPO", "catalog": "469", "title": "Managing Globalization",                  "credits": 3, "is_required": False},
          {"subject": "MGPO", "catalog": "475", "title": "Strategies for Developing Countries",     "credits": 3, "is_required": False},
          {"subject": "MGSC", "catalog": "488", "title": "Sustainability and Operations",            "credits": 3, "is_required": False},
          {"subject": "ACCT", "catalog": "401", "title": "Sustainability and Environmental Accounting", "credits": 3, "is_required": False},
          {"subject": "RETL", "catalog": "410", "title": "Sustainable Retail and Entrepreneurship", "credits": 3, "is_required": False},
        ],
      },
    ],
  },


  # ══════════════════════════════════════════════════════════════════
  # ECONOMICS FOR MANAGEMENT STUDENTS
  # ══════════════════════════════════════════════════════════════════
  {
    "program_key": "economics_management_major_bcom",
    "name": "Economics for Management Students – Major (B.Com.)",
    "program_type": "major",
    "faculty": "Desautels Faculty of Management",
    "total_credits": 30,
    "description": (
      "The Economics Major for BCom students replaces MGCR 293 with "
      "ECON 230D1/D2 and MGCR 294 with ECON 332 + ECON 333 in the core. "
      "Provides a rigorous foundation in micro and macroeconomic theory, "
      "quantitative methods, and applied economics for business decision-making. "
      "Students must consult Economics Departmental Advisors to confirm course choices."
    ),
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/management/programs/majors/economics-management-students-major-bcom/",
    "blocks": [
      {
        "block_key": "econ_major_required",
        "title": "Required Economics Courses",
        "block_type": "required",
        "credits_needed": 15,
        "courses_needed": None,
        "group_name": None,
        "notes": (
          "Students replace MGCR 293 with ECON 230D1/D2 and MGCR 294 with "
          "ECON 332 + ECON 333 in the Management Core. Consult BCom advisors "
          "and Economics Departmental Advisors to confirm course choices."
        ),
        "sort_order": 1,
        "courses": [
          {"subject": "ECON", "catalog": "230D1", "title": "Microeconomic Theory 1",       "credits": 3, "is_required": True},
          {"subject": "ECON", "catalog": "230D2", "title": "Microeconomic Theory 2",       "credits": 3, "is_required": True},
          {"subject": "ECON", "catalog": "227D1", "title": "Economic Statistics 1",        "credits": 3, "is_required": True},
          {"subject": "ECON", "catalog": "227D2", "title": "Economic Statistics 2",        "credits": 3, "is_required": True},
          {"subject": "ECON", "catalog": "332",   "title": "Macroeconomic Theory: Majors 1", "credits": 3, "is_required": True},
        ],
      },
      {
        "block_key": "econ_major_complementary",
        "title": "Complementary Economics Courses",
        "block_type": "group",
        "credits_needed": 15,
        "courses_needed": None,
        "group_name": "Complementary Economics Courses",
        "notes": "Select from ECON 300+ level courses and MGCR 341.",
        "sort_order": 2,
        "courses": [
          {"subject": "ECON", "catalog": "333",   "title": "Macroeconomic Theory: Majors 2", "credits": 3, "is_required": False},
          {"subject": "ECON", "catalog": "337",   "title": "Economic Development",           "credits": 3, "is_required": False},
          {"subject": "ECON", "catalog": "342",   "title": "Environmental Economics",        "credits": 3, "is_required": False},
          {"subject": "ECON", "catalog": "352D1", "title": "International Trade 1",          "credits": 3, "is_required": False},
          {"subject": "ECON", "catalog": "352D2", "title": "International Trade 2",          "credits": 3, "is_required": False},
          {"subject": "ECON", "catalog": "430",   "title": "Economic Policy Analysis",       "credits": 3, "is_required": False},
          {"subject": "ECON", "catalog": "438",   "title": "Industrial Organization",        "credits": 3, "is_required": False},
          {"subject": "ECON", "catalog": "450",   "title": "Advanced Mathematical Economics","credits": 3, "is_required": False},
        ],
      },
    ],
  },


  # ══════════════════════════════════════════════════════════════════
  # MATHEMATICS AND STATISTICS FOR MANAGEMENT
  # ══════════════════════════════════════════════════════════════════
  {
    "program_key": "math_stats_management_major_bcom",
    "name": "Mathematics and Statistics for Management – Major (B.Com.)",
    "program_type": "major",
    "faculty": "Desautels Faculty of Management",
    "total_credits": 30,
    "description": (
      "The Mathematics and Statistics for Management Major provides rigorous "
      "quantitative foundations for business careers in analytics, finance, "
      "operations research, and consulting. Students must take MATH 133, "
      "MATH 140, and MATH 141 and consult with an advisor in the Mathematics "
      "or Statistics department."
    ),
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/management/programs/majors/mathematics-statistics-management-major-bcom/",
    "blocks": [
      {
        "block_key": "math_major_required",
        "title": "Required Mathematics/Statistics Courses",
        "block_type": "required",
        "credits_needed": 15,
        "courses_needed": None,
        "group_name": None,
        "notes": (
          "Students must also complete MATH 133, MATH 140, and MATH 141 "
          "as prerequisites. Consult an advisor in the Mathematics or Statistics "
          "department to confirm course choices."
        ),
        "sort_order": 1,
        "courses": [
          {"subject": "MATH", "catalog": "133",  "title": "Linear Algebra and Geometry",   "credits": 3, "is_required": True},
          {"subject": "MATH", "catalog": "140",  "title": "Calculus 1",                    "credits": 3, "is_required": True},
          {"subject": "MATH", "catalog": "141",  "title": "Calculus 2",                    "credits": 3, "is_required": True},
          {"subject": "MATH", "catalog": "222",  "title": "Calculus 3",                    "credits": 3, "is_required": True},
          {"subject": "MATH", "catalog": "323",  "title": "Probability",                   "credits": 3, "is_required": True},
        ],
      },
      {
        "block_key": "math_major_complementary",
        "title": "Complementary Quantitative Courses",
        "block_type": "group",
        "credits_needed": 15,
        "courses_needed": None,
        "group_name": "Complementary Mathematics, Statistics, and Management Science Courses",
        "notes": "Select from upper-level MATH, STAT, MGSC, and FINE quantitative courses.",
        "sort_order": 2,
        "courses": [
          {"subject": "MATH", "catalog": "324",  "title": "Statistics",                         "credits": 3, "is_required": False},
          {"subject": "MATH", "catalog": "340",  "title": "Discrete Mathematics",               "credits": 3, "is_required": False},
          {"subject": "MATH", "catalog": "423",  "title": "Applied Regression",                 "credits": 3, "is_required": False},
          {"subject": "MGSC", "catalog": "372",  "title": "Advanced Business Statistics",       "credits": 3, "is_required": False},
          {"subject": "MGSC", "catalog": "401",  "title": "Statistical Foundations of Data Analytics",                 "credits": 3, "is_required": False},
          {"subject": "FINE", "catalog": "342",  "title": "Corporate Finance",                  "credits": 3, "is_required": False},
          {"subject": "FINE", "catalog": "448",  "title": "Financial Derivatives",              "credits": 3, "is_required": False},
          {"subject": "INSY", "catalog": "336",  "title": "Data Handling and Coding for Analytics",      "credits": 3, "is_required": False},
        ],
      },
    ],
  },

]


def seed_degree_requirements(supabase):
    """
    Insert all Management (BCom) degree requirements into Supabase.
    Safe to re-run: uses upsert on program_key, then deletes+reinserts blocks.
    """
    inserted_programs = 0
    inserted_blocks = 0
    inserted_courses = 0

    for prog in MANAGEMENT_PROGRAMS:
        # ── Upsert program ──────────────────────────────────────────
        prog_data = {
            "program_key":  prog["program_key"],
            "name":         prog["name"],
            "faculty":      prog.get("faculty", "Desautels Faculty of Management"),
            "program_type": prog["program_type"],
            "total_credits": prog.get("total_credits") or 0,
            "description":  prog.get("description"),
            "ecalendar_url": prog.get("ecalendar_url"),
        }
        result = supabase.table("degree_programs").upsert(
            prog_data, on_conflict="program_key"
        ).execute()
        prog_id = result.data[0]["id"]
        inserted_programs += 1

        # ── Clean re-seed blocks ────────────────────────────────────
        supabase.table("requirement_blocks").delete().eq("program_id", prog_id).execute()

        for i, block in enumerate(prog.get("blocks", [])):
            constraint_notes = block.get("constraint_notes") or block.get("notes") or ""

            block_data = {
                "program_id":       prog_id,
                "block_key":        block.get("block_key", f"block_{i}"),
                "title":            block.get("title", ""),
                "block_type":       block.get("block_type", "choose_credits"),
                "group_name":       block.get("group_name"),
                "courses_needed":   block.get("courses_needed"),
                "constraint_notes": constraint_notes,
                "credits_needed":   block.get("credits_needed"),
                "min_level":        block.get("min_level"),
                "max_credits_200":  block.get("max_credits_200"),
                "min_credits_400":  block.get("min_credits_400"),
                "notes":            block.get("notes", ""),
                "sort_order":       block.get("sort_order", i),
            }
            block_result = supabase.table("requirement_blocks").insert(block_data).execute()
            block_id = block_result.data[0]["id"]
            inserted_blocks += 1

            courses_batch = []
            for j, course in enumerate(block.get("courses", [])):
                is_required = course.get("is_required", False)
                if block.get("block_type") == "required":
                    is_required = True

                courses_batch.append({
                    "block_id":           block_id,
                    "subject":            course.get("subject", ""),
                    "catalog":            course.get("catalog"),
                    "title":              course.get("title", ""),
                    "credits":            course.get("credits", 3),
                    "is_required":        is_required,
                    "choose_from_group":  course.get("choose_from_group"),
                    "choose_n_credits":   course.get("choose_n_credits"),
                    "notes":              course.get("notes"),
                    "recommended":        course.get("recommended", False),
                    "recommendation_reason": course.get("recommendation_reason"),
                    "sort_order":         j,
                })
            for chunk_start in range(0, len(courses_batch), 50):
                chunk = courses_batch[chunk_start:chunk_start + 50]
                if chunk:
                    supabase.table("requirement_courses").insert(chunk).execute()
                    inserted_courses += len(chunk)

    return {
        "programs": inserted_programs,
        "blocks":   inserted_blocks,
        "courses":  inserted_courses,
    }


if __name__ == "__main__":
    import os
    import sys
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
    from api.utils.supabase_client import get_supabase
    supabase = get_supabase()
    stats = seed_degree_requirements(supabase)
    print(f"Seeded: {stats['programs']} programs, {stats['blocks']} blocks, {stats['courses']} courses")
