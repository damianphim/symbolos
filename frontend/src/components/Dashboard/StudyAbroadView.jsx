import React, { useState, useMemo } from 'react'
import {
  FaGlobe, FaUniversity, FaPlane,
  FaMapMarkerAlt, FaClock, FaExternalLinkAlt,
  FaChevronDown, FaChevronUp, FaSearch, FaRegBookmark, FaBookmark,
  FaGraduationCap, FaUsers, FaInfoCircle
} from 'react-icons/fa'
import { useLanguage } from '../../contexts/LanguageContext'
import './StudyAbroadView.css'

const PROGRAMS_EN = [
  {
    id: 'exchange_main', type: 'exchange',
    title: 'McGill Student Exchange Program',
    institution: '160+ Partner Universities',
    regions: ['europe', 'americas', 'asia_pacific', 'africa_middle'],
    country: 'Worldwide · 39 countries',
    duration: '1\u20132 semesters', credits: 'Up to 30 credits',
    faculties: null,
    description: "Complete a semester or full year at one of McGill's bilateral partner universities. You pay McGill tuition, earn credit toward your degree, and your transcript records the exchange with transfer credits. Spaces are limited and competitive.",
    eligibility: ['Full-time, degree-seeking McGill student', 'Minimum CGPA 3.0', 'At least 24 McGill credits completed by start of exchange'],
    deadlines: [{ label: 'Fall / Full-Year 2026', date: 'December 1, 2025 \u2013 January 15, 2026' }, { label: 'Winter 2027', date: 'April \u2013 June 2026 (dates TBC)' }],
    notes: 'Host institution grades do NOT appear on your McGill transcript or affect CGPA. A non-refundable application fee applies.',
    links: [{ label: 'McGill Abroad \u2013 Exchange', url: 'https://www.mcgill.ca/mcgillabroad/go-abroad/steps/apply' }, { label: 'Partner Universities', url: 'https://www.mcgill.ca/mcgillabroad/go-abroad/steps/destinations' }],
  },
  {
    id: 'exchange_management', type: 'exchange',
    title: 'Desautels International Student Exchange',
    institution: 'Top Business Schools Worldwide',
    regions: ['europe', 'americas', 'asia_pacific'],
    country: 'Worldwide', duration: '1 semester', credits: '15 credits',
    faculties: ['Desautels Faculty of Management'],
    description: 'Faculty-specific exchange for BCom students with top-ranked business schools in Europe, Asia, and the Americas.',
    eligibility: ['Enrolled in a BCom program at Desautels', 'Strong academic standing'],
    deadlines: [{ label: 'Application', date: 'Check Desautels International Programs website' }],
    notes: null,
    links: [{ label: 'Desautels International Exchange', url: 'https://www.mcgill.ca/desautels/programs/bcom/academics/exchange/student-going-abroad' }],
  },
  {
    id: 'exchange_law', type: 'exchange',
    title: 'Faculty of Law Exchange Program',
    institution: 'Leading Law Schools Worldwide',
    regions: ['europe', 'americas', 'asia_pacific'],
    country: 'Worldwide', duration: '1 semester', credits: 'Variable',
    faculties: ['Faculty of Law'],
    description: 'Approximately 25% of McGill law students study abroad. Strong partnerships with leading law schools globally. Credited summer Human Rights Internships through CHRLP are also available.',
    eligibility: ['Enrolled in BCL/LLB program at McGill Law'],
    deadlines: [{ label: 'Application', date: 'Contact Faculty of Law Student Affairs Office' }],
    notes: 'Summer Human Rights Internships through CHRLP count for course credit.',
    links: [{ label: 'Law Exchange Programs', url: 'https://www.mcgill.ca/law/students/student-affairs/exchange' }, { label: 'CHRLP Internships', url: 'https://www.mcgill.ca/humanrights/clinical/internships' }],
  },
  {
    id: 'field_east_africa', type: 'field',
    title: 'Field Studies \u2013 East Africa',
    institution: 'McGill University (off-campus)',
    regions: ['africa_middle'], country: 'Kenya / East Africa',
    duration: '1 semester', credits: '15 credits', faculties: ['Faculty of Arts'],
    description: 'Semester-long immersive program in East Africa taught by McGill professors. Students apply classroom knowledge to development, conservation, and social science challenges. McGill tuition applies.',
    eligibility: ['Arts, Science, or B.A.&Sc. students', 'Completed at least one year at McGill', 'Application and interview required'],
    deadlines: [{ label: 'Application', date: 'Check Arts OASIS \u2013 Study Away portal' }],
    notes: 'Field study credits can count toward major program requirements in many Arts programs.',
    links: [{ label: 'Arts OASIS \u2013 Field Studies', url: 'https://www.mcgill.ca/oasis/away' }],
  },
  {
    id: 'field_barbados', type: 'field',
    title: 'Field Studies \u2013 Barbados',
    institution: 'McGill University (off-campus)',
    regions: ['americas'], country: 'Barbados',
    duration: '1 semester', credits: '15 credits', faculties: ['Faculty of Arts'],
    description: 'Semester in Barbados focusing on Caribbean studies, ecology, history, and society. Courses taught by McGill faculty with local institutions.',
    eligibility: ['Arts and related students', 'Completed first year at McGill'],
    deadlines: [{ label: 'Application', date: 'Check Arts OASIS \u2013 Study Away portal' }],
    notes: null,
    links: [{ label: 'Arts OASIS \u2013 Study Away', url: 'https://www.mcgill.ca/oasis/away' }],
  },
  {
    id: 'field_panama', type: 'field',
    title: 'Field Studies \u2013 Panama',
    institution: 'McGill University (off-campus)',
    regions: ['americas'], country: 'Panama',
    duration: '1 semester', credits: '15 credits', faculties: ['Faculty of Arts'],
    description: 'Semester program centered on tropical ecology, biodiversity, indigenous cultures, and sustainable development. Taught by McGill professors with on-the-ground fieldwork.',
    eligibility: ['Arts and related students', 'Completed first year at McGill'],
    deadlines: [{ label: 'Application', date: 'Check Arts OASIS \u2013 Study Away portal' }],
    notes: null,
    links: [{ label: 'Arts OASIS \u2013 Study Away', url: 'https://www.mcgill.ca/oasis/away' }],
  },
  {
    id: 'field_science_minor', type: 'field',
    title: 'Field Studies Minor \u2013 Science',
    institution: 'McGill University',
    regions: ['americas', 'africa_middle', 'asia_pacific', 'europe'],
    country: 'Various international destinations',
    duration: 'Variable (multiple terms)', credits: '18 credits (minor)', faculties: ['Faculty of Science'],
    description: 'An 18-credit minor combining field courses in diverse natural settings. Offers hands-on application of scientific methods outside the lab. Contact IFSO for available destinations.',
    eligibility: ['Enrolled in a B.Sc. program'],
    deadlines: [{ label: 'Inquiries', date: 'ifso.science@mcgill.ca' }],
    notes: null,
    links: [{ label: 'Science Field Studies', url: 'https://www.mcgill.ca/science/undergraduate/internships-field/field' }],
  },
  {
    id: 'courses_abroad', type: 'courses',
    title: 'McGill Courses Taught Abroad',
    institution: 'McGill University',
    regions: ['europe', 'americas', 'asia_pacific', 'africa_middle'],
    country: 'Various (changes each year)',
    duration: 'Short course or full summer', credits: '3\u20136 credits per course', faculties: null,
    description: 'Short courses designed by McGill professors at international locations. Earn full McGill credits at McGill tuition rates. Listings change annually.',
    eligibility: ['Open to all McGill undergraduates', 'Prerequisites vary by course'],
    deadlines: [{ label: 'Listings & Application', date: 'Check McGill Abroad each semester' }],
    notes: 'Courses count toward your degree like any on-campus course.',
    links: [{ label: 'McGill Courses Abroad', url: 'https://www.mcgill.ca/mcgillabroad/' }],
  },
  {
    id: 'internship_arts', type: 'internship',
    title: 'Arts Faculty Internship Program',
    institution: 'Various employers',
    regions: ['americas', 'europe', 'asia_pacific'], country: 'Canada & international',
    duration: '4\u20138 months', credits: 'Variable (may be credited)', faculties: ['Faculty of Arts'],
    description: 'The Faculty of Arts supports domestic and international internship placements aligned with your studies. Some internships count toward degree credits.',
    eligibility: ['Faculty of Arts students in good standing'],
    deadlines: [{ label: 'Application', date: 'Ongoing \u2013 check Arts OASIS' }],
    notes: null,
    links: [{ label: 'Arts Internships & Study Away', url: 'https://www.mcgill.ca/oasis/away' }],
  },
  {
    id: 'internship_engineering', type: 'internship',
    title: 'Engineering Internship & Co-op',
    institution: 'Industry partners',
    regions: ['americas', 'europe', 'asia_pacific'], country: 'Canada & international',
    duration: '12\u201316 months', credits: 'Credited as part of degree', faculties: ['Faculty of Engineering'],
    description: 'Formal internship and co-op programs including Mining and Materials Engineering co-ops. Professional engineering experience with credits toward your degree.',
    eligibility: ['Faculty of Engineering students in good standing', 'Program-specific requirements apply'],
    deadlines: [{ label: 'Application', date: 'Contact Engineering Student Affairs Office' }],
    notes: 'Mining and Materials Engineering also offer dedicated co-op programs.',
    links: [{ label: 'Engineering Internship Program', url: 'https://www.mcgill.ca/engineering/students/internship' }],
  },
  {
    id: 'internship_aes', type: 'internship',
    title: 'AES Internship Opportunities',
    institution: 'Agriculture / Environment employers',
    regions: ['americas', 'africa_middle', 'asia_pacific'], country: 'Various',
    duration: 'Variable', credits: 'May count toward degree', faculties: ['Faculty of Agricultural and Environmental Sciences'],
    description: 'AES students can pursue placements in agricultural, environmental, and food science sectors, with international options through faculty partnerships.',
    eligibility: ['Faculty of AES students'],
    deadlines: [{ label: 'Application', date: 'Check AES Internship Opportunities page' }],
    notes: null,
    links: [{ label: 'AES Internship Opportunities', url: 'https://www.mcgill.ca/macdonald/students/co-op-and-internship' }],
  },
  {
    id: 'internship_law', type: 'internship',
    title: 'Human Rights Internships \u2013 Law',
    institution: 'International Human Rights Organisations',
    regions: ['americas', 'europe', 'africa_middle', 'asia_pacific'], country: 'Various',
    duration: 'Summer (8\u201312 weeks)', credits: '3 credits', faculties: ['Faculty of Law'],
    description: 'Credited summer internships through CHRLP. Students work with human rights organisations and NGOs internationally.',
    eligibility: ['McGill Law students; competitive application'],
    deadlines: [{ label: 'Application', date: 'Check CHRLP website \u2014 typically winter term' }],
    notes: 'Credits count toward BCL/LLB requirements.',
    links: [{ label: 'CHRLP Internships', url: 'https://www.mcgill.ca/humanrights/clinical/internships' }],
  },
  {
    id: 'iut', type: 'iut',
    title: 'Inter-University Transfer (IUT)',
    institution: 'Any Quebec University (BCI network)',
    regions: ['canada'], country: 'Quebec, Canada',
    duration: '1 term', credits: 'Based on courses taken', faculties: null,
    description: "The BCI IUT agreement lets you take courses at any other Quebec university for credit toward your McGill degree at no extra cost. Grades do NOT appear on your transcript or CGPA.",
    eligibility: ['Registered at McGill', 'Course not available at McGill', 'Pre-approval required'],
    deadlines: [{ label: 'Pre-approval', date: 'Before registering at host institution' }, { label: 'Transfer credit', date: 'After completion \u2014 submit transcript to Enrolment Services' }],
    notes: 'IUT grades do NOT count toward your McGill CGPA.',
    links: [{ label: 'IUT Information', url: 'https://www.mcgill.ca/oasis/away/iut' }],
  },
  {
    id: 'isa_canada', type: 'iut',
    title: 'Independent Study Away (ISA)',
    institution: 'Accredited Canadian Universities',
    regions: ['canada'], country: 'Canada (outside Quebec)',
    duration: '1 term or summer', credits: 'Variable (pre-approved)', faculties: null,
    description: "Enrol as a visiting student at a Canadian university to earn credits toward your degree. As of Summer 2025, Arts students are limited to Canadian institutions only. Pre-approval is required.",
    eligibility: ['Currently registered McGill student', 'Courses must be pre-approved', 'Language-centre/practicum courses not eligible'],
    deadlines: [{ label: 'Pre-approval', date: 'Before registering \u2014 contact Faculty Advising' }],
    notes: 'Host institution tuition may be higher than McGill rates.',
    links: [{ label: 'Study Away \u2013 Arts OASIS', url: 'https://www.mcgill.ca/oasis/away/application-process/independent-study-away' }],
  },
  {
    id: 'jexplore', type: 'iut',
    title: "J'Explore Bursary Program",
    institution: 'Canadian Immersion Programs',
    regions: ['canada'], country: 'Canada',
    duration: '3\u20134 weeks (summer)', credits: 'Non-credit (bursary)', faculties: null,
    description: "Federally-funded bursary covering an intensive French or English immersion program at a Canadian university. Helps meet French language requirements for professional licensure in Quebec.",
    eligibility: ['Canadian citizens or permanent residents', 'Full-time McGill student'],
    deadlines: [{ label: 'Application', date: 'Check McGill Abroad or SOFA annually' }],
    notes: 'Good preparation for the OIIQ French proficiency exam.',
    links: [{ label: "J'Explore Program", url: 'https://www.canada.ca/en/canadian-heritage/services/funding/explore.html' }],
  },
]

const PROGRAMS_FR = [
  {
    id: 'exchange_main', type: 'exchange',
    title: "Programme d'\u00e9change \u00e9tudiant de McGill",
    institution: '160+ universit\u00e9s partenaires',
    regions: ['europe', 'americas', 'asia_pacific', 'africa_middle'],
    country: 'Partout dans le monde \u00b7 39 pays',
    duration: '1\u20132 semestres', credits: "Jusqu'\u00e0 30 cr\u00e9dits",
    faculties: null,
    description: "Effectuez un semestre ou une ann\u00e9e compl\u00e8te dans l'une des universit\u00e9s partenaires de McGill. Vous payez les frais de scolarit\u00e9 de McGill, obtenez des cr\u00e9dits pour votre dipl\u00f4me et votre relev\u00e9 enregistre l'\u00e9change avec des cr\u00e9dits de transfert. Les places sont limit\u00e9es et comp\u00e9titives.",
    eligibility: ["\u00c9tudiant(e) \u00e0 temps plein poursuivant un dipl\u00f4me \u00e0 McGill", 'CGPA minimum de 3,0', "Au moins 24 cr\u00e9dits McGill compl\u00e9t\u00e9s avant le d\u00e9but de l'\u00e9change"],
    deadlines: [{ label: 'Automne / Ann\u00e9e compl\u00e8te 2026', date: '1er d\u00e9cembre 2025 \u2013 15 janvier 2026' }, { label: 'Hiver 2027', date: 'Avril \u2013 juin 2026 (dates \u00e0 confirmer)' }],
    notes: "Les notes de l'\u00e9tablissement d'accueil n'apparaissent PAS sur votre relev\u00e9 de notes McGill et n'affectent pas le CGPA. Des frais de demande non remboursables s'appliquent.",
    links: [{ label: "McGill \u00e0 l'\u00e9tranger \u2013 \u00c9change", url: 'https://www.mcgill.ca/mcgillabroad/go-abroad/steps/apply' }, { label: 'Universit\u00e9s partenaires', url: 'https://www.mcgill.ca/mcgillabroad/go-abroad/steps/destinations' }],
  },
  {
    id: 'exchange_management', type: 'exchange',
    title: '\u00c9change international Desautels',
    institution: 'Meilleures \u00e9coles de commerce mondiales',
    regions: ['europe', 'americas', 'asia_pacific'],
    country: 'Partout dans le monde', duration: '1 semestre', credits: '15 cr\u00e9dits',
    faculties: ['Facult\u00e9 de gestion Desautels'],
    description: '\u00c9change sp\u00e9cifique \u00e0 la facult\u00e9 pour les \u00e9tudiants en BCom avec les meilleures \u00e9coles de commerce en Europe, en Asie et dans les Am\u00e9riques.',
    eligibility: ["Inscrit(e) dans un programme BCom \u00e0 Desautels", 'Bon dossier acad\u00e9mique'],
    deadlines: [{ label: 'Demande', date: 'Consulter le site des programmes internationaux Desautels' }],
    notes: null,
    links: [{ label: '\u00c9change international Desautels', url: 'https://www.mcgill.ca/desautels/programs/bcom/academics/exchange/student-going-abroad' }],
  },
  {
    id: 'exchange_law', type: 'exchange',
    title: "Programme d'\u00e9change de la Facult\u00e9 de droit",
    institution: 'Grandes facult\u00e9s de droit mondiales',
    regions: ['europe', 'americas', 'asia_pacific'],
    country: 'Partout dans le monde', duration: '1 semestre', credits: 'Variable',
    faculties: ['Facult\u00e9 de droit'],
    description: "Environ 25\u202f% des \u00e9tudiants en droit de McGill \u00e9tudient \u00e0 l'\u00e9tranger. Partenariats solides avec les grandes facult\u00e9s de droit mondiales. Des stages estivaux en droits humains cr\u00e9dit\u00e9s via le CHRLP sont \u00e9galement disponibles.",
    eligibility: ["Inscrit(e) dans le programme BCL/LLB de la Facult\u00e9 de droit de McGill"],
    deadlines: [{ label: 'Demande', date: "Contacter le Bureau des affaires \u00e9tudiantes de la Facult\u00e9 de droit" }],
    notes: 'Les stages estivaux en droits humains via le CHRLP comptent pour les cr\u00e9dits de cours.',
    links: [{ label: "Programmes d'\u00e9change en droit", url: 'https://www.mcgill.ca/law/students/student-affairs/exchange' }, { label: 'Stages CHRLP', url: 'https://www.mcgill.ca/humanrights/clinical/internships' }],
  },
  {
    id: 'field_east_africa', type: 'field',
    title: "\u00c9tudes sur le terrain \u2013 Afrique de l'Est",
    institution: 'Universit\u00e9 McGill (hors campus)',
    regions: ['africa_middle'], country: "Kenya / Afrique de l'Est",
    duration: '1 semestre', credits: '15 cr\u00e9dits', faculties: ['Facult\u00e9 des arts'],
    description: "Programme immersif d'un semestre en Afrique de l'Est enseign\u00e9 par des professeurs de McGill. Les \u00e9tudiant(e)s appliquent leurs connaissances au d\u00e9veloppement, \u00e0 la conservation et aux sciences sociales.",
    eligibility: ["\u00c9tudiant(e)s en arts, sciences ou B.A.&Sc.", 'Au moins un an compl\u00e9t\u00e9 \u00e0 McGill', 'Candidature et entretien requis'],
    deadlines: [{ label: 'Demande', date: "Consulter le portail Arts OASIS \u2013 \u00c9tudes \u00e0 l'ext\u00e9rieur" }],
    notes: "Les cr\u00e9dits d'\u00e9tudes sur le terrain peuvent compter pour les exigences des programmes majeurs dans de nombreux programmes d'arts.",
    links: [{ label: "Arts OASIS \u2013 \u00c9tudes sur le terrain", url: 'https://www.mcgill.ca/oasis/away' }],
  },
  {
    id: 'field_barbados', type: 'field',
    title: '\u00c9tudes sur le terrain \u2013 Barbade',
    institution: 'Universit\u00e9 McGill (hors campus)',
    regions: ['americas'], country: 'Barbade',
    duration: '1 semestre', credits: '15 cr\u00e9dits', faculties: ['Facult\u00e9 des arts'],
    description: "Semestre \u00e0 la Barbade ax\u00e9 sur les \u00e9tudes carib\u00e9ennes, l'\u00e9cologie, l'histoire et la soci\u00e9t\u00e9. Cours dispens\u00e9s par des professeurs de McGill avec des institutions locales.",
    eligibility: ["\u00c9tudiant(e)s en arts et disciplines connexes", 'Premi\u00e8re ann\u00e9e \u00e0 McGill compl\u00e9t\u00e9e'],
    deadlines: [{ label: 'Demande', date: "Consulter le portail Arts OASIS \u2013 \u00c9tudes \u00e0 l'ext\u00e9rieur" }],
    notes: null,
    links: [{ label: "Arts OASIS \u2013 \u00c9tudes \u00e0 l'ext\u00e9rieur", url: 'https://www.mcgill.ca/oasis/away' }],
  },
  {
    id: 'field_panama', type: 'field',
    title: '\u00c9tudes sur le terrain \u2013 Panama',
    institution: 'Universit\u00e9 McGill (hors campus)',
    regions: ['americas'], country: 'Panama',
    duration: '1 semestre', credits: '15 cr\u00e9dits', faculties: ['Facult\u00e9 des arts'],
    description: "Programme semestriel ax\u00e9 sur l'\u00e9cologie tropicale, la biodiversit\u00e9, les cultures autochtones et le d\u00e9veloppement durable. Enseign\u00e9 par des professeurs de McGill avec des travaux sur le terrain.",
    eligibility: ["\u00c9tudiant(e)s en arts et disciplines connexes", 'Premi\u00e8re ann\u00e9e \u00e0 McGill compl\u00e9t\u00e9e'],
    deadlines: [{ label: 'Demande', date: "Consulter le portail Arts OASIS \u2013 \u00c9tudes \u00e0 l'ext\u00e9rieur" }],
    notes: null,
    links: [{ label: "Arts OASIS \u2013 \u00c9tudes \u00e0 l'ext\u00e9rieur", url: 'https://www.mcgill.ca/oasis/away' }],
  },
  {
    id: 'field_science_minor', type: 'field',
    title: 'Mineure en \u00e9tudes sur le terrain \u2013 Sciences',
    institution: 'Universit\u00e9 McGill',
    regions: ['americas', 'africa_middle', 'asia_pacific', 'europe'],
    country: 'Diverses destinations internationales',
    duration: 'Variable (plusieurs trimestres)', credits: '18 cr\u00e9dits (mineure)', faculties: ['Facult\u00e9 des sciences'],
    description: "Une mineure de 18 cr\u00e9dits combinant des cours sur le terrain dans des milieux naturels vari\u00e9s. Offre une application pratique des m\u00e9thodes scientifiques hors laboratoire. Contacter l'IFSO pour les destinations disponibles.",
    eligibility: ["Inscrit(e) dans un programme B.Sc."],
    deadlines: [{ label: 'Renseignements', date: 'ifso.science@mcgill.ca' }],
    notes: null,
    links: [{ label: '\u00c9tudes sur le terrain \u2013 Sciences', url: 'https://www.mcgill.ca/science/undergraduate/internships-field/field' }],
  },
  {
    id: 'courses_abroad', type: 'courses',
    title: "Cours McGill enseign\u00e9s \u00e0 l'\u00e9tranger",
    institution: 'Universit\u00e9 McGill',
    regions: ['europe', 'americas', 'asia_pacific', 'africa_middle'],
    country: 'Divers (change chaque ann\u00e9e)',
    duration: 'Cours court ou \u00e9t\u00e9 complet', credits: '3\u20136 cr\u00e9dits par cours', faculties: null,
    description: "Cours courts con\u00e7us par des professeurs de McGill dans des lieux internationaux. Obtenez des cr\u00e9dits McGill complets aux tarifs de scolarit\u00e9 McGill. Les offres changent chaque ann\u00e9e.",
    eligibility: ["Ouvert \u00e0 tous les \u00e9tudiants de premier cycle de McGill", 'Les pr\u00e9alables varient selon le cours'],
    deadlines: [{ label: 'Offres et candidature', date: "Consulter McGill \u00e0 l'\u00e9tranger chaque semestre" }],
    notes: 'Les cours comptent pour votre dipl\u00f4me comme tout cours sur campus.',
    links: [{ label: "Cours McGill \u00e0 l'\u00e9tranger", url: 'https://www.mcgill.ca/mcgillabroad/' }],
  },
  {
    id: 'internship_arts', type: 'internship',
    title: 'Programme de stages de la Facult\u00e9 des arts',
    institution: 'Divers employeurs',
    regions: ['americas', 'europe', 'asia_pacific'], country: 'Canada et international',
    duration: '4\u20138 mois', credits: 'Variable (peut \u00eatre cr\u00e9dit\u00e9)', faculties: ['Facult\u00e9 des arts'],
    description: "La Facult\u00e9 des arts soutient des stages nationaux et internationaux align\u00e9s sur vos \u00e9tudes. Certains stages comptent pour des cr\u00e9dits de dipl\u00f4me.",
    eligibility: ["\u00c9tudiant(e)s de la Facult\u00e9 des arts en bonne standing acad\u00e9mique"],
    deadlines: [{ label: 'Demande', date: 'En cours \u2013 consulter Arts OASIS' }],
    notes: null,
    links: [{ label: "Stages arts et \u00e9tudes \u00e0 l'ext\u00e9rieur", url: 'https://www.mcgill.ca/oasis/away' }],
  },
  {
    id: 'internship_engineering', type: 'internship',
    title: 'Stage et co-op en g\u00e9nie',
    institution: 'Partenaires industriels',
    regions: ['americas', 'europe', 'asia_pacific'], country: 'Canada et international',
    duration: '12\u201316 mois', credits: 'Cr\u00e9dit\u00e9 dans le cadre du dipl\u00f4me', faculties: ['Facult\u00e9 de g\u00e9nie'],
    description: "Programmes formels de stage et de co-op incluant les co-ops en g\u00e9nie minier et des mat\u00e9riaux. Exp\u00e9rience professionnelle en ing\u00e9nierie avec cr\u00e9dits vers votre dipl\u00f4me.",
    eligibility: ["\u00c9tudiant(e)s de la Facult\u00e9 de g\u00e9nie en bonne standing", "Les exigences sp\u00e9cifiques au programme s'appliquent"],
    deadlines: [{ label: 'Demande', date: "Contacter le Bureau des affaires \u00e9tudiantes en g\u00e9nie" }],
    notes: 'Les programmes de g\u00e9nie minier et des mat\u00e9riaux proposent \u00e9galement des programmes de co-op d\u00e9di\u00e9s.',
    links: [{ label: 'Programme de stages en g\u00e9nie', url: 'https://www.mcgill.ca/engineering/students/internship' }],
  },
  {
    id: 'internship_aes', type: 'internship',
    title: 'Opportunit\u00e9s de stages AES',
    institution: 'Employeurs agriculture / environnement',
    regions: ['americas', 'africa_middle', 'asia_pacific'], country: 'Divers',
    duration: 'Variable', credits: 'Peut compter pour le dipl\u00f4me', faculties: ['Facult\u00e9 des sciences agricoles et environnementales'],
    description: "Les \u00e9tudiant(e)s AES peuvent effectuer des stages dans les secteurs agricoles, environnementaux et des sciences alimentaires, avec des options internationales via les partenariats de la facult\u00e9.",
    eligibility: ["\u00c9tudiant(e)s de la Facult\u00e9 AES"],
    deadlines: [{ label: 'Demande', date: 'Consulter la page Opportunit\u00e9s de stages AES' }],
    notes: null,
    links: [{ label: 'Opportunit\u00e9s de stages AES', url: 'https://www.mcgill.ca/macdonald/students/co-op-and-internship' }],
  },
  {
    id: 'internship_law', type: 'internship',
    title: 'Stages en droits humains \u2013 Droit',
    institution: 'Organisations internationales de droits humains',
    regions: ['americas', 'europe', 'africa_middle', 'asia_pacific'], country: 'Divers',
    duration: '\u00c9t\u00e9 (8\u201312 semaines)', credits: '3 cr\u00e9dits', faculties: ['Facult\u00e9 de droit'],
    description: "Stages estivaux cr\u00e9dit\u00e9s via le CHRLP. Les \u00e9tudiant(e)s travaillent avec des organisations de droits humains et des ONG \u00e0 l'international.",
    eligibility: ["\u00c9tudiant(e)s en droit de McGill\u00a0; candidature comp\u00e9titive"],
    deadlines: [{ label: 'Demande', date: "Consulter le site du CHRLP \u2014 g\u00e9n\u00e9ralement au trimestre d'hiver" }],
    notes: 'Les cr\u00e9dits comptent pour les exigences BCL/LLB.',
    links: [{ label: 'Stages CHRLP', url: 'https://www.mcgill.ca/humanrights/clinical/internships' }],
  },
  {
    id: 'iut', type: 'iut',
    title: 'Transfert inter-universitaire (TIU)',
    institution: 'Toute universit\u00e9 qu\u00e9b\u00e9coise (r\u00e9seau BCI)',
    regions: ['canada'], country: 'Qu\u00e9bec, Canada',
    duration: '1 trimestre', credits: 'Selon les cours suivis', faculties: null,
    description: "L'accord TIU du BCI vous permet de suivre des cours dans toute autre universit\u00e9 qu\u00e9b\u00e9coise pour des cr\u00e9dits vers votre dipl\u00f4me McGill sans frais suppl\u00e9mentaires. Les notes N'APPARAISSENT PAS sur votre relev\u00e9 de notes ou CGPA.",
    eligibility: ["Inscrit(e) \u00e0 McGill", 'Cours non disponible \u00e0 McGill', 'Pr\u00e9-approbation requise'],
    deadlines: [{ label: 'Pr\u00e9-approbation', date: "Avant de s'inscrire \u00e0 l'\u00e9tablissement d'accueil" }, { label: 'Cr\u00e9dit de transfert', date: "Apr\u00e8s compl\u00e9tion \u2014 soumettre le relev\u00e9 aux Services d'inscription" }],
    notes: 'Les notes TIU ne comptent PAS dans votre CGPA McGill.',
    links: [{ label: 'Information TIU', url: 'https://www.mcgill.ca/oasis/away/iut' }],
  },
  {
    id: 'isa_canada', type: 'iut',
    title: "\u00c9tudes ind\u00e9pendantes \u00e0 l'ext\u00e9rieur (ISA)",
    institution: 'Universit\u00e9s canadiennes accr\u00e9dit\u00e9es',
    regions: ['canada'], country: 'Canada (hors Qu\u00e9bec)',
    duration: '1 trimestre ou \u00e9t\u00e9', credits: 'Variable (pr\u00e9-approuv\u00e9)', faculties: null,
    description: "Inscrivez-vous comme \u00e9tudiant(e) visiteur dans une universit\u00e9 canadienne pour obtenir des cr\u00e9dits vers votre dipl\u00f4me. Depuis l'\u00e9t\u00e9 2025, les \u00e9tudiant(e)s en arts sont limit\u00e9(e)s aux \u00e9tablissements canadiens uniquement. La pr\u00e9-approbation est obligatoire.",
    eligibility: ["\u00c9tudiant(e) actuellement inscrit(e) \u00e0 McGill", 'Les cours doivent \u00eatre pr\u00e9-approuv\u00e9s', 'Cours de centre linguistique/stage pratique non admissibles'],
    deadlines: [{ label: 'Pr\u00e9-approbation', date: "Avant de s'inscrire \u2014 contacter le conseiller de facult\u00e9" }],
    notes: "Les frais de scolarit\u00e9 de l'\u00e9tablissement d'accueil peuvent \u00eatre plus \u00e9lev\u00e9s que ceux de McGill.",
    links: [{ label: "\u00c9tudes \u00e0 l'ext\u00e9rieur \u2013 Arts OASIS", url: 'https://www.mcgill.ca/oasis/away/application-process/independent-study-away' }],
  },
  {
    id: 'jexplore', type: 'iut',
    title: "Programme de bourses J'Explore",
    institution: "Programmes d'immersion canadiens",
    regions: ['canada'], country: 'Canada',
    duration: '3\u20134 semaines (\u00e9t\u00e9)', credits: 'Sans cr\u00e9dit (bourse)', faculties: null,
    description: "Bourse financ\u00e9e par le gouvernement f\u00e9d\u00e9ral couvrant un programme intensif d'immersion en fran\u00e7ais ou en anglais dans une universit\u00e9 canadienne. Aide \u00e0 satisfaire les exigences en langue fran\u00e7aise pour l'accr\u00e9ditation professionnelle au Qu\u00e9bec.",
    eligibility: ['Citoyens canadiens ou r\u00e9sidents permanents', "\u00c9tudiant(e) \u00e0 temps plein \u00e0 McGill"],
    deadlines: [{ label: 'Demande', date: "Consulter McGill \u00e0 l'\u00e9tranger ou SOFA chaque ann\u00e9e" }],
    notes: "Bonne pr\u00e9paration pour l'examen de comp\u00e9tence en fran\u00e7ais de l'OIIQ.",
    links: [{ label: "Programme J'Explore", url: 'https://www.canada.ca/fr/patrimoine-canadien/services/financement/explorer.html' }],
  },
]

const TYPE_BADGE_KEYS = {
  exchange:   'sa.badgeExchange',
  field:      'sa.badgeField',
  courses:    'sa.badgeCourses',
  internship: 'sa.badgeInternship',
  iut:        'sa.badgeIut',
}

function ProgramCard({ program, saved, onToggleSave, t }) {
  const [open, setOpen] = useState(false)
  return (
    <div className={`sa-card ${open ? 'sa-card--open' : ''}`}>
      <div className="sa-card-header" onClick={() => setOpen(o => !o)}>
        <div className="sa-card-left">
          <span className={`sa-badge sa-badge--${program.type}`}>
            {t(TYPE_BADGE_KEYS[program.type])}
          </span>
          <div className="sa-card-info">
            <h3 className="sa-card-title">{program.title}</h3>
            <div className="sa-card-meta">
              <span className="sa-meta"><FaUniversity className="sa-mi" />{program.institution}</span>
              <span className="sa-meta"><FaMapMarkerAlt className="sa-mi" />{program.country}</span>
              <span className="sa-meta"><FaClock className="sa-mi" />{program.duration}</span>
              <span className="sa-meta"><FaGraduationCap className="sa-mi" />{program.credits}</span>
            </div>
          </div>
        </div>
        <div className="sa-card-controls">
          <button
            className={`sa-bm ${saved ? 'sa-bm--on' : ''}`}
            onClick={e => { e.stopPropagation(); onToggleSave(program.id) }}
            title={saved ? t('sa.removeBookmark') : t('sa.saveBookmark')}
          >
            {saved ? <FaBookmark /> : <FaRegBookmark />}
          </button>
          <span className="sa-chevron">{open ? <FaChevronUp /> : <FaChevronDown />}</span>
        </div>
      </div>
      {open && (
        <div className="sa-card-body">
          <p className="sa-desc">{program.description}</p>
          <div className="sa-body-grid">
            {program.eligibility?.length > 0 && (
              <div className="sa-section">
                <h4 className="sa-section-title"><FaUsers /> {t('sa.eligibility')}</h4>
                <ul className="sa-list-items">
                  {program.eligibility.map((e, i) => <li key={i}>{e}</li>)}
                </ul>
              </div>
            )}
            {program.deadlines?.length > 0 && (
              <div className="sa-section">
                <h4 className="sa-section-title"><FaClock /> {t('sa.deadlines')}</h4>
                {program.deadlines.map((d, i) => (
                  <div key={i} className="sa-dl-row">
                    <span className="sa-dl-label">{d.label}</span>
                    <span className="sa-dl-date">{d.date}</span>
                  </div>
                ))}
              </div>
            )}
          </div>
          {program.notes && (
            <div className="sa-note"><FaInfoCircle className="sa-note-icon" /><span>{program.notes}</span></div>
          )}
          <div className="sa-links">
            {program.links?.map((l, i) => (
              <a key={i} href={l.url} target="_blank" rel="noopener noreferrer" className="sa-link">
                {l.label} <FaExternalLinkAlt />
              </a>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

export default function StudyAbroadView({ profile = {} }) {
  const { t, language } = useLanguage()
  const [view,         setView]         = useState('browse')
  const [typeFilter,   setTypeFilter]   = useState('all')
  const [regionFilter, setRegionFilter] = useState('all')
  const [search,       setSearch]       = useState('')
  const [savedIds,     setSavedIds]     = useState(new Set())

  const PROGRAMS = language === 'fr' ? PROGRAMS_FR : PROGRAMS_EN

  const PROGRAM_TYPES = [
    { id: 'all',         label: t('sa.typeAll') },
    { id: 'exchange',    label: t('sa.typeExchange') },
    { id: 'field',       label: t('sa.typeField') },
    { id: 'courses',     label: t('sa.typeCourses') },
    { id: 'internship',  label: t('sa.typeInternship') },
    { id: 'iut',         label: t('sa.typeIut') },
  ]

  const REGIONS = [
    { id: 'all',           label: t('sa.regionAll') },
    { id: 'europe',        label: t('sa.regionEurope') },
    { id: 'americas',      label: t('sa.regionAmericas') },
    { id: 'asia_pacific',  label: t('sa.regionAsia') },
    { id: 'africa_middle', label: t('sa.regionAfrica') },
    { id: 'canada',        label: t('sa.regionCanada') },
  ]

  const toggleSave = id => setSavedIds(prev => {
    const next = new Set(prev)
    next.has(id) ? next.delete(id) : next.add(id)
    return next
  })

  const browsed = useMemo(() => PROGRAMS.filter(p => {
    if (typeFilter   !== 'all' && p.type !== typeFilter) return false
    if (regionFilter !== 'all' && !p.regions.includes(regionFilter)) return false
    if (search.trim()) {
      const q = search.toLowerCase()
      return p.title.toLowerCase().includes(q) ||
             p.institution.toLowerCase().includes(q) ||
             p.country.toLowerCase().includes(q) ||
             p.description.toLowerCase().includes(q)
    }
    return true
  }), [typeFilter, regionFilter, search, PROGRAMS])

  const savedPrograms = useMemo(() => PROGRAMS.filter(p => savedIds.has(p.id)), [savedIds, PROGRAMS])
  const hasFilters = typeFilter !== 'all' || regionFilter !== 'all' || search.trim()

  return (
    <div className="sa-view">
      <div className="sa-header">
        <div className="sa-header-icon"><FaGlobe /></div>
        <div>
          <h2 className="sa-title">{t('sa.title')}</h2>
          <p className="sa-sub">{t('sa.subtitle')}</p>
        </div>
      </div>

      <div className="sa-tabs">
        <button className={`sa-tab ${view === 'browse' ? 'sa-tab--active' : ''}`} onClick={() => setView('browse')}>
          {t('sa.browse')} <span className="sa-tab-pill">{PROGRAMS.length}</span>
        </button>
        <button className={`sa-tab ${view === 'saved' ? 'sa-tab--active' : ''}`} onClick={() => setView('saved')}>
          {t('sa.saved')} {savedIds.size > 0 && <span className="sa-tab-pill sa-tab-pill--accent">{savedIds.size}</span>}
        </button>
      </div>

      {view === 'browse' && (
        <>
          <div className="sa-stats">
            <span><b>150+</b> {t('sa.statPartners')}</span>
            <span className="sa-stats-dot">\u00b7</span>
            <span><b>39</b> {t('sa.statCountries')}</span>
            <span className="sa-stats-dot">\u00b7</span>
            <span><b>5</b> {t('sa.statTypes')}</span>
          </div>

          <div className="sa-search-row">
            <FaSearch className="sa-search-ico" />
            <input className="sa-search" placeholder={t('sa.searchPlaceholder')} value={search} onChange={e => setSearch(e.target.value)} />
            {search && <button className="sa-search-x" onClick={() => setSearch('')}>\u00d7</button>}
          </div>

          <div className="sa-pill-row">
            {PROGRAM_TYPES.map(pt => (
              <button key={pt.id} className={`sa-pill ${typeFilter === pt.id ? 'sa-pill--on' : ''}`} onClick={() => setTypeFilter(pt.id)}>{pt.label}</button>
            ))}
          </div>

          <div className="sa-pill-row sa-pill-row--sm">
            {REGIONS.map(r => (
              <button key={r.id} className={`sa-pill sa-pill--sm ${regionFilter === r.id ? 'sa-pill--on' : ''}`} onClick={() => setRegionFilter(r.id)}>{r.label}</button>
            ))}
          </div>

          <div className="sa-result-bar">
            <span className="sa-result-count">
              {browsed.length === 1 ? t('sa.program').replace('{count}', browsed.length) : t('sa.programs').replace('{count}', browsed.length)}
              {hasFilters ? t('sa.matchingFilters') : ''}
            </span>
            {hasFilters && (
              <button className="sa-clear-btn" onClick={() => { setTypeFilter('all'); setRegionFilter('all'); setSearch('') }}>{t('sa.clearFilters')}</button>
            )}
          </div>

          {browsed.length === 0
            ? <div className="sa-empty"><FaPlane className="sa-empty-ico" /><p>{t('sa.noMatch')}</p></div>
            : <div className="sa-cards">{browsed.map(p => <ProgramCard key={p.id} program={p} saved={savedIds.has(p.id)} onToggleSave={toggleSave} t={t} />)}</div>
          }
        </>
      )}

      {view === 'saved' && (
        <div className="sa-cards">
          {savedPrograms.length === 0 ? (
            <div className="sa-empty">
              <FaRegBookmark className="sa-empty-ico" />
              <p>{t('sa.noSaved')}</p>
              <p className="sa-empty-sub">{t('sa.noSavedSub')} <FaRegBookmark style={{verticalAlign:'middle'}} /></p>
            </div>
          ) : savedPrograms.map(p => <ProgramCard key={p.id} program={p} saved={true} onToggleSave={toggleSave} t={t} />)}
        </div>
      )}

      <div className="sa-footer">
        <span>{t('sa.footerText')}</span>
        <a href="https://www.mcgill.ca/mcgillabroad/go-abroad" target="_blank" rel="noopener noreferrer" className="sa-footer-link">
          {t('sa.footerLink')} <FaExternalLinkAlt />
        </a>
      </div>
    </div>
  )
}
