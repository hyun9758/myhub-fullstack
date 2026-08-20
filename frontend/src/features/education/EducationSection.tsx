import { useEffect, useState } from 'react'
import { createEducation, deleteEducation, fetchEducations, updateEducation } from './api'
import { EducationForm } from './EducationForm'
import { ApiError } from '../../api/httpClient'
import type { Education, EducationCreate } from '../../api/types'
import './education.css'

interface Props {
  authenticated: boolean
  onUnauthorized: () => void
}

function formatPeriod(startDate: string, endDate: string | null) {
  const end = endDate ?? '재학 중'
  return `${startDate} ~ ${end}`
}

export function EducationSection({ authenticated, onUnauthorized }: Props) {
  const [items, setItems] = useState<Education[] | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [showAddForm, setShowAddForm] = useState(false)
  const [editingId, setEditingId] = useState<number | null>(null)

  function load() {
    fetchEducations()
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

  async function handleCreate(data: EducationCreate) {
    try {
      const created = await createEducation(data)
      setItems((prev) => (prev ? [created, ...prev] : [created]))
      setShowAddForm(false)
    } catch (e) {
      if (e instanceof ApiError && e.status === 401) onUnauthorized()
      throw e
    }
  }

  async function handleUpdate(id: number, data: EducationCreate) {
    try {
      const updated = await updateEducation(id, data)
      setItems((prev) => (prev ? prev.map((it) => (it.id === id ? updated : it)) : prev))
      setEditingId(null)
    } catch (e) {
      if (e instanceof ApiError && e.status === 401) onUnauthorized()
      throw e
    }
  }

  async function handleDelete(id: number) {
    if (!window.confirm('이 학력 항목을 삭제할까요?')) return
    try {
      await deleteEducation(id)
      setItems((prev) => (prev ? prev.filter((it) => it.id !== id) : prev))
    } catch (e) {
      if (e instanceof ApiError && e.status === 401) onUnauthorized()
    }
  }

  if (error) {
    return <div className="education-section profile-error">학력을 불러오지 못했습니다: {error}</div>
  }

  if (items === null) {
    return <div className="education-section profile-loading">불러오는 중...</div>
  }

  return (
    <section className="education-section">
      <h2 className="education-title">학력</h2>

      {items.map((item) =>
        editingId === item.id ? (
          <EducationForm
            key={item.id}
            initial={{
              school: item.school,
              degree: item.degree,
              field_of_study: item.field_of_study,
              start_date: item.start_date,
              end_date: item.end_date,
            }}
            onSubmit={(data) => handleUpdate(item.id, data)}
            onCancel={() => setEditingId(null)}
          />
        ) : (
          <div className="education-item" key={item.id}>
            <div className="education-item-main">
              <p className="education-school">{item.school}</p>
              <p className="education-detail">
                {item.degree}
                {item.field_of_study ? ` · ${item.field_of_study}` : ''}
              </p>
              <p className="education-period">{formatPeriod(item.start_date, item.end_date)}</p>
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
          <EducationForm onSubmit={handleCreate} onCancel={() => setShowAddForm(false)} />
        ) : (
          <button type="button" className="link-button" onClick={() => setShowAddForm(true)}>
            + 학력 추가
          </button>
        ))}
    </section>
  )
}
