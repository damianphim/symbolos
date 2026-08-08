import { describe, it, expect, afterEach, vi } from 'vitest'
import { toProxiedStorageUrl } from './storageUrl'

const SUPA = 'https://jgkfeyqnpsivbgoiekze.supabase.co'
const OBJ = `${SUPA}/storage/v1/object/public/profile-images/abc/avatar.png`

function setOrigin(href) {
  vi.stubGlobal('window', { location: new URL(href) })
}
afterEach(() => vi.unstubAllGlobals())

describe('toProxiedStorageUrl', () => {
  it('rewrites to the same origin over https', () => {
    setOrigin('https://symbolos.ca/')
    expect(toProxiedStorageUrl(OBJ)).toBe(
      'https://symbolos.ca/storage/profile-images/abc/avatar.png'
    )
  })

  it('produces an absolute https URL — the backend validator rejects relative ones', () => {
    setOrigin('https://symbolos.ca/')
    expect(toProxiedStorageUrl(OBJ).startsWith('https://')).toBe(true)
  })

  it('leaves the Supabase URL alone on http (local dev)', () => {
    // http://localhost would fail validate_profile_image, which requires https
    // on an allowlisted host — so dev must keep the original URL.
    setOrigin('http://localhost:5173/')
    expect(toProxiedStorageUrl(OBJ)).toBe(OBJ)
  })

  it('leaves the Supabase URL alone on Capacitor native', () => {
    setOrigin('capacitor://localhost/')
    expect(toProxiedStorageUrl(OBJ)).toBe(OBJ)
  })

  it('passes through non-Supabase URLs untouched', () => {
    setOrigin('https://symbolos.ca/')
    const other = 'https://example.com/pic.png'
    expect(toProxiedStorageUrl(other)).toBe(other)
  })

  it('handles club-logos as well as profile-images', () => {
    setOrigin('https://symbolos.ca/')
    const logo = `${SUPA}/storage/v1/object/public/club-logos/x/logo.png`
    expect(toProxiedStorageUrl(logo)).toBe('https://symbolos.ca/storage/club-logos/x/logo.png')
  })

  it('is null-safe', () => {
    setOrigin('https://symbolos.ca/')
    expect(toProxiedStorageUrl(null)).toBe(null)
    expect(toProxiedStorageUrl('')).toBe('')
  })
})
