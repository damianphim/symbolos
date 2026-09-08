import { it, expect, vi } from 'vitest'
import { saveCourseCompletion } from './saveCourseCompletion'
function setup() {
  return {
    api: {addCompleted:vi.fn().mockResolvedValue({completed_course:{grade:'A'}}), updateCompleted:vi.fn(), removeCompleted:vi.fn().mockResolvedValue({})},
    userId:'student', course:{course_code:'MIMM 211',grade:'A'},
    transferCode:'MIMM211', standing:[{course_code:'MIMM 211'},{course_code:'CEGEP',credits:30}],
    updateProfile:vi.fn().mockResolvedValue({error:null}), onRollbackFailure:vi.fn(),
  }
}
it('reclassifies one course while retaining unrelated advanced standing',async()=>{
 const args=setup(); await saveCourseCompletion(args)
 expect(args.updateProfile).toHaveBeenCalledWith({advanced_standing:[{course_code:'CEGEP',credits:30}]})
 expect(args.api.removeCompleted).not.toHaveBeenCalled()
})
it('rolls back a new completion when exemption removal fails',async()=>{
 const args=setup(); args.updateProfile.mockResolvedValue({error:Error('offline')})
 await expect(saveCourseCompletion(args)).rejects.toThrow('offline')
 expect(args.api.removeCompleted).toHaveBeenCalledWith('student','MIMM 211')
})
it('does not delete an existing completion after a failed profile update',async()=>{
 const args=setup(); args.editing=true; args.updateProfile.mockRejectedValue(Error('offline'))
 await expect(saveCourseCompletion(args)).rejects.toThrow('offline')
 expect(args.api.removeCompleted).not.toHaveBeenCalled()
})
it('refreshes visible state if rollback also fails so retry edits the saved record',async()=>{
 const args=setup(); args.updateProfile.mockResolvedValue({error:Error('offline')}); args.api.removeCompleted.mockRejectedValue(Error('offline'))
 await expect(saveCourseCompletion(args)).rejects.toThrow('offline')
 expect(args.onRollbackFailure).toHaveBeenCalledOnce()
})
