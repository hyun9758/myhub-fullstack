import { useState, type FormEvent } from 'react'
import type { EducationCreate } from '../../api/types'

interface Props {
  initial?: EducationCreate
  onSubmit: (data: EducationCreate) => Promise<void>
  onCancel: () => void
}

export function EducationForm({ initial, onSubmit, onCancel }: Props) {
  const [school, setSchool] = useState(initial?.school ?? '')
  const [degree, setDegree] = useState(initial?.degree ?? '')
  const [fieldOfStudy, setFieldOfStudy] = useState(initial?.field_of_study ?? '')
  const [startDate, setStartDate] = useState(initial?.start_date ?? '')
  const [endDate, setEndDate] = useState(initial?.end_date ?? '')
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState<string | null>(null)

  async function handleSubmit(e: FormEvent) {
    e.preventDefault()
    setSubmitting(true)
    setError(null)
    try {
      await onSubmit({
        school,
        degree,
        field_of_study: fieldOfStudy || null,
        start_date: startDate,
        end_date: endDate || null,
      })
    } catch (err) {
      setError(err instanceof Error ? err.message : '저장에 실패했습니다.')
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <form className="form-card education-form" onSubmit={handleSubmit}>
      <input placeholder="학교명" value={school} onChange={(e) => setSchool(e.target.value)} required />
      <input placeholder="학위 (예: 학사)" value={degree} onChange={(e) => setDegree(e.target.value)} required />
      <input
        placeholder="전공/과정 (선택)"
        value={fieldOfStudy}
        onChange={(e) => setFieldOfStudy(e.target.value)}
      />
      <div className="education-form-dates">
        <label>
          시작일
          <input type="date" value={startDate} onChange={(e) => setStartDate(e.target.value)} required />
        </label>
        <label>
          종료일 (재학 중이면 비움)
          <input type="date" value={endDate} onChange={(e) => setEndDate(e.target.value)} />
        </label>
      </div>
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
