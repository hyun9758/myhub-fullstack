import { useState, type FormEvent } from 'react'
import type { CareerCreate } from '../../api/types'

interface Props {
  initial?: CareerCreate
  onSubmit: (data: CareerCreate) => Promise<void>
  onCancel: () => void
}

export function CareerForm({ initial, onSubmit, onCancel }: Props) {
  const [institution, setInstitution] = useState(initial?.institution ?? '')
  const [period, setPeriod] = useState(initial?.period ?? '')
  const [role, setRole] = useState(initial?.role ?? '')
  const [description, setDescription] = useState(initial?.description ?? '')
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState<string | null>(null)

  async function handleSubmit(e: FormEvent) {
    e.preventDefault()
    setSubmitting(true)
    setError(null)
    try {
      await onSubmit({ institution, period, role, description: description || null })
    } catch (err) {
      setError(err instanceof Error ? err.message : '저장에 실패했습니다.')
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <form className="form-card education-form" onSubmit={handleSubmit}>
      <input placeholder="기관명" value={institution} onChange={(e) => setInstitution(e.target.value)} required />
      <input
        placeholder="기간 (예: 2025.12 ~ 2026.02)"
        value={period}
        onChange={(e) => setPeriod(e.target.value)}
        required
      />
      <input placeholder="역할/직무" value={role} onChange={(e) => setRole(e.target.value)} required />
      <input placeholder="설명 (선택)" value={description} onChange={(e) => setDescription(e.target.value)} />
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
