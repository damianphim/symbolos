import { it, expect } from 'vitest'
import { summarizeGrades } from './academicGrades'
it('weights edited grades and excludes exemptions and pass/fail credits', () => {
  expect(summarizeGrades([{grade:'A',credits:3},{grade:'F',credits:3},{grade:'S',credits:30}])).toEqual({gpa:2,credits:6})
  expect(summarizeGrades([{grade:'A',credits:3},{grade:'A',credits:3},{grade:null,credits:30}])).toEqual({gpa:4,credits:6})
})
