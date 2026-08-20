import { apiFetchJson } from '../../api/httpClient'
import type { AuthStatus } from '../../api/types'

export function checkSession(): Promise<AuthStatus> {
  return apiFetchJson<AuthStatus>('/api/auth/session')
}

export function login(passcode: string): Promise<AuthStatus> {
  return apiFetchJson<AuthStatus>('/api/auth/session', {
    method: 'POST',
    body: JSON.stringify({ passcode }),
  })
}

export function logout(): Promise<AuthStatus> {
  return apiFetchJson<AuthStatus>('/api/auth/session', { method: 'DELETE' })
}
