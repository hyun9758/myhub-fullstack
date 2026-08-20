import { apiFetchJson } from '../../api/httpClient'
import type { Career, CareerCreate, CareerUpdate } from '../../api/types'

export function fetchCareers(): Promise<Career[]> {
  return apiFetchJson<Career[]>('/api/careers')
}

export function createCareer(body: CareerCreate): Promise<Career> {
  return apiFetchJson<Career>('/api/careers', {
    method: 'POST',
    body: JSON.stringify(body),
  })
}

export function updateCareer(id: number, body: CareerUpdate): Promise<Career> {
  return apiFetchJson<Career>(`/api/careers/${id}`, {
    method: 'PUT',
    body: JSON.stringify(body),
  })
}

export async function deleteCareer(id: number): Promise<void> {
  await apiFetchJson<void>(`/api/careers/${id}`, { method: 'DELETE' })
}
