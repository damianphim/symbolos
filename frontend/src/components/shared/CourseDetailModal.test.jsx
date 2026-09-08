import { it, expect, vi } from 'vitest'
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import CourseDetailModal from './CourseDetailModal'
const closeCourse = vi.hoisted(() => vi.fn())
vi.mock('../../contexts/CourseDetailContext', () => ({useCourseDetail:()=>({course:{subject:'MIMM',catalog:'211',title:'Microbiology'},closeCourse})}))
vi.mock('../../contexts/PreferencesContext', () => ({useLanguage:()=>({t:key=>key})}))
it('closes course details before opening the completion form', async()=>{
 const toggle=vi.fn(); render(<CourseDetailModal onToggleCompleted={toggle} />)
 await userEvent.click(screen.getByRole('button',{name:'courses.detailDone'}))
 expect(closeCourse).toHaveBeenCalledOnce()
 expect(toggle).toHaveBeenCalledWith(expect.objectContaining({subject:'MIMM',catalog:'211'}))
 expect(closeCourse.mock.invocationCallOrder[0]).toBeLessThan(toggle.mock.invocationCallOrder[0])
})
