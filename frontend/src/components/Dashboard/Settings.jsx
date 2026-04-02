import { useState, useEffect } from 'react'
import { createPortal } from 'react-dom'
import {
  FaCog, FaPalette, FaBell, FaLock, FaBolt, FaGlobe,
  FaSun, FaMoon, FaSyncAlt, FaDownload,
  FaEnvelope, FaGraduationCap, FaUsers, FaUser, FaCheck,
  FaTrash, FaExclamationTriangle, FaClipboardList,
  FaNewspaper,
} from 'react-icons/fa'
import { useLanguage } from '../../contexts/LanguageContext'
import { useAuth } from '../../contexts/AuthContext'
import { useTheme } from '../../contexts/ThemeContext'
import { useTimezone, TIMEZONES } from '../../contexts/TimezoneContext'
import useNotificationPrefs from '../../hooks/useNotificationPrefs'
import './Settings.css'

export default function Settings({ user, profile, onUpdateSettings }) {
  const { language, setLanguage, t } = useLanguage()
  const { deleteAccount, authFlags, updatePassword } = useAuth()
  const { theme, setTheme } = useTheme()
  const { timezone, setTimezone } = useTimezone()

  // FIX: pass user?.id as first arg so prefs sync to Supabase
  const [notifPrefs, setNotifPrefs, syncing] = useNotificationPrefs(user?.id, user?.email)

  const [settings, setSettings] = useState({
    theme: theme || 'light',
    profileVisibility:  localStorage.getItem('profileVisibility') || 'private',
    shareProgress:      JSON.parse(localStorage.getItem('shareProgress') ?? 'false'),
    language: language || 'en',
    timezone,
  })

  const [showExportModal, setShowExportModal] = useState(false)
  const [autoSaveFlash, setAutoSaveFlash] = useState(false)
  const [showDeleteModal, setShowDeleteModal] = useState(false)
  const [deleteConfirm, setDeleteConfirm] = useState('')
  const [deleting, setDeleting] = useState(false)
  const [deleteError, setDeleteError] = useState('')

  // ── Change password state ─────────────────────────────────────────
  const [isRecoveryFlow, setIsRecoveryFlow] = useState(false)
  const [showPwModal, setShowPwModal] = useState(() => {
    // Auto-open if user arrived via a password-reset email link
    if (localStorage.getItem('symbolos_open_pw_change')) {
      localStorage.removeItem('symbolos_open_pw_change')
      return true
    }
    return false
  })

  // Mark as recovery flow so modal can't be dismissed until password is set
  useEffect(() => {
    if (showPwModal && !isRecoveryFlow) {
      const flag = sessionStorage.getItem('symbolos_recovery_flow')
      if (flag) {
        setIsRecoveryFlow(true)
        sessionStorage.removeItem('symbolos_recovery_flow')
      }
    }
  }, [showPwModal, isRecoveryFlow])

  // Lock body scroll while any modal is open (prevents scrollbar-width layout shift)
  const anyModalOpen = showPwModal || showExportModal || showDeleteModal
  useEffect(() => {
    if (anyModalOpen) {
      document.body.style.overflow = 'hidden'
    } else {
      document.body.style.overflow = ''
    }
    return () => { document.body.style.overflow = '' }
  }, [anyModalOpen])
  const [pwNew, setPwNew] = useState('')
  const [pwConfirm, setPwConfirm] = useState('')
  const [pwLoading, setPwLoading] = useState(false)
  const [pwError, setPwError] = useState('')
  const [pwSuccess, setPwSuccess] = useState(false)

  const handleChangePassword = async () => {
    setPwError('')
    if (pwNew.length < 8) { setPwError(t('settings.passwordTooShort')); return }
    if (pwNew !== pwConfirm) { setPwError(t('settings.passwordMismatch')); return }
    setPwLoading(true)
    try {
      const { error } = await updatePassword(pwNew)
      if (error) setPwError(error.message)
      else { setPwSuccess(true); setTimeout(() => { setShowPwModal(false); setPwSuccess(false); setPwNew(''); setPwConfirm('') }, 2000) }
    } finally {
      setPwLoading(false)
    }
  }

  const isMcGillEmail = authFlags?.is_mcgill_email ?? false

  const flash = () => {
    setAutoSaveFlash(true)
    setTimeout(() => setAutoSaveFlash(false), 1800)
  }

  const handleThemeChange = (v) => {
    setSettings(p => ({ ...p, theme: v }))
    setTheme(v)
    onUpdateSettings?.({ theme: v })
    flash()
  }

  const handleLanguageChange = (v) => {
    setSettings(p => ({ ...p, language: v }))
    setLanguage(v)
    onUpdateSettings?.({ language: v })
    flash()
  }

  const handleToggle = (key) => {
    const val = !settings[key]
    setSettings(p => ({ ...p, [key]: val }))
    localStorage.setItem(key, JSON.stringify(val))
    onUpdateSettings?.({ [key]: val })
    flash()
  }

  const handleSelect = (key, val) => {
    setSettings(p => ({ ...p, [key]: val }))
    localStorage.setItem(key, typeof val === 'boolean' ? JSON.stringify(val) : val)
    if (key === 'timezone') setTimezone(val)
    onUpdateSettings?.({ [key]: val })
    flash()
  }

  const setNotifMethod  = (v) => { setNotifPrefs(p => ({ ...p, method: v })); flash() }
  const toggleTiming    = (k) => { setNotifPrefs(p => ({ ...p, timing: { ...p.timing, [k]: !p.timing[k] } })); flash() }
  const toggleEventType = (k) => { setNotifPrefs(p => ({ ...p, eventTypes: { ...p.eventTypes, [k]: !p.eventTypes[k] } })); flash() }
  const setNotifPhone   = (v) => { setNotifPrefs(p => ({ ...p, phone: v })); flash() }

  const handleExportData = () => {
    const blob = new Blob([JSON.stringify({ user: { email: user?.email, id: user?.id }, profile, settings, exportDate: new Date().toISOString() }, null, 2)], { type: 'application/json' })
    const url = URL.createObjectURL(blob)
    const a = Object.assign(document.createElement('a'), { href: url, download: `mcgill-advisor-data-${new Date().toISOString().split('T')[0]}.json` })
    document.body.appendChild(a); a.click(); document.body.removeChild(a); URL.revokeObjectURL(url)
    setShowExportModal(false)
    alert(t('settings.dataExported'))
  }

  const confirmWord = t('settings.deleteConfirmPlaceholder').replace('Type ', '').replace('Tapez ', '').trim()

  const handleDeleteAccount = async () => {
    if (deleteConfirm !== confirmWord) return
    setDeleting(true)
    setDeleteError('')
    try {
      await deleteAccount()
    } catch (err) {
      setDeleteError(t('settings.deleteError'))
      setDeleting(false)
    }
  }

  const METHOD_OPTIONS = [
    { value: 'email', icon: <FaEnvelope size={16} />, label: t('settings.notifEmail') },
    { value: 'none',  icon: null,                     label: t('settings.notifNone') },
  ]

  const EVENT_TYPE_CFG = {
    exam:       { icon: <FaClipboardList />, color: '#7c3aed', bg: '#f5f3ff', label: language === 'fr' ? 'Examens finaux' : 'Final Exams' },
    academic:   { icon: <FaGraduationCap />, color: '#1d4ed8', bg: '#eff6ff', label: t('calendar.academicDates') },
    club:       { icon: <FaUsers />,         color: '#d97706', bg: '#fef3c7', label: t('calendar.clubEvents') },
    personal:   { icon: <FaUser />,          color: '#059669', bg: '#ecfdf5', label: t('calendar.personalEvents') },
    newsletter: { icon: <FaNewspaper />,     color: '#0891b2', bg: '#ecfeff', label: language === 'fr' ? 'Infolettres' : language === 'zh' ? '通讯' : 'Newsletters' },
  }

  return (
    <div className="settings-container">

      {/* Page header */}
      <div className="settings-header">
        <div className="settings-header-row">
          <div>
            <h2 className="settings-title">
              <FaCog className="settings-title-icon" /> {t('settings.title')}
            </h2>
            <p className="settings-subtitle">{t('settings.subtitle')}</p>
          </div>
          {autoSaveFlash && (
            <div className="settings-autosave-badge">
              <FaCheck size={10} /> {syncing ? 'Saving…' : t('settings.notifSaved')}
            </div>
          )}
        </div>
      </div>

      <div className="settings-sections">

        {/* ── Appearance ── */}
        <div className="settings-section">
          <div className="section-header">
            <span className="section-icon"><FaPalette /></span>
            <h3 className="section-title">{t('settings.appearance')}</h3>
          </div>
          <div className="section-content">
            <div className="setting-item">
              <div className="setting-info">
                <label className="setting-label">{t('settings.theme')}</label>
                <p className="setting-description">{t('settings.themeDescription')}</p>
              </div>
              <div className="theme-toggle">
                {[
                  { v: 'light', icon: <FaSun />,     label: t('settings.light') },
                  { v: 'dark',  icon: <FaMoon />,    label: t('settings.dark') },
                  { v: 'auto',  icon: <FaSyncAlt />, label: t('settings.auto') },
                ].map(({ v, icon, label }) => (
                  <button key={v} className={`theme-btn ${settings.theme === v ? 'active' : ''}`} onClick={() => handleThemeChange(v)}>
                    <span className="theme-btn-icon">{icon}</span> {label}
                  </button>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* ── Calendar Notification Defaults ── */}
        <div className="settings-section">
          <div className="section-header">
            <span className="section-icon"><FaBell /></span>
            <h3 className="section-title">{t('settings.calendarNotifications')}</h3>
          </div>
          <div className="section-content">

            {/* Method */}
            <div className="setting-item setting-item--block">
              <div className="setting-info">
                <label className="setting-label">{t('settings.notifMethod')}</label>
                <p className="setting-description">{t('settings.notifMethodDesc')}</p>
              </div>
              <div className="notif-method-grid">
                {METHOD_OPTIONS.map(({ value, icon, label }) => (
                  <button key={value}
                    className={`notif-method-btn ${notifPrefs.method === value ? 'active' : ''}`}
                    onClick={() => setNotifMethod(value)}>
                    {icon && <span className="notif-method-icon">{icon}</span>}
                    {label}
                    {notifPrefs.method === value && <FaCheck className="notif-method-check" />}
                  </button>
                ))}
              </div>
            </div>

            {/* Timing */}
            <div className="setting-item setting-item--block">
              <div className="setting-info">
                <label className="setting-label">{t('settings.notifTiming')}</label>
                <p className="setting-description">{t('settings.notifTimingDesc')}</p>
              </div>
              <div className="notif-timing-grid">
                {[
                  { key: 'sameDay', label: t('settings.notifSameDay') },
                  { key: 'oneDay',  label: t('settings.notifOneDay') },
                  { key: 'oneWeek', label: t('settings.notifOneWeek') },
                ].map(({ key, label }) => (
                  <label key={key} className={`notif-timing-chip ${notifPrefs.timing[key] ? 'active' : ''}`}>
                    <input type="checkbox" checked={notifPrefs.timing[key]} onChange={() => toggleTiming(key)} />
                    {notifPrefs.timing[key] && <FaCheck size={9} />} {label}
                  </label>
                ))}
              </div>
            </div>

            {/* Event types */}
            <div className="setting-item setting-item--block">
              <div className="setting-info">
                <label className="setting-label">{t('settings.notifEventTypes')}</label>
                <p className="setting-description">
                  {language === 'fr'
                    ? 'Les examens finaux sont automatiquement programmés. Décochez pour désactiver.'
                    : 'Final exams are automatically scheduled. Uncheck any type to opt out.'}
                </p>
              </div>
              <div className="notif-type-grid">
                {Object.entries(EVENT_TYPE_CFG).map(([key, cfg]) => (
                  <label key={key}
                    className={`notif-type-chip ${notifPrefs.eventTypes[key] ? 'active' : ''}`}
                    style={notifPrefs.eventTypes[key] ? { borderColor: cfg.color, background: cfg.bg, color: cfg.color } : {}}>
                    <input type="checkbox" checked={notifPrefs.eventTypes[key]} onChange={() => toggleEventType(key)} />
                    {cfg.icon} {cfg.label}
                    {notifPrefs.eventTypes[key] && <FaCheck size={9} />}
                  </label>
                ))}
              </div>
            </div>

          </div>
        </div>

        {/* ── Privacy ── */}
        <div className="settings-section">
          <div className="section-header">
            <span className="section-icon"><FaLock /></span>
            <h3 className="section-title">{t('settings.privacyData')}</h3>
          </div>
          <div className="section-content">
            <div className="setting-item">
              <div className="setting-info">
                <label className="setting-label">{t('settings.profileVisibility')}</label>
                <p className="setting-description">{t('settings.profileVisibilityDesc')}</p>
              </div>
              <div className="clubs-visibility-toggle">
                <button type="button"
                  className={`clubs-visibility-option${settings.profileVisibility === 'public' ? ' active' : ''}`}
                  onClick={() => handleSelect('profileVisibility', 'public')}>
                  <FaGlobe size={12} /> {t('settings.public')}
                </button>
                <button type="button"
                  className={`clubs-visibility-option${settings.profileVisibility !== 'public' ? ' active' : ''}`}
                  onClick={() => handleSelect('profileVisibility', 'private')}>
                  <FaLock size={11} /> {t('settings.private')}
                </button>
              </div>
            </div>
            <div className="setting-item">
              <div className="setting-info">
                <label className="setting-label">{t('settings.shareYearAndProgram')}</label>
                <p className="setting-description">{t('settings.shareYearAndProgramDesc')}</p>
              </div>
              <label className="toggle-switch">
                <input type="checkbox" checked={settings.shareProgress} onChange={() => handleSelect('shareProgress', !settings.shareProgress)} />
                <span className="toggle-slider" />
              </label>
            </div>
            <div className="setting-item">
              <div className="setting-info">
                <label className="setting-label">{t('settings.exportYourData')}</label>
                <p className="setting-description">{t('settings.exportDataDesc')}</p>
              </div>
              <button className="export-btn" onClick={() => setShowExportModal(true)}>
                <FaDownload className="export-btn-icon" /> {t('settings.exportData')}
              </button>
            </div>
          </div>
        </div>

        {/* ── Preferences ── */}
        <div className="settings-section">
          <div className="section-header">
            <span className="section-icon"><FaBolt /></span>
            <h3 className="section-title">{t('settings.preferences')}</h3>
          </div>
          <div className="section-content">
            <div className="setting-item">
              <div className="setting-info">
                <label className="setting-label">{t('settings.language')}</label>
                <p className="setting-description">{t('settings.languageDesc')}</p>
              </div>
              <select className="setting-select" value={settings.language} onChange={e => handleLanguageChange(e.target.value)}>
                <option value="en">{t('common.english')}</option>
                <option value="fr">{t('common.french')}</option>
                <option value="zh">{t('common.mandarin')}</option>
              </select>
            </div>
            <div className="setting-item">
              <div className="setting-info">
                <label className="setting-label">{t('settings.timezone')}</label>
                <p className="setting-description">{t('settings.timezoneDesc')}</p>
              </div>
              <select className="setting-select" value={settings.timezone} onChange={e => handleSelect('timezone', e.target.value)}>
                {TIMEZONES.map(({ value, label }) => (
                  <option key={value} value={value}>{label}</option>
                ))}
              </select>
            </div>
          </div>
        </div>


        {/* ── Danger Zone ── */}
        <div className="settings-section settings-section--danger">
          <div className="section-header">
            <span className="section-icon section-icon--danger"><FaExclamationTriangle /></span>
            <h3 className="section-title section-title--danger">{t('settings.dangerZone')}</h3>
          </div>
          <div className="section-content">
            <div className="setting-item">
              <div className="setting-info">
                <label className="setting-label">{t('settings.changePassword')}</label>
                <p className="setting-description">{t('settings.changePasswordDesc')}</p>
              </div>
              <button className="delete-account-btn settings-btn--primary" onClick={() => { setShowPwModal(true); setPwNew(''); setPwConfirm(''); setPwError(''); setPwSuccess(false) }}>
                <FaLock size={12} /> {t('settings.changePassword')}
              </button>
            </div>
            <div className="setting-item">
              <div className="setting-info">
                <label className="setting-label">{t('settings.deleteAccount')}</label>
                <p className="setting-description">{t('settings.deleteAccountDesc')}</p>
              </div>
              <button className="delete-account-btn" onClick={() => { setShowDeleteModal(true); setDeleteConfirm(''); setDeleteError('') }}>
                <FaTrash size={12} /> {t('settings.deleteAccountBtn')}
              </button>
            </div>
          </div>
        </div>

      </div>

      {/* Export Modal */}
      {showExportModal && createPortal(
        <div className="modal-overlay" onClick={() => setShowExportModal(false)}>
          <div className="modal-content" onClick={e => e.stopPropagation()}>
            <h3 className="modal-title">{t('settings.exportYourData')}</h3>
            <p className="modal-text">{t('settings.exportModalText')}</p>
            <div className="modal-actions">
              <button className="modal-btn cancel-btn" onClick={() => setShowExportModal(false)}>{t('common.cancel')}</button>
              <button className="modal-btn confirm-btn" onClick={handleExportData}>{t('settings.downloadJson')}</button>
            </div>
          </div>
        </div>,
        document.body
      )}

      {/* Delete Account Modal */}
      {showDeleteModal && createPortal(
        <div className="modal-overlay" onClick={() => !deleting && setShowDeleteModal(false)}>
          <div className="modal-content modal-content--danger" onClick={e => e.stopPropagation()}>
            <div className="modal-danger-icon"><FaTrash size={22} /></div>
            <h3 className="modal-title">{t('settings.deleteConfirmTitle')}</h3>
            <p className="modal-text">{t('settings.deleteConfirmText')}</p>
            <div className="modal-confirm-field">
              <label className="modal-confirm-label">{t('settings.deleteConfirmPrompt')}</label>
              <input
                className="modal-confirm-input"
                type="text"
                placeholder={t('settings.deleteConfirmPlaceholder')}
                value={deleteConfirm}
                onChange={e => setDeleteConfirm(e.target.value)}
                disabled={deleting}
                autoFocus
              />
            </div>
            {deleteError && <p className="modal-error">{deleteError}</p>}
            <div className="modal-actions">
              <button className="modal-btn cancel-btn" onClick={() => setShowDeleteModal(false)} disabled={deleting}>{t('common.cancel')}</button>
              <button
                className="modal-btn delete-confirm-btn"
                onClick={handleDeleteAccount}
                disabled={deleteConfirm !== confirmWord || deleting}
              >
                {deleting ? t('settings.deleteDeleting') : t('settings.deleteConfirmBtn')}
              </button>
            </div>
          </div>
        </div>,
        document.body
      )}

      {/* Change Password Modal */}
      {showPwModal && createPortal(
        <div className="modal-overlay" onClick={() => !isRecoveryFlow && !pwLoading && setShowPwModal(false)}>
          <div className="modal-content" onClick={e => e.stopPropagation()}>
            <h3 className="modal-title">{t('settings.changePasswordTitle')}</h3>
            {isRecoveryFlow && (
              <p className="modal-text" style={{ marginBottom: 12, fontSize: '0.85rem', color: 'var(--text-secondary)' }}>
                {t('settings.recoveryFlowNote')}
              </p>
            )}
            {pwSuccess ? (
              <p className="modal-text" style={{ color: 'var(--success-primary)' }}><FaCheck /> {t('settings.passwordUpdateSuccess')}</p>
            ) : (
              <>
                <div className="modal-confirm-field">
                  <label className="modal-confirm-label">{t('settings.newPasswordLabel')}</label>
                  <input
                    className="modal-confirm-input"
                    type="password"
                    placeholder={t('settings.passwordPlaceholder')}
                    value={pwNew}
                    onChange={e => setPwNew(e.target.value)}
                    disabled={pwLoading}
                    autoFocus
                  />
                </div>
                <div className="modal-confirm-field" style={{ marginTop: 12 }}>
                  <label className="modal-confirm-label">{t('settings.confirmPasswordLabel')}</label>
                  <input
                    className="modal-confirm-input"
                    type="password"
                    placeholder={t('settings.confirmPasswordPlaceholder')}
                    value={pwConfirm}
                    onChange={e => setPwConfirm(e.target.value)}
                    disabled={pwLoading}
                  />
                </div>
                {pwError && <p className="modal-error">{pwError}</p>}
                <div className="modal-actions">
                  {!isRecoveryFlow && (
                    <button className="modal-btn cancel-btn" onClick={() => setShowPwModal(false)} disabled={pwLoading}>{t('common.cancel')}</button>
                  )}
                  <button className="modal-btn confirm-btn" onClick={handleChangePassword} disabled={pwLoading || !pwNew || !pwConfirm}>
                    {pwLoading ? t('settings.passwordUpdating') : t('settings.updatePasswordBtn')}
                  </button>
                </div>
              </>
            )}
          </div>
        </div>,
        document.body
      )}
    </div>
  )
}
