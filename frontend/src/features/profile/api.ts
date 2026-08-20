import { apiFetchJson } from '../../api/httpClient'
import type { ProfileResponse, ProfileUpdate } from '../../api/types'

export function fetchProfile(): Promise<ProfileResponse> {
  return apiFetchJson<ProfileResponse>('/api/profile')
}

export function updateProfile(body: ProfileUpdate): Promise<ProfileResponse> {
  return apiFetchJson<ProfileResponse>('/api/profile', {
    method: 'PUT',
    body: JSON.stringify(body),
  })
}
