import { apiFetchJson } from '../../api/httpClient'
import type { Skills, SkillsUpdate } from '../../api/types'

export function fetchSkills(): Promise<Skills> {
  return apiFetchJson<Skills>('/api/skills')
}

export function updateSkills(body: SkillsUpdate): Promise<Skills> {
  return apiFetchJson<Skills>('/api/skills', {
    method: 'PUT',
    body: JSON.stringify(body),
  })
}
