import { useEffect, useState } from 'react'
import { createCareer, deleteCareer, fetchCareers, updateCareer } from './api'
import { CareerForm } from './CareerForm'
import { ApiError } from '../../api/httpClient'
import type { Career, CareerCreate } from '../../api/types'
import '../education/education.css'

interface Props {
  authenticated: boolean
  onUnauthorized: () => void
}

export function CareerSection({ authenticated, onUnauthorized }: Props) {
  const [items, setItems] = useState<Career[] | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [showAddForm, setShowAddForm] = useState(false)
  const [editingId, setEditingId] = useState<number | null>(null)

  function load() {
    fetchCareers()
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

  async function handleCreate(data: CareerCreate) {
    try {
      const created = await createCareer(data)
      setItems((prev) => (prev ? [created, ...prev] : [created]))
      setShowAddForm(false)
    } catch (e) {
      if (e instanceof ApiError && e.status === 401) onUnauthorized()
      throw e
    }
  }

  async function handleUpdate(id: number, data: CareerCreate) {
    try {
      const updated = await updateCareer(id, data)
      setItems((prev) => (prev ? prev.map((it) => (it.id === id ? updated : it)) : prev))
      setEditingId(null)
    } catch (e) {
      if (e instanceof ApiError && e.status === 401) onUnauthorized()
      throw e
    }
  }

  async function handleDelete(id: number) {
    if (!window.confirm('이 경력 항목을 삭제할까요?')) return
    try {
      await deleteCareer(id)
      setItems((prev) => (prev ? prev.filter((it) => it.id !== id) : prev))
    } catch (e) {
      if (e instanceof ApiError && e.status === 401) onUnauthorized()
    }
  }

  if (error) {
    return <div className="education-section profile-error">경력을 불러오지 못했습니다: {error}</div>
  }

  if (items === null) {
    return <div className="education-section profile-loading">불러오는 중...</div>
  }

  if (items.length === 0 && !authenticated) {
    return null
  }

  return (
    <section className="education-section">
      <h2 className="education-title">경력</h2>

      {items.map((item) =>
        editingId === item.id ? (
          <CareerForm
            key={item.id}
            initial={{
              institution: item.institution,
              period: item.period,
              role: item.role,
              description: item.description,
            }}
            onSubmit={(data) => handleUpdate(item.id, data)}
            onCancel={() => setEditingId(null)}
          />
        ) : (
          <div className="education-item" key={item.id}>
            <div className="education-item-main">
              <p className="education-school">{item.institution}</p>
              <p className="education-detail">{item.role}</p>
              {item.description && <p className="education-detail">{item.description}</p>}
              <p className="education-period">{item.period}</p>
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
          <CareerForm onSubmit={handleCreate} onCancel={() => setShowAddForm(false)} />
        ) : (
          <button type="button" className="link-button" onClick={() => setShowAddForm(true)}>
            + 경력 추가
          </button>
        ))}
    </section>
  )
}
