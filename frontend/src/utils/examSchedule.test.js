import { describe, it, expect } from 'vitest'
import { lookupExams } from './examSchedule'
import { DEC_2026_EXAMS } from './examSchedule_dec2026'

describe('December 2026 exam schedule', () => {
  it('is registered as the Fall 2026 term', () => {
    const exam = lookupExams('ACCT 351').find(e => e.term === 'Fall')
    expect(exam).toMatchObject({
      term: 'Fall',
      year: 2026,
      termLabel: 'Fall 2026 Finals',
      date: '2026-12-15',
      start: '14:00',
      end: '17:00',
      campus: 'D.T.',
      type: 'IN-PERSON',
    })
  })

  it('keeps the April 2026 term alongside it', () => {
    const terms = lookupExams('ACCT 351').map(e => `${e.term} ${e.year}`)
    expect(terms).toContain('Winter 2026')
    expect(terms).toContain('Fall 2026')
  })

  it('has well-formed entries inside the exam period', () => {
    expect(DEC_2026_EXAMS.length).toBeGreaterThan(600)
    for (const e of DEC_2026_EXAMS) {
      expect(e.code).toMatch(/^[A-Z][A-Z0-9]{3} \d{3}[A-Z0-9]*$/)
      expect(e.date >= '2026-11-30' && e.date <= '2026-12-22').toBe(true)
      expect(e.start).toMatch(/^\d{2}:\d{2}$/)
      expect(['IN-PERSON', 'ONLINE']).toContain(e.type)
      if (e.type === 'ONLINE') expect(e.campus).toBeNull()
      if (e.end) expect(e.end > e.start).toBe(true)
    }
  })

  // FINE 443 has an in-person and an online section starting together, so
  // delivery type is part of what makes a slot distinct.
  it('has no duplicate slots for a course', () => {
    const keys = DEC_2026_EXAMS.map(e => `${e.code}|${e.date}|${e.start}|${e.type}`)
    expect(new Set(keys).size).toBe(keys.length)
  })

  it('keeps both slots when sections of a course sit different days', () => {
    expect(lookupExams('MUSP 123').filter(e => e.year === 2026 && e.term === 'Fall').map(e => e.date).sort())
      .toEqual(['2026-12-09', '2026-12-11'])
  })

  it('represents a multi-day take-home by its release time with no end', () => {
    const exam = lookupExams('ARTH 223').find(e => e.term === 'Fall')
    expect(exam).toMatchObject({ type: 'ONLINE', date: '2026-12-07', start: '09:00', end: null, campus: null })
  })
})
