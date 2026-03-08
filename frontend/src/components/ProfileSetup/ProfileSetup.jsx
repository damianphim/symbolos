import { useState, useRef } from 'react'
import { useAuth } from '../../contexts/AuthContext'
import { useLanguage } from '../../contexts/LanguageContext'
import { useTheme } from '../../contexts/ThemeContext'
import { usersAPI } from '../../lib/api'
import { supabase } from '../../lib/supabase'

/** Returns { Authorization: 'Bearer <token>' } for the current session. */
async function getAuthHeaders() {
  const { data: { session } } = await supabase.auth.getSession()
  if (!session?.access_token) return {}
  return { Authorization: `Bearer ${session.access_token}` }
}
import {
  FaGraduationCap, FaFileUpload, FaCheckCircle,
  FaExclamationTriangle, FaArrowRight, FaLightbulb, FaSpinner,
  FaTimes, FaCloudUploadAlt, FaCheck, FaBook, FaCalendarAlt,
  FaChalkboardTeacher, FaPlus,
} from 'react-icons/fa'
import './ProfileSetup.css'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'
const BASE_URL = API_URL.replace(/\/api\/?$/, '').replace(/\/$/, '')

export default function ProfileSetup() {
  const { user, completeOnboarding } = useAuth()
  const { t, language, setLanguage } = useLanguage()
  const { theme, setTheme, resolvedTheme } = useTheme()

  const [step, setStep] = useState('transcript')

  // ── Transcript ─────────────────────────────────────────
  const [txStep, setTxStep]       = useState('idle')
  const [dragOver, setDragOver]   = useState(false)
  const [file, setFile]           = useState(null)
  const [txError, setTxError]     = useState('')
  const [txResults, setTxResults] = useState(null)
  const fileRef = useRef(null)

  // ── Syllabi ────────────────────────────────────────────
  const [sylStep, setSylStep]         = useState('idle')
  const [sylFiles, setSylFiles]       = useState([])
  const [sylDragOver, setSylDragOver] = useState(false)
  const [sylError, setSylError]       = useState('')
  const [sylResults, setSylResults]   = useState(null)
  const sylFileRef = useRef(null)

  const [finishing, setFinishing] = useState(false)

  const finish = async () => {
    setFinishing(true)
    await completeOnboarding()
  }

  const ensureUser = async () => {
    try {
      await usersAPI.createUser({ id: user.id, email: user.email })
    } catch (err) {
      if (err.response?.status !== 409 && err.response?.data?.code !== 'user_already_exists') {
        console.warn('Could not ensure profile row:', err)
      }
    }
  }

  // ── Transcript helpers ─────────────────────────────────
  const pickFile = (f) => {
    if (!f) return
    if (!f.name.toLowerCase().endsWith('.pdf')) { setTxError(t('ps.txPdfOnly')); return }
    if (f.size > 10 * 1024 * 1024) { setTxError(t('ps.txTooLarge')); return }
    setTxError('')
    setFile(f)
  }

  const handleDrop = (e) => {
    e.preventDefault()
    setDragOver(false)
    pickFile(e.dataTransfer.files[0])
  }

  const handleUpload = async () => {
    if (!file) return
    await ensureUser()
    setTxStep('uploading')
    setTxError('')
    try {
      const form = new FormData()
      form.append('file', file)
      form.append('dry_run', 'false')
      const res = await fetch(`${BASE_URL}/api/transcript/parse/${user.id}`, { method: 'POST', headers: await getAuthHeaders(), body: form })
      if (!res.ok) {
        const data = await res.json().catch(() => ({}))
        throw new Error(data.detail || `Upload failed (${res.status})`)
      }
      const data = await res.json()
      setTxResults(data.results)
      setTxStep('done')
    } catch (err) {
      setTxError(err.message)
      setTxStep('error')
    }
  }

  // ── Syllabi helpers ────────────────────────────────────
  const pickSylFiles = (fileList) => {
    const valid = []
    for (const f of fileList) {
      if (!f.name.toLowerCase().endsWith('.pdf')) continue
      if (f.size > 15 * 1024 * 1024) continue
      valid.push(f)
    }
    if (valid.length === 0) { setSylError(t('ps.sylPdfOnly')); return }
    setSylError('')
    setSylFiles(prev => {
      const existing = new Set(prev.map(f => f.name))
      return [...prev, ...valid.filter(f => !existing.has(f.name))]
    })
  }

  const handleSylDrop = (e) => {
    e.preventDefault()
    setSylDragOver(false)
    pickSylFiles(Array.from(e.dataTransfer.files))
  }

  const removeSylFile = (name) => {
    setSylFiles(prev => prev.filter(f => f.name !== name))
  }

  const handleSylUpload = async () => {
    if (sylFiles.length === 0) return
    setSylStep('uploading')
    setSylError('')
    try {
      const form = new FormData()
      sylFiles.forEach(f => form.append('files', f))
      form.append('dry_run', 'false')
      const res = await fetch(`${BASE_URL}/api/syllabus/parse/${user.id}`, { method: 'POST', headers: await getAuthHeaders(), body: form })
      if (!res.ok) {
        const data = await res.json().catch(() => ({}))
        throw new Error(data.detail || `Upload failed (${res.status})`)
      }
      const data = await res.json()
      setSylResults(data)
      setSylStep('done')
    } catch (err) {
      setSylError(err.message)
      setSylStep('error')
    }
  }

  const cycleTheme = () => setTheme(resolvedTheme === 'dark' ? 'light' : 'dark')

  const stepOrder = ['transcript', 'syllabus']
  const stepIdx = stepOrder.indexOf(step)

  const StepBar = () => (
    <div className="ps-stepbar">
      <div className={`ps-stepbar-item ${stepIdx === 0 ? 'active' : 'done'}`}>
        <div className="ps-stepbar-dot">
          {stepIdx > 0 ? <FaCheck size={10} /> : <span>1</span>}
        </div>
        <span className="ps-stepbar-label">{t('ps.stepTranscript')}</span>
      </div>
      <div className={`ps-stepbar-line ${stepIdx > 0 ? 'filled' : ''}`} />
      <div className={`ps-stepbar-item ${stepIdx === 1 ? 'active' : stepIdx > 1 ? 'done' : ''}`}>
        <div className="ps-stepbar-dot">
          {stepIdx > 1 ? <FaCheck size={10} /> : <span>2</span>}
        </div>
        <span className="ps-stepbar-label">{t('ps.stepSyllabi')}</span>
      </div>
    </div>
  )

  // ── Corner controls (language + theme) ────────────────
  const CornerControls = () => (
    <div className="ps-corner-controls">
      <button
        className="ps-corner-btn"
        onClick={() => setLanguage(language === 'en' ? 'fr' : 'en')}
        title={t('auth.langToggle')}
      >
        {language === 'en' ? 'FR' : 'EN'}
      </button>
      <button
        className="ps-corner-btn"
        onClick={cycleTheme}
        title={resolvedTheme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode'}
      >
        {resolvedTheme === 'dark' ? '☀' : '☽'}
      </button>
    </div>
  )

  // ══════════════════════════════════════════════════════
  // Step 1: Transcript
  // ══════════════════════════════════════════════════════
  if (step === 'transcript') {
    return (
      <div className="ps-page">
        <CornerControls />
        <div className="ps-container">
          <div className="ps-header">
            <div className="ps-header-icon ps-header-icon--green"><FaGraduationCap /></div>
            <div>
              <h1 className="ps-title">{t('ps.txTitle')}</h1>
              <p className="ps-subtitle">{t('ps.txSubtitle')}</p>
            </div>
          </div>
          <StepBar />

          {txStep === 'idle' && (
            <>
              <div
                className={`ps-dropzone ${dragOver ? 'ps-dropzone--over' : ''} ${file ? 'ps-dropzone--has-file' : ''}`}
                onDragOver={e => { e.preventDefault(); setDragOver(true) }}
                onDragLeave={() => setDragOver(false)}
                onDrop={handleDrop}
                onClick={() => !file && fileRef.current?.click()}
              >
                <input ref={fileRef} type="file" accept=".pdf" style={{ display: 'none' }}
                  onChange={e => pickFile(e.target.files[0])} />
                {file ? (
                  <div className="ps-dropzone-file">
                    <FaCheckCircle className="ps-dropzone-check" />
                    <div>
                      <p className="ps-dropzone-filename">{file.name}</p>
                      <p className="ps-dropzone-filesize">{(file.size / 1024).toFixed(0)} KB</p>
                    </div>
                    <button className="ps-dropzone-remove" onClick={e => { e.stopPropagation(); setFile(null) }}>
                      <FaTimes />
                    </button>
                  </div>
                ) : (
                  <div className="ps-dropzone-empty">
                    <FaCloudUploadAlt className="ps-dropzone-icon" />
                    <p className="ps-dropzone-main">{t('ps.dropTranscript')}</p>
                    <p className="ps-dropzone-sub">{t('ps.dropBrowse')}</p>
                  </div>
                )}
              </div>

              {txError && (
                <div className="ps-alert ps-alert--error">
                  <FaExclamationTriangle className="ps-alert-icon" />
                  <span>{txError}</span>
                </div>
              )}

              <div className="ps-actions">
                <button className="ps-btn ps-btn--primary" onClick={handleUpload} disabled={!file}>
                  {t('ps.importTranscript')} <FaArrowRight />
                </button>
                <button className="ps-btn ps-btn--ghost" onClick={async () => { await ensureUser(); setStep('syllabus') }}>
                  {t('ps.skipForNow')}
                </button>
              </div>
              <div className="ps-hint">
                <FaLightbulb className="ps-hint-icon" />
                <p>{t('ps.hintTranscriptPre')}<strong>{t('ps.hintTranscriptBold1')}</strong>{t('ps.hintTranscriptMid')}<strong>{t('ps.hintTranscriptBold2')}</strong>{t('ps.hintTranscriptPost')}</p>
              </div>
            </>
          )}

          {txStep === 'uploading' && (
            <div className="ps-status">
              <div className="ps-status-icon ps-status-icon--spin"><FaSpinner /></div>
              <h3 className="ps-status-title">{t('ps.txUploading')}</h3>
              <p className="ps-status-sub">{t('ps.txUploadingSub')}</p>
            </div>
          )}

          {txStep === 'done' && txResults && (
            <div className="ps-status">
              <div className="ps-status-icon ps-status-icon--success"><FaCheckCircle /></div>
              <h3 className="ps-status-title">{t('ps.txDone')}</h3>
              <p className="ps-status-sub">{t('ps.txDoneSub')}</p>
              <div className="ps-chips">
                {txResults.completed_added > 0 && (
                  <div className="ps-chip">
                    <span className="ps-chip-num">{txResults.completed_added}</span>
                    <span className="ps-chip-label">{t('ps.txCompletedLabel')}</span>
                  </div>
                )}
                {txResults.current_added > 0 && (
                  <div className="ps-chip">
                    <span className="ps-chip-num">{txResults.current_added}</span>
                    <span className="ps-chip-label">{t('ps.txCurrentLabel')}</span>
                  </div>
                )}
                {txResults.profile_updated && (
                  <div className="ps-chip ps-chip--success">
                    <FaCheck className="ps-chip-check" />
                    <span className="ps-chip-label">{t('ps.txProfileUpdated')}</span>
                  </div>
                )}
              </div>
              <button className="ps-btn ps-btn--primary" onClick={() => setStep('syllabus')}>
                {t('ps.continueSyllabi')} <FaArrowRight />
              </button>
            </div>
          )}

          {txStep === 'error' && (
            <div className="ps-status">
              <div className="ps-status-icon ps-status-icon--warning"><FaExclamationTriangle /></div>
              <h3 className="ps-status-title">{t('ps.txError')}</h3>
              <p className="ps-status-sub">{txError}</p>
              <div className="ps-actions ps-actions--center">
                <button className="ps-btn ps-btn--secondary" onClick={() => { setTxStep('idle'); setTxError('') }}>{t('ps.tryAgain')}</button>
                <button className="ps-btn ps-btn--ghost" onClick={() => setStep('syllabus')}>
                  {t('ps.skipSyllabi')}
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    )
  }

  // ══════════════════════════════════════════════════════
  // Step 2: Syllabi
  // ══════════════════════════════════════════════════════
  return (
    <div className="ps-page">
      <CornerControls />
      <div className="ps-container">
        <div className="ps-header">
          <div className="ps-header-icon ps-header-icon--blue"><FaBook /></div>
          <div>
            <h1 className="ps-title">{t('ps.sylTitle')}</h1>
            <p className="ps-subtitle">{t('ps.sylSubtitle')}</p>
          </div>
        </div>
        <StepBar />

        {sylStep === 'idle' && (
          <>
            <div className="ps-syl-info">
              <div className="ps-syl-info-item">
                <FaCalendarAlt className="ps-syl-info-icon" />
                <span>{t('ps.sylInfo1')}</span>
              </div>
              <div className="ps-syl-info-item">
                <FaChalkboardTeacher className="ps-syl-info-icon" />
                <span>{t('ps.sylInfo2')}</span>
              </div>
              <div className="ps-syl-info-item">
                <FaCheck className="ps-syl-info-icon ps-syl-info-icon--green" />
                <span>{t('ps.sylInfo3')}</span>
              </div>
            </div>

            <div
              className={`ps-dropzone ps-dropzone--multi ${sylDragOver ? 'ps-dropzone--over' : ''}`}
              onDragOver={e => { e.preventDefault(); setSylDragOver(true) }}
              onDragLeave={() => setSylDragOver(false)}
              onDrop={handleSylDrop}
              onClick={() => sylFileRef.current?.click()}
            >
              <input ref={sylFileRef} type="file" accept=".pdf" multiple style={{ display: 'none' }}
                onChange={e => pickSylFiles(Array.from(e.target.files))} />
              <FaCloudUploadAlt className="ps-dropzone-icon" />
              <p className="ps-dropzone-main">{t('ps.dropSyllabi')}</p>
              <p className="ps-dropzone-sub">{t('ps.dropSyllabiSub')}</p>
            </div>

            {sylFiles.length > 0 && (
              <div className="ps-syl-filelist">
                {sylFiles.map(f => (
                  <div key={f.name} className="ps-syl-filerow">
                    <FaBook className="ps-syl-filerow-icon" />
                    <span className="ps-syl-filerow-name">{f.name}</span>
                    <span className="ps-syl-filerow-size">{(f.size / 1024).toFixed(0)} KB</span>
                    <button className="ps-syl-filerow-remove" onClick={() => removeSylFile(f.name)}>
                      <FaTimes />
                    </button>
                  </div>
                ))}
                <button className="ps-syl-add-more" onClick={() => sylFileRef.current?.click()}>
                  <FaPlus /> {t('ps.addMore')}
                </button>
              </div>
            )}

            {sylError && (
              <div className="ps-alert ps-alert--error">
                <FaExclamationTriangle className="ps-alert-icon" />
                <span>{sylError}</span>
              </div>
            )}

            <div className="ps-actions">
              <button className="ps-btn ps-btn--primary" onClick={handleSylUpload} disabled={sylFiles.length === 0}>
                {sylFiles.length > 1
                  ? t('ps.importSyllabiCount').replace('{count}', sylFiles.length)
                  : sylFiles.length === 1
                  ? t('ps.importSyllabusCount').replace('{count}', 1)
                  : t('ps.importSyllabi')} <FaArrowRight />
              </button>
              <button className="ps-btn ps-btn--ghost" onClick={finish} disabled={finishing}>
                {finishing ? <><FaSpinner className="ps-spin" /> {t('ps.loading')}</> : t('ps.skipForNow')}
              </button>
            </div>

            <div className="ps-hint">
              <FaLightbulb className="ps-hint-icon" />
              <p>{t('ps.hintSyllabiPre')}<strong>{t('ps.hintSyllabiCalendar')}</strong>{t('ps.hintSyllabiMid')}<strong>{t('ps.hintSyllabiProfile')}</strong>{t('ps.hintSyllabiPost')}</p>
            </div>
          </>
        )}

        {sylStep === 'uploading' && (
          <div className="ps-status">
            <div className="ps-status-icon ps-status-icon--spin"><FaSpinner /></div>
            <h3 className="ps-status-title">{t('ps.sylUploading')}</h3>
            <p className="ps-status-sub">
              {(sylFiles.length > 1 ? t('ps.sylUploadingSubPlural') : t('ps.sylUploadingSub')).replace('{count}', sylFiles.length)}
            </p>
          </div>
        )}

        {sylStep === 'done' && sylResults && (
          <div className="ps-status">
            <div className="ps-status-icon ps-status-icon--success"><FaCheckCircle /></div>
            <h3 className="ps-status-title">{t('ps.sylDone')}</h3>
            <p className="ps-status-sub">{t('ps.sylDoneSub')}</p>
            <div className="ps-chips">
              {sylResults.total_events_added > 0 && (
                <div className="ps-chip">
                  <span className="ps-chip-num">{sylResults.total_events_added}</span>
                  <span className="ps-chip-label">{t('ps.sylEventsLabel')}</span>
                </div>
              )}
              {sylResults.total_courses_updated > 0 && (
                <div className="ps-chip ps-chip--success">
                  <FaCheck className="ps-chip-check" />
                  <span className="ps-chip-label">
                    {(sylResults.total_courses_updated > 1 ? t('ps.sylCoursesLabelPlural') : t('ps.sylCoursesLabel')).replace('{count}', sylResults.total_courses_updated)}
                  </span>
                </div>
              )}
              {sylResults.results?.filter(r => r.success).map(r => (
                <div key={r.filename} className="ps-chip ps-chip--neutral">
                  <span className="ps-chip-label">{r.course_code || r.filename}</span>
                </div>
              ))}
            </div>
            {sylResults.results?.some(r => !r.success) && (
              <div className="ps-syl-errors">
                {sylResults.results.filter(r => !r.success).map(r => (
                  <p key={r.filename} className="ps-syl-error-row">
                    <FaExclamationTriangle /> {r.filename}: {r.error}
                  </p>
                ))}
              </div>
            )}
            <button className="ps-btn ps-btn--primary" onClick={finish} disabled={finishing}>
              {finishing ? <><FaSpinner className="ps-spin" /> {t('ps.loading')}</> : <>{t('ps.toDashboard')} <FaArrowRight /></>}
            </button>
          </div>
        )}

        {sylStep === 'error' && (
          <div className="ps-status">
            <div className="ps-status-icon ps-status-icon--warning"><FaExclamationTriangle /></div>
            <h3 className="ps-status-title">{t('ps.sylError')}</h3>
            <p className="ps-status-sub">{sylError}</p>
            <div className="ps-actions ps-actions--center">
              <button className="ps-btn ps-btn--secondary" onClick={() => { setSylStep('idle'); setSylError('') }}>{t('ps.tryAgain')}</button>
              <button className="ps-btn ps-btn--ghost" onClick={finish} disabled={finishing}>
                {finishing ? <><FaSpinner className="ps-spin" /> {t('ps.loading')}</> : t('ps.skipDashboard')}
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
