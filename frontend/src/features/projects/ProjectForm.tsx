import { useState, type FormEvent } from 'react'
import type { ProjectCreate, ProjectLink } from '../../api/types'

interface Props {
  initial?: ProjectCreate
  onSubmit: (data: ProjectCreate) => Promise<void>
  onCancel: () => void
}

export function ProjectForm({ initial, onSubmit, onCancel }: Props) {
  const [category, setCategory] = useState(initial?.category ?? '팀 프로젝트')
  const [year, setYear] = useState(initial?.year ?? '')
  const [period, setPeriod] = useState(initial?.period ?? '')
  const [name, setName] = useState(initial?.name ?? '')
  const [role, setRole] = useState(initial?.role ?? '')
  const [description, setDescription] = useState(initial?.description ?? '')
  const [links, setLinks] = useState<ProjectLink[]>(initial?.links ?? [])
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState<string | null>(null)

  async function handleSubmit(e: FormEvent) {
    e.preventDefault()
    setSubmitting(true)
    setError(null)
    try {
      await onSubmit({
        category,
        year,
        period: period || null,
        name,
        role,
        description: description || null,
        links: links.filter((l) => l.label.trim() && l.url.trim()),
      })
    } catch (err) {
      setError(err instanceof Error ? err.message : '저장에 실패했습니다.')
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <form className="form-card education-form" onSubmit={handleSubmit}>
      <input placeholder="구분 (예: 팀 프로젝트)" value={category} onChange={(e) => setCategory(e.target.value)} required />
      <div className="education-form-dates">
        <label>
          연도
          <input value={year} onChange={(e) => setYear(e.target.value)} placeholder="2026" required />
        </label>
        <label>
          기간 (선택)
          <input value={period} onChange={(e) => setPeriod(e.target.value)} placeholder="2026.01 - 2026.03" />
        </label>
      </div>
      <input placeholder="프로젝트명" value={name} onChange={(e) => setName(e.target.value)} required />
      <input placeholder="역할" value={role} onChange={(e) => setRole(e.target.value)} required />
      <input placeholder="설명 (선택)" value={description} onChange={(e) => setDescription(e.target.value)} />

      {links.map((link, idx) => (
        <div className="education-form-dates" key={idx}>
          <input
            placeholder="레이블 (예: GitHub)"
            value={link.label}
            onChange={(e) => setLinks((prev) => prev.map((l, i) => (i === idx ? { ...l, label: e.target.value } : l)))}
          />
          <input
            placeholder="URL"
            value={link.url}
            onChange={(e) => setLinks((prev) => prev.map((l, i) => (i === idx ? { ...l, url: e.target.value } : l)))}
          />
          <button type="button" className="link-button danger" onClick={() => setLinks((prev) => prev.filter((_, i) => i !== idx))}>
            삭제
          </button>
        </div>
      ))}
      <button type="button" className="link-button" onClick={() => setLinks((prev) => [...prev, { label: '', url: '' }])}>
        + 링크 추가
      </button>

      <div className="education-form-actions">
        <button type="submit" disabled={submitting}>
          저장
        </button>
        <button type="button" className="secondary" onClick={onCancel} disabled={submitting}>
          취소
        </button>
      </div>
      {error && <p className="login-form-error">{error}</p>}
    </form>
  )
}
