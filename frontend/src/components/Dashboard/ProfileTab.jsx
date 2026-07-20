import { FaCamera, FaSignOutAlt, FaChevronRight } from 'react-icons/fa'
import { useLanguage } from '../../contexts/PreferencesContext'
import useViewport from '../../hooks/useViewport'
import PersonalInfoCard from './PersonalInfoCard'
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
}) {
  const { t } = useLanguage()
  const { isMobile } = useViewport()

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
          <div className="card-full-width">
            <PersonalInfoCard
              profile={profile}
              user={user}
              onUpdateProfile={updateProfile}
            />
          </div>

          {/* Settings */}
          <div className="profile-section-card card-full-width">
            <Settings
              user={user}
              profile={profile}
              onUpdateSettings={(settings) => console.log('Settings updated:', settings)}
            />
          </div>

          {/* Sign Out.
              On mobile this is a single destructive action, which is exactly
              what a one-row grouped list is for — a title/description/button
              card here would be the last piece of web chrome on the screen. */}
          {isMobile ? (
            <div className="card-full-width">
              <div className="m-group profile-signout-group">
                <button
                  type="button"
                  className="m-row m-row--tappable profile-signout-row"
                  onClick={signOut}
                >
                  <FaSignOutAlt className="profile-signout-icon" />
                  <span className="profile-signout-label">{t('sidebar.signOut')}</span>
                  <FaChevronRight className="profile-signout-chev" size={12} />
                </button>
              </div>
            </div>
          ) : (
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
          )}
        </div>
      </div>
    </div>
  )
}
