const GRADE_POINTS = { A: 4, 'A-': 3.7, 'B+': 3.3, B: 3, 'B-': 2.7, 'C+': 2.3, C: 2, 'C-': 1.7, D: 1, F: 0 }

export function summarizeGrades(courses) {
  let points = 0
  let credits = 0
  for (const course of courses) {
    const grade = GRADE_POINTS[String(course.grade || '').trim().toUpperCase()]
    const weight = Number(course.credits ?? 3)
    if (grade == null || !Number.isFinite(weight) || weight <= 0) continue
    points += grade * weight
    credits += weight
  }
  return { gpa: credits > 0 ? points / credits : null, credits }
}
