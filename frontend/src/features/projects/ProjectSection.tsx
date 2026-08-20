import { useEffect, useState } from 'react'
import { createProject, deleteProject, fetchProjects, updateProject } from './api'
import { ProjectForm } from './ProjectForm'
import { ApiError } from '../../api/httpClient'
import type { Project, ProjectCreate } from '../../api/types'
import '../education/education.css'

interface Props {
  authenticated: boolean
  onUnauthorized: () => void
}

export function ProjectSection({ authenticated, onUnauthorized }: Props) {
  const [items, setItems] = useState<Project[] | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [showAddForm, setShowAddForm] = useState(false)
  const [editingId, setEditingId] = useState<number | null>(null)

  function load() {
    fetchProjects()
      .then(setItems)
      .catch((e) => setError(e.message))
  }

  useEffect(load, [])

  useEffect(() => {
    if (!authenticated) {
      setShowAddForm(false)
      setEditingId(null)
    }
  }, [authenticated])

  async function handleCreate(data: ProjectCreate) {
    try {
      const created = await createProject(data)
      setItems((prev) => (prev ? [created, ...prev] : [created]))
      setShowAddForm(false)
    } catch (e) {
      if (e instanceof ApiError && e.status === 401) onUnauthorized()
      throw e
    }
  }

  async function handleUpdate(id: number, data: ProjectCreate) {
    try {
      const updated = await updateProject(id, data)
      setItems((prev) => (prev ? prev.map((it) => (it.id === id ? updated : it)) : prev))
      setEditingId(null)
    } catch (e) {
      if (e instanceof ApiError && e.status === 401) onUnauthorized()
      throw e
    }
  }

  async function handleDelete(id: number) {
    if (!window.confirm('이 프로젝트 항목을 삭제할까요?')) return
    try {
      await deleteProject(id)
      setItems((prev) => (prev ? prev.filter((it) => it.id !== id) : prev))
    } catch (e) {
      if (e instanceof ApiError && e.status === 401) onUnauthorized()
    }
  }

  if (error) {
    return <div className="education-section profile-error">프로젝트를 불러오지 못했습니다: {error}</div>
  }

  if (items === null) {
    return <div className="education-section profile-loading">불러오는 중...</div>
  }

  if (items.length === 0 && !authenticated) {
    return null
  }

  return (
    <section className="education-section">
      <h2 className="education-title">프로젝트</h2>

      {items.map((item) =>
        editingId === item.id ? (
          <ProjectForm
            key={item.id}
            initial={{
              category: item.category,
              year: item.year,
              period: item.period,
              name: item.name,
              role: item.role,
              description: item.description,
              links: item.links,
            }}
            onSubmit={(data) => handleUpdate(item.id, data)}
            onCancel={() => setEditingId(null)}
          />
        ) : (
          <div className="education-item" key={item.id}>
            <div className="education-item-main">
              <span className="entry-tag">{item.category}</span>
              <p className="education-school">{item.name}</p>
              <p className="education-detail">{item.role}</p>
              {item.description && <p className="education-detail">{item.description}</p>}
              <p className="education-period">
                {item.year}
                {item.period ? ` · ${item.period}` : ''}
              </p>
              {item.links.length > 0 && (
                <div className="entry-links">
                  {item.links.map((l) => (
                    <a href={l.url} target="_blank" rel="noopener" key={l.url}>
                      🔗 {l.label}
                    </a>
                  ))}
                </div>
              )}
            </div>
            {authenticated && (
              <div className="education-item-actions">
                <button type="button" className="link-button" onClick={() => setEditingId(item.id)}>
                  수정
                </button>
                <button type="button" className="link-button danger" onClick={() => handleDelete(item.id)}>
                  삭제
                </button>
              </div>
            )}
          </div>
        ),
      )}

      {authenticated &&
        (showAddForm ? (
          <ProjectForm onSubmit={handleCreate} onCancel={() => setShowAddForm(false)} />
        ) : (
          <button type="button" className="link-button" onClick={() => setShowAddForm(true)}>
            + 프로젝트 추가
          </button>
        ))}
    </section>
  )
}
