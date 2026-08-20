import { apiFetchJson } from '../../api/httpClient'
import type { Education, EducationCreate, EducationUpdate } from '../../api/types'

export function fetchEducations(): Promise<Education[]> {
  return apiFetchJson<Education[]>('/api/educations')
}

export function createEducation(body: EducationCreate): Promise<Education> {
  return apiFetchJson<Education>('/api/educations', {
    method: 'POST',
    body: JSON.stringify(body),
  })
}

export function updateEducation(id: number, body: EducationUpdate): Promise<Education> {
  return apiFetchJson<Education>(`/api/educations/${id}`, {
    method: 'PUT',
    body: JSON.stringify(body),
  })
}

export async function deleteEducation(id: number): Promise<void> {
  await apiFetchJson<void>(`/api/educations/${id}`, { method: 'DELETE' })
}
