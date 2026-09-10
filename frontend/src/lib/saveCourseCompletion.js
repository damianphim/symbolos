/** Save the course before removing its exemption, preserving credit on failure. */
export async function saveCourseCompletion({ api, userId, course, editing, transferCode, standing, updateProfile, onRollbackFailure }) {
  const { term, year, grade, credits } = course
  const response = editing
    ? await api.updateCompleted(userId, course.course_code, { term, year, grade, credits })
    : await api.addCompleted(userId, course)
  if (!transferCode) return response

  const code = transferCode.replace(/\s/g, '').toUpperCase()
  let error
  try {
    const result = await updateProfile({ advanced_standing: standing.filter(
      item => String(item.course_code || '').replace(/\s/g, '').toUpperCase() !== code
    ) })
    error = result?.error
  } catch (failure) {
    error = failure
  }
  if (error) {
    if (!editing) {
      try { await api.removeCompleted(userId, course.course_code) }
      catch { await onRollbackFailure() }
    } else {
      await onRollbackFailure()
    }
    throw error
  }
  return response
}
