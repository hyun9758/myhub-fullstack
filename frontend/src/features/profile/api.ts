import { apiFetchJson } from '../../api/httpClient'
import type { ProfileResponse } from '../../api/types'

export function fetchProfile(): Promise<ProfileResponse> {
  return apiFetchJson<ProfileResponse>('/api/profile')
}
