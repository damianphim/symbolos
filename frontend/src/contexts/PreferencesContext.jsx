/* eslint-disable react-refresh/only-export-components */
import { createContext, useContext, useState, useEffect, useCallback } from 'react'
import EN from '../locales/en.js'
import FR from '../locales/fr.js'
import ZH from '../locales/zh.js'

const translations = { en: EN, fr: FR, zh: ZH }
const SUPPORTED_LANGS = ['en', 'fr', 'zh']

const TIMEZONES = [
  { value: 'America/Montreal',     label: 'Montreal / Toronto (ET)' },
  { value: 'America/Vancouver',    label: 'Vancouver (PT)' },
  { value: 'America/Edmonton',     label: 'Calgary / Edmonton (MT)' },
  { value: 'America/Winnipeg',     label: 'Winnipeg (CT)' },
  { value: 'America/Halifax',      label: 'Halifax (AT)' },
  { value: 'America/St_Johns',     label: "St. John's (NT)" },
  { value: 'America/New_York',     label: 'New York (ET)' },
  { value: 'America/Chicago',      label: 'Chicago (CT)' },
  { value: 'America/Denver',       label: 'Denver (MT)' },
  { value: 'America/Los_Angeles',  label: 'Los Angeles (PT)' },
  { value: 'Pacific/Honolulu',     label: 'Honolulu (HT)' },
  { value: 'Europe/London',        label: 'London (GMT/BST)' },
  { value: 'Europe/Paris',         label: 'Paris / Brussels (CET)' },
  { value: 'Europe/Berlin',        label: 'Berlin / Amsterdam (CET)' },
  { value: 'Europe/Rome',          label: 'Rome / Madrid (CET)' },
  { value: 'Europe/Athens',        label: 'Athens / Helsinki (EET)' },
  { value: 'Europe/Moscow',        label: 'Moscow (MSK)' },
  { value: 'Asia/Dubai',           label: 'Dubai (GST)' },
  { value: 'Asia/Karachi',         label: 'Karachi / Islamabad (PKT)' },
  { value: 'Asia/Kolkata',         label: 'Mumbai / Delhi (IST)' },
  { value: 'Asia/Dhaka',           label: 'Dhaka (BST)' },
  { value: 'Asia/Bangkok',         label: 'Bangkok / Jakarta (ICT)' },
  { value: 'Asia/Shanghai',        label: 'Beijing / Shanghai (CST)' },
  { value: 'Asia/Tokyo',           label: 'Tokyo (JST)' },
  { value: 'Asia/Seoul',           label: 'Seoul (KST)' },
  { value: 'Asia/Singapore',       label: 'Singapore (SGT)' },
  { value: 'Asia/Hong_Kong',       label: 'Hong Kong (HKT)' },
  { value: 'Africa/Cairo',         label: 'Cairo (EET)' },
  { value: 'Africa/Johannesburg',  label: 'Johannesburg (SAST)' },
  { value: 'Africa/Lagos',         label: 'Lagos / Accra (WAT)' },
  { value: 'Australia/Sydney',     label: 'Sydney / Melbourne (AEST)' },
  { value: 'Australia/Perth',      label: 'Perth (AWST)' },
  { value: 'Pacific/Auckland',     label: 'Auckland (NZST)' },
  { value: 'America/Sao_Paulo',    label: 'São Paulo / Rio (BRT)' },
  { value: 'America/Argentina/Buenos_Aires', label: 'Buenos Aires (ART)' },
  { value: 'America/Bogota',       label: 'Bogotá / Lima (COT)' },
  { value: 'America/Mexico_City',  label: 'Mexico City (CST)' },
  { value: 'UTC',                  label: 'UTC' },
]

// Separate internal contexts to avoid cross-preference re-renders
const ThemeCtx    = createContext(null)
const LangCtx     = createContext(null)
const TimezoneCtx = createContext(null)

function getSystemTheme() {
  return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'
}

function resolveTheme(preference) {
  if (preference === 'auto') return getSystemTheme()
  return preference === 'dark' ? 'dark' : 'light'
}

export function PreferencesProvider({ children }) {
  // ── Theme ──
  const [theme, setThemeState] = useState(() => {
    const stored = localStorage.getItem('theme')
    return stored === 'dark' || stored === 'auto' ? stored : 'light'
  })
  const [resolvedTheme, setResolvedTheme] = useState(() => resolveTheme(
    localStorage.getItem('theme') || 'light'
  ))

  const applyTheme = useCallback((preference) => {
    const resolved = resolveTheme(preference)
    setResolvedTheme(resolved)
    document.documentElement.setAttribute('data-theme', resolved)
  }, [])

  const setTheme = useCallback((newTheme) => {
    const valid = newTheme === 'dark' || newTheme === 'auto' ? newTheme : 'light'
    setThemeState(valid)
    localStorage.setItem('theme', valid)
    applyTheme(valid)
  }, [applyTheme])

  useEffect(() => { applyTheme(theme) }, []) // eslint-disable-line react-hooks/exhaustive-deps

  useEffect(() => {
    if (theme !== 'auto') return
    const mq = window.matchMedia('(prefers-color-scheme: dark)')
    const handler = () => {
      const resolved = getSystemTheme()
      setResolvedTheme(resolved)
      document.documentElement.setAttribute('data-theme', resolved)
    }
    mq.addEventListener('change', handler)
    return () => mq.removeEventListener('change', handler)
  }, [theme])

  // ── Language ──
  const [language, setLanguageState] = useState(() => {
    const stored = localStorage.getItem('language')
    return SUPPORTED_LANGS.includes(stored) ? stored : 'en'
  })

  const setLanguage = useCallback((lang) => {
    const valid = SUPPORTED_LANGS.includes(lang) ? lang : 'en'
    setLanguageState(valid)
    localStorage.setItem('language', valid)
  }, [])

  const t = useCallback((key) => {
    return translations[language]?.[key] ?? translations.en?.[key] ?? key
  }, [language])

  // ── Timezone ──
  const [timezone, setTimezoneState] = useState(
    () => localStorage.getItem('timezone') || Intl.DateTimeFormat().resolvedOptions().timeZone
  )

  const setTimezone = useCallback((tz) => {
    setTimezoneState(tz)
    localStorage.setItem('timezone', tz)
  }, [])

  const getTodayStr = useCallback(() => {
    return new Date().toLocaleDateString('en-CA', { timeZone: timezone })
  }, [timezone])

  const getNow = useCallback(() => {
    return new Date(new Date().toLocaleString('en-US', { timeZone: timezone }))
  }, [timezone])

  return (
    <ThemeCtx.Provider value={{ theme, setTheme, resolvedTheme }}>
      <LangCtx.Provider value={{ language, setLanguage, t }}>
        <TimezoneCtx.Provider value={{ timezone, setTimezone, getTodayStr, getNow, TIMEZONES }}>
          {children}
        </TimezoneCtx.Provider>
      </LangCtx.Provider>
    </ThemeCtx.Provider>
  )
}

export function useTheme() {
  const ctx = useContext(ThemeCtx)
  if (!ctx) throw new Error('useTheme must be used within PreferencesProvider')
  return ctx
}

export function useLanguage() {
  const ctx = useContext(LangCtx)
  if (!ctx) throw new Error('useLanguage must be used within PreferencesProvider')
  return ctx
}

export function useTimezone() {
  const ctx = useContext(TimezoneCtx)
  if (!ctx) throw new Error('useTimezone must be used within PreferencesProvider')
  return ctx
}

export { TIMEZONES }
