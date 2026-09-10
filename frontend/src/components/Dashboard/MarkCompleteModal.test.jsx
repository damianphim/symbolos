import { describe, it, expect, vi } from 'vitest'
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { PreferencesProvider } from '../../contexts/PreferencesContext'
import MarkCompleteModal from './MarkCompleteModal'

describe('Completed course correction', () => {
  it('prefills an existing grade and saves the corrected grade', async () => {
    const user = userEvent.setup()
    const confirm = vi.fn().mockResolvedValue(undefined)
    render(<PreferencesProvider><MarkCompleteModal course={{subject: 'MIMM', catalog: '211', grade: 'B', credits: 3, term: 'winter', year: 2025, editing: true}} onConfirm={confirm} onCancel={() => {}} /></PreferencesProvider>)
    expect(screen.getByLabelText(/grade/i)).toHaveValue('B')
    await user.selectOptions(screen.getByLabelText(/grade/i), 'A')
    await user.click(screen.getByRole('button', {name: 'Save'}))
    expect(confirm).toHaveBeenCalledWith(expect.objectContaining({grade: 'A', term: 'winter', year: 2025, course_code: 'MIMM 211'}))
  })
})
