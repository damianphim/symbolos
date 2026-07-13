import { FaCamera, FaChartBar, FaBullseye, FaLightbulb, FaFileUpload } from 'react-icons/fa'
import { useLanguage } from '../../contexts/PreferencesContext'
import PersonalInfoCard from './PersonalInfoCard'
import DegreeProgressTracker from './DegreeProgressTracker'
import GPATrendChart from './GPATrendChart'
import Settings from './Settings'
import './ProfileTab.css'

export default function ProfileTab({
  user,
  profile,
  updateProfile,
  signOut,
  // Image
  profileImage,
  isUploadingImage,
  fileInputRef,
  handleImageUpload,
  handleAvatarClick,
  // Data
  completedCourses,
}) {
  const { t } = useLanguage()
  
  return (
    <div className="profile-page">
      <div className="profile-page-header">
        <div className="profile-hero">
          <div className="profile-avatar-section">
            <div className="profile-avatar-xl-wrapper" onClick={handleAvatarClick}>
              {profileImage ? (
                <img src={profileImage} alt="Profile" className="profile-avatar-xl-image" />
              ) : (
                <div className="profile-avatar-xl">
                  {user?.email?.[0].toUpperCase()}
                </div>
              )}
              <div className="avatar-xl-overlay">
                <FaCamera className="camera-xl-icon" />
                <span className="overlay-xl-text">{t('profile.changePhoto')}</span>
              </div>
              {isUploadingImage && (
                <div className="avatar-xl-loading">
                  <div className="spinner-xl"></div>
                </div>
              )}
            </div>
            <input
              ref={fileInputRef}
              type="file"
              accept="image/*"
              onChange={handleImageUpload}
              style={{ display: 'none' }}
            />
            <div className="profile-hero-info">
              <h1 className="profile-display-name">{profile?.username || t('profile.mcgillStudent')}</h1>
              <div className="profile-badges">
                <span className="badge badge-year">
                  {profile?.year ?
                    t('profile.yearLabel').replace('{year}', profile.year) : t('profile.yearNotSet')}
                </span>
                {profile?.major && (
                  <span className="badge badge-major">{profile.major}</span>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="profile-content">
        <div className="profile-grid">
          {/* Personal Information Card */}
          <div className="profile-card-main">
            <PersonalInfoCard
              profile={profile}
              user={user}
              onUpdateProfile={updateProfile}
            />
          </div>

          {/* Academic Performance Card */}
          <div className="profile-section-card profile-card-sidebar">
            <div className="card-header">
              <div className="card-title-group">
                <span className="card-icon"><FaChartBar /></span>
                <h2 className="card-title">{t('profile.academicPerformance')}</h2>
              </div>
            </div>
            <div className="card-content">
              <div className="stat-showcase">
                <div className="stat-item">
                  <div className="stat-value-large">{profile?.current_gpa || '--'}</div>
                  <div className="stat-label">{t('profile.currentGpa')}</div>
                </div>
              </div>
              <div className="performance-tips">
                <div className="tip-item">
                  <span className="tip-icon"><FaLightbulb /></span>
                  <p className="tip-text">{t('profile.gpaTip')}</p>
                </div>
              </div>
              <GPATrendChart
                completedCourses={completedCourses}
                currentGPA={profile?.current_gpa}
              />
            </div>
          </div>

          {/* Settings */}
          <div className="profile-section-card card-full-width">
            <Settings
              user={user}
              profile={profile}
              onUpdateSettings={(settings) => console.log('Settings updated:', settings)}
            />
          </div>

          {/* Sign Out */}
          <div className="profile-section-card card-full-width">
            <div className="card-content">
              <div className="sign-out-section">
                <div className="sign-out-info">
                  <h3 className="sign-out-title">{t('profile.signOutTitle')}</h3>
                  <p className="sign-out-description">{t('profile.signOutDescription')}</p>
                </div>
                <button className="btn btn-secondary" onClick={signOut}>
                  {t('sidebar.signOut')}
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
