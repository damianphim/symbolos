import { useState, useRef, useEffect } from 'react'
import {
  FaChevronRight, FaComments, FaBook,
  FaUser, FaCog, FaPalette, FaSignOutAlt, FaCalendarAlt,
  FaGraduationCap, FaUsers, FaExpandAlt, FaInfoCircle, FaShieldAlt, FaFileAlt
} from 'react-icons/fa'
import { MdLanguage } from 'react-icons/md'
import { useTheme } from '../../contexts/ThemeContext'
import { useLanguage } from '../../contexts/LanguageContext'
import PrivacyPolicy from '../Legal/PrivacyPolicy'
import TermsOfService from '../Legal/TOS'
import AboutUs from '../Legal/AboutUs'
import './Sidebar.css'

const NAV_ITEMS = (t) => [
  { key: 'chat',      icon: <FaComments />,     label: t('nav.chat') },
  { key: 'favorites', icon: <FaGraduationCap />, label: t('nav.degreePlanning') },
  { key: 'courses',   icon: <FaBook />,          label: t('nav.courses') },
  { key: 'calendar',  icon: <FaCalendarAlt />,   label: t('nav.calendar') },
  { key: 'clubs',     icon: <FaUsers />,         label: t('nav.clubs') },
  { key: 'forum',     icon: <FaComments />,      label: t('nav.forum') },
  { key: 'profile',   icon: <FaUser />,          label: t('nav.profile') },
]

export default function Sidebar({
  sidebarOpen, setSidebarOpen,
  activeTab, onTabChange,
  user, profile, profileImage, onSignOut,
}) {
  const [popupOpen, setPopupOpen] = useState(false)
  const [isMounted, setIsMounted] = useState(sidebarOpen)
  const [legalModal, setLegalModal] = useState(null) // 'privacy' | 'terms' | 'about'
  const popupRef   = useRef(null)
  const triggerRef = useRef(null)

  const { theme, setTheme } = useTheme()
  const { language, setLanguage, t } = useLanguage()

  // Handle delayed unmount for exit animation
  useEffect(() => {
    if (sidebarOpen) {
      setIsMounted(true)
    } else {
      setPopupOpen(false)
      // Keep mounted long enough for the exit animation (200ms)
      const timer = setTimeout(() => setIsMounted(false), 220)
      return () => clearTimeout(timer)
    }
  }, [sidebarOpen])

  useEffect(() => {
    if (!popupOpen) return
    const handler = (e) => {
      if (
        popupRef.current   && !popupRef.current.contains(e.target) &&
        triggerRef.current && !triggerRef.current.contains(e.target)
      ) setPopupOpen(false)
    }
    document.addEventListener('mousedown', handler)
    return () => document.removeEventListener('mousedown', handler)
  }, [popupOpen])

  const themeLabel = theme === 'light' ? t('settings.light') : theme === 'dark' ? t('settings.dark') : t('settings.auto')

  const handleSettingsClick = () => {
    setPopupOpen(false)
    onTabChange('profile')
    setTimeout(() => {
      const el = document.querySelector('.settings-container')
      if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' })
    }, 150)
  }

  const handleLanguageToggle = () => {
    const next = language === 'en' ? 'fr' : language === 'fr' ? 'zh' : 'en'
    setLanguage(next)
    setPopupOpen(false)
  }

  const cycleTheme = () => setTheme(theme === 'light' ? 'dark' : theme === 'dark' ? 'auto' : 'light')

  const navItems = NAV_ITEMS(t)
  const avatarLetter = user?.email?.[0].toUpperCase()

  return (
    <>
      {/* ── Legal modals ── */}
      {legalModal === 'privacy' && <PrivacyPolicy onClose={() => setLegalModal(null)} />}
      {legalModal === 'terms'   && <TermsOfService onClose={() => setLegalModal(null)} />}
      {legalModal === 'about'   && <AboutUs onClose={() => setLegalModal(null)} />}
      <aside className={`sidebar ${sidebarOpen ? 'sidebar--open' : 'sidebar--mini'}`}>

        {/* ── OPEN: full sidebar with animated content ── */}
        {isMounted && (
          <div className={`sidebar-content ${sidebarOpen ? 'sidebar-content--visible' : 'sidebar-content--hidden'}`}>
            <div className="sidebar-header">
              <div className="logo-container">
                <div className="logo-icon">SY</div>
                <span className="logo-name">Symbolos</span>
              </div>
              <button className="sidebar-collapse-btn" onClick={() => setSidebarOpen(false)} title="Collapse">
                <FaChevronRight size={12} style={{ transform: 'rotate(180deg)' }} />
              </button>
            </div>

            <nav className="sidebar-nav">
              {navItems.map(({ key, icon, label }, index) => (
                <button
                  key={key}
                  className={`nav-item ${activeTab === key ? 'active' : ''}`}
                  onClick={() => onTabChange(key)}
                  style={{ '--nav-index': index }}
                >
                  <span className="nav-icon">{icon}</span>
                  <span className="nav-label">{label}</span>
                </button>
              ))}
            </nav>

            <div className="sidebar-footer">
              {popupOpen && (
                <div className="sidebar-popup" ref={popupRef}>
                  <button className="sidebar-popup-item" onClick={handleSettingsClick}>
                    <span className="sidebar-popup-icon"><FaCog /></span>
                    <span className="sidebar-popup-label">{t('sidebar.settings')}</span>
                  </button>
                  <button className="sidebar-popup-item" onClick={handleLanguageToggle}>
                    <span className="sidebar-popup-icon"><MdLanguage /></span>
                    <span className="sidebar-popup-label">{language === 'en' ? 'Français' : language === 'fr' ? '中文' : 'English'}</span>
                  </button>
                  <button className="sidebar-popup-item" onClick={cycleTheme}>
                    <span className="sidebar-popup-icon"><FaPalette /></span>
                    <span className="sidebar-popup-label">{t('sidebar.colorTheme')}: {themeLabel}</span>
                  </button>
                  <div className="sidebar-popup-divider" />
                  <button className="sidebar-popup-item" onClick={() => { setPopupOpen(false); setLegalModal('about') }}>
                    <span className="sidebar-popup-icon"><FaInfoCircle /></span>
                    <span className="sidebar-popup-label">About Symbolos</span>
                  </button>
                  <button className="sidebar-popup-item" onClick={() => { setPopupOpen(false); setLegalModal('privacy') }}>
                    <span className="sidebar-popup-icon"><FaShieldAlt /></span>
                    <span className="sidebar-popup-label">Privacy Policy</span>
                  </button>
                  <button className="sidebar-popup-item" onClick={() => { setPopupOpen(false); setLegalModal('terms') }}>
                    <span className="sidebar-popup-icon"><FaFileAlt /></span>
                    <span className="sidebar-popup-label">Terms of Service</span>
                  </button>
                  <div className="sidebar-popup-divider" />
                  <button className="sidebar-popup-item sidebar-popup-item--danger" onClick={() => { setPopupOpen(false); onSignOut() }}>
                    <span className="sidebar-popup-icon"><FaSignOutAlt /></span>
                    <span className="sidebar-popup-label">{t('sidebar.logOut')}</span>
                  </button>
                  <div className="sidebar-popup-arrow" />
                </div>
              )}
              <div className="sidebar-not-affiliated">{t('rsb.notAffiliated')}</div>
              {/* Legal links row */}
              <div className="sidebar-legal-links">
                <button className="sidebar-legal-link" onClick={() => setLegalModal('privacy')}>Privacy</button>
                <span className="sidebar-legal-sep">·</span>
                <button className="sidebar-legal-link" onClick={() => setLegalModal('terms')}>Terms</button>
                <span className="sidebar-legal-sep">·</span>
                <button className="sidebar-legal-link" onClick={() => setLegalModal('about')}>About</button>
              </div>
              <button className="user-info" ref={triggerRef} onClick={() => setPopupOpen(p => !p)}>
                <div className="user-avatar">
                  {profileImage ? <img src={profileImage} alt="Profile" className="user-avatar-image" /> : avatarLetter}
                </div>
                <div className="user-details">
                  <div className="user-name">{profile?.username || t('common.user')}</div>
                  <div className="user-email">{user?.email}</div>
                </div>
              </button>
            </div>
          </div>
        )}

        {/* ── MINI: icon pills inside ONE shared capsule outline ── */}
        {!sidebarOpen && !isMounted && (
          <div className="mini-rail">
            <div className="mini-capsule">
              {navItems.map(({ key, icon, label }, index) => (
                <button
                  key={key}
                  className={`mini-pill ${activeTab === key ? 'mini-pill--active' : ''}`}
                  onClick={() => onTabChange(key)}
                  title={label}
                  style={{ '--pill-index': index }}
                >
                  {icon}
                </button>
              ))}
              <div className="mini-capsule-divider" />
              <button
                className="mini-pill mini-pill--lang"
                onClick={handleLanguageToggle}
                title={language === 'en' ? 'Passer en français' : language === 'fr' ? '切换到中文' : 'Switch to English'}
              >
                <span style={{ fontSize: '0.7rem', fontWeight: 700, letterSpacing: '-0.5px' }}>
                  {language === 'en' ? 'FR' : language === 'fr' ? '中' : 'EN'}
                </span>
              </button>
            </div>
            <button
              className="mini-expand-btn"
              onClick={() => setSidebarOpen(true)}
              title="Expand sidebar"
            >
              <FaExpandAlt size={13} />
            </button>
          </div>
        )}
      </aside>

      {/* Overlay with fade animation */}
      <div
        className={`sidebar-overlay ${sidebarOpen ? 'sidebar-overlay--visible' : ''}`}
        onClick={() => setSidebarOpen(false)}
      />
    </>
  )
}
