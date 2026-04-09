import { createContext, useContext, useState, useCallback } from 'react'
import EN from '../locales/en.js'
import FR from '../locales/fr.js'
import ZH from '../locales/zh.js'

// Translations split into src/locales/{en,fr,zh}.js for maintainability.
// Edit translations there — this file only contains the context logic.
const translations = { en: EN, fr: FR, zh: ZH }

const LanguageContext = createContext(null)

export function LanguageProvider({ children }) {
  const SUPPORTED = ['en', 'fr', 'zh']

  const [language, setLanguageState] = useState(() => {
    const stored = localStorage.getItem('language')
    return SUPPORTED.includes(stored) ? stored : 'en'
  })

  const setLanguage = useCallback((lang) => {
    const valid = SUPPORTED.includes(lang) ? lang : 'en'
    setLanguageState(valid)
    localStorage.setItem('language', valid)
  }, [])

  const t = useCallback((key) => {
    return translations[language]?.[key] ?? translations.en?.[key] ?? key
  }, [language])

  return (
    <LanguageContext.Provider value={{ language, setLanguage, t }}>
      {children}
    </LanguageContext.Provider>
  )
}

export function useLanguage() {
  const context = useContext(LanguageContext)
  if (!context) {
    throw new Error('useLanguage must be used within a LanguageProvider')
  }
  return context
}
