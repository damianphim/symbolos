import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { PreferencesProvider } from '../../contexts/PreferencesContext'
import TargetGPACalculator from './TargetGPACalculator'

describe('GPA calculation windows', () => {
  it('uses only credits and grades in the selected term', async () => {
    const user = userEvent.setup()
    render(<PreferencesProvider><TargetGPACalculator currentGPA={2} completedCredits={90} /></PreferencesProvider>)
    await user.selectOptions(screen.getByRole('combobox'), 'term')
    await user.clear(screen.getByLabelText('Graded credits in window'))
    await user.type(screen.getByLabelText('Graded credits in window'), '6')
    await user.clear(screen.getByLabelText('GPA on those graded credits'))
    await user.type(screen.getByLabelText('GPA on those graded credits'), '3')
    await user.type(screen.getByLabelText('Target GPA'), '3.6')
    await user.click(screen.getByRole('button', { name: /calculate/i }))
    expect(document.querySelector('.result-value')).toHaveTextContent('4.00')
  })

  it('allows a zero GPA and renders an already exceeded target without crashing', async () => {
    const user = userEvent.setup()
    render(<PreferencesProvider><TargetGPACalculator currentGPA={4} completedCredits={100} /></PreferencesProvider>)
    await user.type(screen.getByLabelText('Target GPA'), '1')
    await user.click(screen.getByRole('button', { name: /calculate/i }))
    expect(document.querySelector('.result-value')).toHaveTextContent('0.00')
    await user.selectOptions(screen.getByRole('combobox'), 'term')
    await user.clear(screen.getByLabelText('Target GPA'))
    await user.type(screen.getByLabelText('Target GPA'), '3')
    await user.click(screen.getByRole('button', { name: /calculate/i }))
    expect(document.querySelector('.result-value')).toHaveTextContent('3.00')
  })
})
