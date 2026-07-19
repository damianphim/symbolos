import { useState } from 'react'
import { FaEdit, FaCheck, FaUser, FaEnvelope, FaGraduationCap } from 'react-icons/fa'
import { HiMiniSparkles } from 'react-icons/hi2'
import { useLanguage } from '../../contexts/PreferencesContext'
import EnhancedProfileForm from './EnhancedProfileForm'
import './PersonalInfoCard.css'

/** One aligned label/value row of the definition list. */
function InfoRow({ label, children }) {
  return (
    <div className="pic-row">
      <span className="pic-row-label">{label}</span>
      <span className="pic-row-value">{children}</span>
    </div>
  )
}

export default function PersonalInfoCard({ profile, user, onUpdateProfile }) {
  const { t } = useLanguage()
  const [isEditing, setIsEditing] = useState(false)
  const [saveError, setSaveError] = useState(null)

  // Calculate profile completeness
  const calculateCompleteness = () => {
    const fields = [
      'username', 'major', 'year', 'faculty',
      'interests', 'concentration'
    ]
    const completed = fields.filter(field => profile?.[field]).length
    return Math.round((completed / fields.length) * 100)
  }

  const completeness = calculateCompleteness()
  const muted = (text) => <span className="pic-muted">{text}</span>

  return (
    <div className="pic-card">
      {/* Header */}
      <div className="pic-header">
        <div className="pic-header-left">
          <span className="pic-header-icon"><FaUser /></span>
          <div className="pic-header-text">
            <h2 className="pic-title">{t('profile.personalInfo')}</h2>
            <p className="pic-subtitle">{t('profile.manageDetails')}</p>
          </div>
        </div>
        {!isEditing && (
          <button
            className="pic-edit-btn"
            onClick={() => { setSaveError(null); setIsEditing(true) }}
          >
            <FaEdit /> {t('profile.editProfile')}
          </button>
        )}
      </div>

      {/* Profile completeness */}
      <div className="pic-progress">
        <span className="pic-progress-label">{t('profile.completeness')}</span>
        <div className="pic-progress-bar">
          <div
            className="pic-progress-fill"
            style={{
              width: `${completeness}%`,
              background: completeness === 100
                ? 'linear-gradient(90deg, #10b981, #059669)'
                : 'linear-gradient(90deg, var(--accent-primary), #c91625)'
            }}
          />
        </div>
        <span className="pic-progress-pct">{completeness}%</span>
      </div>

      {saveError && !isEditing && (
        <div className="pic-error">
          {saveError},{' '}
          <button className="pic-error-retry" onClick={() => setIsEditing(true)}>
            {t('profile.editProfile')}
          </button>
        </div>
      )}

      {!isEditing ? (
        <div className="pic-body">
          {/* Academic */}
          <section className="pic-group">
            <h3 className="pic-group-label">
              <FaGraduationCap className="pic-group-icon" /> {t('profile.academicInfo')}
            </h3>
            <div className="pic-rows">
              <InfoRow label={t('profile.major')}>
                {profile?.major
                  ? <>{profile.major}{profile?.is_honours && <span className="pic-honours">Honours</span>}</>
                  : muted(t('profile.notSpecified'))}
              </InfoRow>

              {profile?.other_majors?.length > 0 && (
                <InfoRow label={t('profile.additionalMajors')}>
                  {profile.other_majors.map((major, idx) => (
                    <span key={idx} className="pic-tag pic-tag--major">{major}</span>
                  ))}
                </InfoRow>
              )}

              {profile?.minor && (
                <InfoRow label={t('profile.primaryMinor')}>{profile.minor}</InfoRow>
              )}

              {profile?.other_minors?.length > 0 && (
                <InfoRow label={t('profile.additionalMinors')}>
                  {profile.other_minors.map((minor, idx) => (
                    <span key={idx} className="pic-tag pic-tag--minor">{minor}</span>
                  ))}
                </InfoRow>
              )}

              {profile?.concentration && (
                <InfoRow label={t('profile.concentration')}>{profile.concentration}</InfoRow>
              )}

              <InfoRow label={t('profile.faculty')}>
                {profile?.faculty || muted(t('profile.notSpecified'))}
              </InfoRow>

              <InfoRow label={t('profile.year')}>
                {profile?.year
                  ? <span className="pic-year">U{profile.year}</span>
                  : muted(t('profile.notSpecified'))}
              </InfoRow>
            </div>
          </section>

          <div className="pic-col">
            {/* Contact */}
            <section className="pic-group">
              <h3 className="pic-group-label">
                <FaEnvelope className="pic-group-icon" /> {t('profile.contactInfo')}
              </h3>
              <div className="pic-rows">
                <InfoRow label={t('profile.username')}>
                  {profile?.username || muted(t('profile.notSet'))}
                </InfoRow>
                <InfoRow label={t('profile.email')}>
                  {user?.email}
                  <span className="pic-verified"><FaCheck /> {t('profileForm.verified')}</span>
                </InfoRow>
              </div>
            </section>

            {/* Additional */}
            <section className="pic-group">
              <h3 className="pic-group-label">
                <HiMiniSparkles className="pic-group-icon" /> {t('profile.additionalInfo')}
              </h3>
              <div className="pic-rows">
                <InfoRow label={t('profile.academicInterests')}>
                  {profile?.interests
                    ? profile.interests.split(',').map((interest, idx) => (
                        <span key={idx} className="pic-tag pic-tag--interest">{interest.trim()}</span>
                      ))
                    : muted(t('profileForm.noInterestsAdded'))}
                </InfoRow>

                {profile?.advanced_standing?.length > 0 && (
                  <InfoRow
                    label={
                      <>
                        {t('profileForm.advancedStanding')}
                        <span className="pic-credits-badge">
                          {profile.advanced_standing.reduce((sum, c) => sum + (c.credits || 0), 0)} {t('profileForm.credits').toLowerCase()}
                        </span>
                      </>
                    }
                  >
                    {profile.advanced_standing.map((course, idx) => (
                      <span key={idx} className="pic-chip">
                        <strong>{course.course_code}</strong> {course.credits} cr
                      </span>
                    ))}
                  </InfoRow>
                )}
              </div>
            </section>
          </div>
        </div>
      ) : (
        <div className="pic-edit-wrap">
          {saveError && (
            <div className="pic-error pic-error--inline">{saveError}</div>
          )}
          <EnhancedProfileForm
            profile={profile}
            user={user}
            onSave={(formData) => {
              // Optimistic: updateProfile paints the new values synchronously,
              // so we can drop straight back to the read view with no spinner
              // or artificial delay. The network save runs in the background;
              // if it fails we reopen the form and show the error.
              setSaveError(null)
              setIsEditing(false)
              Promise.resolve(onUpdateProfile(formData))
                .then(result => {
                  if (result?.error) {
                    setSaveError(t('profile.saveFailed') || 'Could not save changes. Please try again.')
                    setIsEditing(true)
                  }
                })
                .catch(() => {
                  setSaveError(t('profile.saveFailed') || 'Could not save changes. Please try again.')
                  setIsEditing(true)
                })
            }}
            onCancel={() => setIsEditing(false)}
          />
        </div>
      )}
    </div>
  )
}
