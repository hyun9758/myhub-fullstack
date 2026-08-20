import { apiFetchJson } from '../../api/httpClient'
import type { Project, ProjectCreate, ProjectUpdate } from '../../api/types'

export function fetchProjects(): Promise<Project[]> {
  return apiFetchJson<Project[]>('/api/projects')
}

export function createProject(body: ProjectCreate): Promise<Project> {
  return apiFetchJson<Project>('/api/projects', {
    method: 'POST',
    body: JSON.stringify(body),
  })
}

export function updateProject(id: number, body: ProjectUpdate): Promise<Project> {
  return apiFetchJson<Project>(`/api/projects/${id}`, {
    method: 'PUT',
    body: JSON.stringify(body),
  })
}

export async function deleteProject(id: number): Promise<void> {
  await apiFetchJson<void>(`/api/projects/${id}`, { method: 'DELETE' })
}
