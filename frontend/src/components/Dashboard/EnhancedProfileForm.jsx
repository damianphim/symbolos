import { useState, useEffect } from 'react'
import { FaCheck, FaEnvelope, FaGraduationCap } from 'react-icons/fa'
import { HiMiniSparkles } from 'react-icons/hi2'
import { useLanguage } from '../../contexts/PreferencesContext'
import {
  MAJORS, MINORS, FACULTIES,
  getMajorsForFaculty, majorHasHonours,
  ARTS_MAJORS_BASC, SCIENCE_MAJORS_BASC,
  BASC_INTERFACULTY_PROGRAMS, BASC_STREAMS,
} from '../../utils/mcgillData'
import './EnhancedProfileForm.css'

const isBasc = (faculty) => faculty === 'Bachelor of Arts and Science'
const bascIsMultiTrack = (c) => c === 'Multi-track' || c === 'Joint Honours'

/** Same row shape as the read view's InfoRow, with a control on the value side. */
function EditRow({ label, hint, children }) {
  return (
    <div className="pic-row">
      <span className="pic-row-label">{label}</span>
      <span className="pic-row-value pef-value">
        {children}
        {hint && <span className="pef-hint">{hint}</span>}
      </span>
    </div>
  )
}

export default function EnhancedProfileForm({ profile, user, onSave, onCancel }) {
  const { t } = useLanguage()

  const [formData, setFormData] = useState({
    username: '',
    major: '',
    other_majors: [],
    minor: '',
    other_minors: [],
    concentration: '',
    faculty: '',
    year: '',
    interests: '',
    current_gpa: '',
    is_honours: false,
    advanced_standing: []
  })

  const [showMajorDropdown, setShowMajorDropdown] = useState(false)
  const [showMinorDropdown, setShowMinorDropdown] = useState(false)
  const [newAdvancedCourse, setNewAdvancedCourse] = useState({
    course_code: '',
    course_title: '',
    credits: 3
  })

  useEffect(() => {
    if (profile) {
      setFormData({
        username: profile.username || '',
        major: profile.major || '',
        other_majors: profile.other_majors || [],
        minor: profile.minor || '',
        other_minors: profile.other_minors || [],
        concentration: profile.concentration || '',
        faculty: profile.faculty || '',
        year: profile.year || '',
        interests: profile.interests || '',
        current_gpa: profile.current_gpa || '',
        is_honours: profile.is_honours || false,
        advanced_standing: (profile.advanced_standing || []).map(c => ({
          counts_toward_degree: true,
          counts_toward_major: false,
          ...c,
        }))
      })
    }
  }, [profile])

  // Get majors for the currently selected faculty
  const primaryMajorOptions = (() => {
    const f = formData.faculty
    if (!f) return MAJORS
    if (isBasc(f)) return [] // handled separately
    const facultyMajors = getMajorsForFaculty(f)
    return facultyMajors.length > 0 ? facultyMajors : MAJORS
  })()

  // Check if current major supports honours
  const showHonoursToggle = (() => {
    if (isBasc(formData.faculty)) {
      // BASC honours is handled via program names (e.g., "Cognitive Science (Honours)")
      return false
    }
    return majorHasHonours(formData.faculty, formData.major)
  })()

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({ ...prev, [name]: value }))
  }

  // When faculty changes, reset major if it's not in the new faculty's list
  const handleFacultyChange = (e) => {
    const newFaculty = e.target.value
    const newMajors = getMajorsForFaculty(newFaculty)
    setFormData(prev => ({
      ...prev,
      faculty: newFaculty,
      // Clear major if it doesn't exist in the new faculty
      major: newMajors.includes(prev.major) ? prev.major : '',
      // Reset honours when changing faculty
      is_honours: false,
      // Reset BASC-specific fields
      ...(isBasc(newFaculty) ? { concentration: '', other_majors: [] } : {}),
    }))
  }

  // When major changes, reset honours if new major doesn't support it
  const handleMajorChange = (e) => {
    const newMajor = e.target.value
    const hasHon = majorHasHonours(formData.faculty, newMajor)
    setFormData(prev => ({
      ...prev,
      major: newMajor,
      is_honours: hasHon ? prev.is_honours : false,
    }))
  }

  const handleAddMajor = (major) => {
    if (!formData.other_majors.includes(major) && major !== formData.major) {
      setFormData(prev => ({
        ...prev,
        other_majors: [...prev.other_majors, major]
      }))
    }
    setShowMajorDropdown(false)
  }

  const handleRemoveMajor = (major) => {
    setFormData(prev => ({
      ...prev,
      other_majors: prev.other_majors.filter(m => m !== major)
    }))
  }

  const handleAddMinor = (minor) => {
    if (!formData.other_minors.includes(minor) && minor !== formData.minor) {
      setFormData(prev => ({
        ...prev,
        other_minors: [...prev.other_minors, minor]
      }))
    }
    setShowMinorDropdown(false)
  }

  const handleRemoveMinor = (minor) => {
    setFormData(prev => ({
      ...prev,
      other_minors: prev.other_minors.filter(m => m !== minor)
    }))
  }

  const handleAddAdvancedCourse = () => {
    if (newAdvancedCourse.course_code) {
      setFormData(prev => ({
        ...prev,
        advanced_standing: [...prev.advanced_standing, {
          course_code: newAdvancedCourse.course_code,
          course_title: newAdvancedCourse.course_title || null,
          credits: newAdvancedCourse.credits,
          counts_toward_degree: true,
          counts_toward_major: false,
        }]
      }))
      setNewAdvancedCourse({ course_code: '', course_title: '', credits: 3 })
    }
  }

  const handleToggleAdvancedFlag = (index, flag) => {
    setFormData(prev => ({
      ...prev,
      advanced_standing: prev.advanced_standing.map((c, i) =>
        i === index ? { ...c, [flag]: !c[flag] } : c
      )
    }))
  }

  const handleRemoveAdvancedCourse = (index) => {
    setFormData(prev => ({
      ...prev,
      advanced_standing: prev.advanced_standing.filter((_, i) => i !== index)
    }))
  }

  const handleSubmit = (e) => {
    e.preventDefault()

    const cleanedData = {}

    const trimmedUsername = formData.username?.trim()
    cleanedData.username = trimmedUsername || null

    const trimmedMinor = formData.minor?.trim()
    cleanedData.minor = trimmedMinor || null

    const trimmedConcentration = formData.concentration?.trim()
    cleanedData.concentration = trimmedConcentration || null

    const trimmedInterests = formData.interests?.trim()
    cleanedData.interests = trimmedInterests || null

    cleanedData.major = formData.major?.trim() || ""
    cleanedData.faculty = formData.faculty?.trim() || ""
    cleanedData.is_honours = formData.is_honours || false

    cleanedData.year = formData.year ? parseInt(formData.year) : null

    if (formData.current_gpa) {
      const gpa = parseFloat(formData.current_gpa)
      if (!isNaN(gpa) && gpa >= 0 && gpa <= 4) {
        cleanedData.current_gpa = gpa
      } else {
        cleanedData.current_gpa = null
      }
    } else {
      cleanedData.current_gpa = null
    }

    if (formData.other_majors?.length > 0) {
      cleanedData.other_majors = [...new Set(formData.other_majors.filter(m => m?.trim()))]
    } else {
      cleanedData.other_majors = []
    }

    if (formData.other_minors?.length > 0) {
      cleanedData.other_minors = [...new Set(formData.other_minors.filter(m => m?.trim()))]
    } else {
      cleanedData.other_minors = []
    }

    if (formData.advanced_standing?.length > 0) {
      cleanedData.advanced_standing = formData.advanced_standing.filter(
        course => course.course_code?.trim()
      )
    } else {
      cleanedData.advanced_standing = []
    }

    onSave(cleanedData)
  }

  const required = <span className="pef-req">*</span>

  return (
    <form onSubmit={handleSubmit} className="pef">
      <div className="pic-body">
        {/* Academic */}
        <section className="pic-group">
          <h3 className="pic-group-label">
            <FaGraduationCap className="pic-group-icon" /> {t('profile.academicInfo')}
          </h3>
          <div className="pic-rows">
            <EditRow label={<>{t('profile.faculty')} {required}</>}>
              <select
                className="pef-control"
                name="faculty"
                value={formData.faculty}
                onChange={handleFacultyChange}
                required
              >
                <option value="">{t('profileForm.selectFaculty')}</option>
                {FACULTIES.map(faculty => (
                  <option key={faculty} value={faculty}>{faculty}</option>
                ))}
              </select>
              {formData.faculty === 'Faculty of Arts' && (
                <span className="pef-note">
                  <strong>Faculty of Arts degree structure:</strong> A B.A. requires at least one major and one minor. You don't need to decide on your exact combination right away, you have until you apply to graduate.
                </span>
              )}
            </EditRow>

            <EditRow label={t('profile.year')}>
              <select className="pef-control pef-control--narrow" name="year" value={formData.year} onChange={handleChange}>
                <option value="">{t('profileForm.selectYear')}</option>
                <option value="0">U0 (Foundation)</option>
                <option value="1">U1</option>
                <option value="2">U2</option>
                <option value="3">U3</option>
                <option value="4">U4</option>
                <option value="5+">U5+</option>
              </select>
            </EditRow>

            {isBasc(formData.faculty) ? (
              <>
                <EditRow label={<>Program Stream {required}</>}>
                  <select
                    className="pef-control"
                    value={
                      bascIsMultiTrack(formData.concentration)
                        ? formData.concentration
                        : 'Interfaculty'
                    }
                    onChange={(e) => {
                      const stream = e.target.value
                      setFormData(prev => ({
                        ...prev,
                        concentration: stream === 'Interfaculty' ? '' : stream,
                        major: '',
                        other_majors: [],
                        is_honours: false,
                      }))
                    }}
                  >
                    {BASC_STREAMS.map(s => (
                      <option key={s.value} value={s.value}>{s.label}, {s.description}</option>
                    ))}
                  </select>
                </EditRow>

                {!bascIsMultiTrack(formData.concentration) ? (
                  <EditRow
                    label={<>Interfaculty Program {required}</>}
                    hint="The interfaculty concentration you are completing"
                  >
                    <select className="pef-control" name="major" value={formData.major} onChange={handleChange}>
                      <option value="">Select your program</option>
                      {BASC_INTERFACULTY_PROGRAMS.map(prog => (
                        <option key={prog} value={prog}>{prog}</option>
                      ))}
                    </select>
                    {formData.major && (
                      <label className="pef-check">
                        <input
                          type="checkbox"
                          checked={formData.is_honours}
                          onChange={(e) => setFormData(prev => ({ ...prev, is_honours: e.target.checked }))}
                        />
                        Honours Program
                      </label>
                    )}
                  </EditRow>
                ) : (
                  <>
                    <EditRow label={<>Arts Concentration {required}</>} hint="36-credit Arts major concentration">
                      <select className="pef-control" name="major" value={formData.major} onChange={handleChange}>
                        <option value="">Select Arts program</option>
                        {ARTS_MAJORS_BASC.map(m => <option key={m} value={m}>{m}</option>)}
                      </select>
                    </EditRow>
                    <EditRow label={<>Science Concentration {required}</>} hint="36-credit Science major concentration">
                      <select
                        className="pef-control"
                        value={formData.other_majors[0] || ''}
                        onChange={(e) => setFormData(prev => ({
                          ...prev,
                          other_majors: e.target.value ? [e.target.value] : []
                        }))}
                      >
                        <option value="">Select Science program</option>
                        {SCIENCE_MAJORS_BASC.map(m => <option key={m} value={m}>{m}</option>)}
                      </select>
                    </EditRow>
                  </>
                )}

                <EditRow label={t('profile.primaryMinor')}>
                  <select className="pef-control" name="minor" value={formData.minor} onChange={handleChange}>
                    <option value="">{t('profileForm.selectMinor')}</option>
                    {MINORS.map(m => <option key={m} value={m}>{m}</option>)}
                  </select>
                </EditRow>
              </>
            ) : (
              <>
                <EditRow label={<>{t('profile.major')} {required}</>}>
                  <select
                    className="pef-control"
                    name="major"
                    value={formData.major}
                    onChange={handleMajorChange}
                    required
                  >
                    <option value="">{t('profileForm.selectMajor')}</option>
                    {primaryMajorOptions.map(major => (
                      <option key={major} value={major}>{major}</option>
                    ))}
                  </select>
                  {showHonoursToggle && (
                    <label className="pef-check">
                      <input
                        type="checkbox"
                        checked={formData.is_honours}
                        onChange={(e) => setFormData(prev => ({ ...prev, is_honours: e.target.checked }))}
                      />
                      Honours Program
                    </label>
                  )}
                </EditRow>

                <EditRow label={t('profile.additionalMajors')} hint={t('profileForm.forDoubleMajors')}>
                  <div className="pef-tags">
                    {formData.other_majors.map(major => (
                      <span key={major} className="pic-tag pic-tag--major">
                        {major}
                        <button type="button" className="pef-tag-x" onClick={() => handleRemoveMajor(major)} aria-label={t('profileForm.removeCourse')}>×</button>
                      </span>
                    ))}
                    <button type="button" className="pef-add-tag" onClick={() => setShowMajorDropdown(!showMajorDropdown)}>
                      +
                    </button>
                  </div>
                  {showMajorDropdown && (
                    <div className="pef-dropdown">
                      {MAJORS.filter(m => m !== formData.major && !formData.other_majors.includes(m)).map(major => (
                        <button key={major} type="button" className="pef-dropdown-item" onClick={() => handleAddMajor(major)}>{major}</button>
                      ))}
                    </div>
                  )}
                </EditRow>

                <EditRow label={t('profile.primaryMinor')}>
                  <select className="pef-control" name="minor" value={formData.minor} onChange={handleChange}>
                    <option value="">{t('profileForm.selectMinor')}</option>
                    {MINORS.map(minor => (
                      <option key={minor} value={minor}>{minor}</option>
                    ))}
                  </select>
                </EditRow>

                <EditRow label={t('profile.additionalMinors')} hint={t('profileForm.multipleMinors')}>
                  <div className="pef-tags">
                    {formData.other_minors.map(minor => (
                      <span key={minor} className="pic-tag pic-tag--minor">
                        {minor}
                        <button type="button" className="pef-tag-x" onClick={() => handleRemoveMinor(minor)} aria-label={t('profileForm.removeCourse')}>×</button>
                      </span>
                    ))}
                    <button type="button" className="pef-add-tag" onClick={() => setShowMinorDropdown(!showMinorDropdown)}>
                      +
                    </button>
                  </div>
                  {showMinorDropdown && (
                    <div className="pef-dropdown">
                      {MINORS.filter(m => m !== formData.minor && !formData.other_minors.includes(m)).map(minor => (
                        <button key={minor} type="button" className="pef-dropdown-item" onClick={() => handleAddMinor(minor)}>{minor}</button>
                      ))}
                    </div>
                  )}
                </EditRow>

                <EditRow label={t('profile.concentration')} hint="e.g., AI/ML, Software Systems">
                  <input
                    className="pef-control"
                    type="text"
                    name="concentration"
                    value={formData.concentration}
                    onChange={handleChange}
                    placeholder="Your area of focus"
                  />
                </EditRow>
              </>
            )}
          </div>
        </section>

        <div className="pic-col">
          {/* Contact */}
          <section className="pic-group">
            <h3 className="pic-group-label">
              <FaEnvelope className="pic-group-icon" /> {t('profile.contactInfo')}
            </h3>
            <div className="pic-rows">
              <EditRow label={t('profile.username')}>
                <input
                  className="pef-control"
                  type="text"
                  name="username"
                  value={formData.username}
                  onChange={handleChange}
                  placeholder={t('profileForm.displayName')}
                />
              </EditRow>
              {user?.email && (
                <EditRow label={t('profile.email')}>
                  <span className="pef-static">
                    {user.email}
                    <span className="pic-verified"><FaCheck /> {t('profileForm.verified')}</span>
                  </span>
                </EditRow>
              )}
            </div>
          </section>

          {/* Additional */}
          <section className="pic-group">
            <h3 className="pic-group-label">
              <HiMiniSparkles className="pic-group-icon" /> {t('profile.additionalInfo')}
            </h3>
            <div className="pic-rows">
              <EditRow label={t('profile.currentGpa')} hint={t('profileForm.gpaScale')}>
                <input
                  className="pef-control pef-control--narrow"
                  type="number"
                  name="current_gpa"
                  value={formData.current_gpa}
                  onChange={handleChange}
                  step="0.01"
                  min="0"
                  max="4.0"
                  placeholder="e.g., 3.75"
                />
              </EditRow>

              <EditRow label={t('profile.academicInterests')} hint={t('profileForm.separateCommas')}>
                <textarea
                  className="pef-control"
                  name="interests"
                  value={formData.interests}
                  onChange={handleChange}
                  placeholder="e.g., Machine Learning, Web Development, Data Science"
                  rows={3}
                />
              </EditRow>

              <EditRow label={t('profileForm.advancedStanding')} hint={t('profileForm.advancedStandingDesc')}>
                <div className="pef-as">
                  {formData.advanced_standing.map((course, index) => (
                    <div key={index} className="pef-as-item">
                      <div className="pef-as-item-top">
                        <span className="pef-as-code">{course.course_code}</span>
                        {course.course_title && course.course_title !== 'None' && (
                          <span className="pef-as-title">{course.course_title}</span>
                        )}
                        <span className="pef-as-credits">{course.credits} cr</span>
                        <button
                          type="button"
                          className="pef-as-remove"
                          onClick={() => handleRemoveAdvancedCourse(index)}
                          aria-label={t('profileForm.removeCourse')}
                        >
                          ×
                        </button>
                      </div>
                      <div className="pef-as-flags">
                        <label className="pef-flag">
                          <input
                            type="checkbox"
                            checked={course.counts_toward_degree !== false}
                            onChange={() => handleToggleAdvancedFlag(index, 'counts_toward_degree')}
                          />
                          Counts toward degree
                        </label>
                        <label className="pef-flag">
                          <input
                            type="checkbox"
                            checked={!!course.counts_toward_major}
                            onChange={() => handleToggleAdvancedFlag(index, 'counts_toward_major')}
                          />
                          Counts toward major
                        </label>
                      </div>
                    </div>
                  ))}
                  <div className="pef-as-add">
                    <input
                      className="pef-control pef-control--code"
                      type="text"
                      placeholder="MATH 133"
                      value={newAdvancedCourse.course_code}
                      onChange={(e) => setNewAdvancedCourse(prev => ({ ...prev, course_code: e.target.value }))}
                    />
                    <input
                      className="pef-control pef-control--title"
                      type="text"
                      placeholder="Course title (optional)"
                      value={newAdvancedCourse.course_title}
                      onChange={(e) => setNewAdvancedCourse(prev => ({ ...prev, course_title: e.target.value }))}
                    />
                    <input
                      className="pef-control pef-control--credits"
                      type="number"
                      placeholder="cr"
                      value={newAdvancedCourse.credits}
                      onChange={(e) => setNewAdvancedCourse(prev => ({ ...prev, credits: parseInt(e.target.value) || 3 }))}
                      min="1"
                      max="12"
                    />
                    <button
                      type="button"
                      className="pef-add-btn"
                      onClick={handleAddAdvancedCourse}
                      disabled={!newAdvancedCourse.course_code.trim()}
                    >
                      {t('profileForm.addCourse')}
                    </button>
                  </div>
                </div>
              </EditRow>
            </div>
          </section>
        </div>
      </div>

      {/* Actions */}
      <div className="pef-actions">
        {onCancel && (
          <button type="button" onClick={onCancel} className="pef-btn pef-btn--ghost">
            Cancel
          </button>
        )}
        <button type="submit" className="pef-btn pef-btn--primary">
          Save Profile
        </button>
      </div>
    </form>
  )
}
