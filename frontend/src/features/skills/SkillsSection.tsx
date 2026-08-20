import { useEffect, useState } from 'react'
import { fetchSkills, updateSkills } from './api'
import { ApiError } from '../../api/httpClient'
import type { Skills } from '../../api/types'
import './skills.css'

interface Props {
  authenticated: boolean
  onUnauthorized: () => void
}

type LanguageRow = { name: string; level: string }

export function SkillsSection({ authenticated, onUnauthorized }: Props) {
  const [skills, setSkills] = useState<Skills | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [editing, setEditing] = useState(false)
  const [techInput, setTechInput] = useState('')
  const [languages, setLanguages] = useState<LanguageRow[]>([])
  const [saving, setSaving] = useState(false)
  const [saveError, setSaveError] = useState<string | null>(null)

  useEffect(() => {
    fetchSkills()
      .then(setSkills)
      .catch((e) => setError(e.message))
  }, [])

  useEffect(() => {
    if (!authenticated) setEditing(false)
  }, [authenticated])

  function startEditing() {
    if (!skills) return
    setTechInput(skills.tech.join(', '))
    setLanguages(skills.languages.map((l) => ({ ...l })))
    setSaveError(null)
    setEditing(true)
  }

  async function handleSave() {
    setSaving(true)
    setSaveError(null)
    try {
      const tech = techInput
        .split(',')
        .map((t) => t.trim())
        .filter(Boolean)
      const updated = await updateSkills({
        tech,
        languages: languages.filter((l) => l.name.trim() && l.level.trim()),
      })
      setSkills(updated)
      setEditing(false)
    } catch (e) {
      if (e instanceof ApiError && e.status === 401) {
        onUnauthorized()
        setSaveError('세션이 만료되었습니다. 다시 로그인해주세요.')
      } else {
        setSaveError(e instanceof Error ? e.message : '저장에 실패했습니다.')
      }
    } finally {
      setSaving(false)
    }
  }

  if (error) {
    return <div className="skills-section profile-error">스킬을 불러오지 못했습니다: {error}</div>
  }

  if (!skills) {
    return <div className="skills-section profile-loading">불러오는 중...</div>
  }

  if (skills.tech.length === 0 && skills.languages.length === 0 && !authenticated) {
    return null
  }

  if (editing) {
    return (
      <section className="skills-section">
        <h2 className="education-title">스킬</h2>
        <div className="form-card">
          <div className="skills-field-label">기술 스택 (쉼표로 구분)</div>
          <input className="editable" value={techInput} onChange={(e) => setTechInput(e.target.value)} />

          <div className="skills-field-label" style={{ marginTop: 10 }}>
            언어 능력
          </div>
          {languages.map((lang, idx) => (
            <div className="skills-lang-row" key={idx}>
              <input
                className="editable"
                placeholder="언어"
                value={lang.name}
                onChange={(e) =>
                  setLanguages((prev) => prev.map((l, i) => (i === idx ? { ...l, name: e.target.value } : l)))
                }
              />
              <input
                className="editable"
                placeholder="숙련도"
                value={lang.level}
                onChange={(e) =>
                  setLanguages((prev) => prev.map((l, i) => (i === idx ? { ...l, level: e.target.value } : l)))
                }
              />
              <button
                type="button"
                className="link-button danger"
                onClick={() => setLanguages((prev) => prev.filter((_, i) => i !== idx))}
              >
                삭제
              </button>
            </div>
          ))}
          <button
            type="button"
            className="link-button"
            onClick={() => setLanguages((prev) => [...prev, { name: '', level: '' }])}
          >
            + 언어 추가
          </button>

          <div className="profile-actions" style={{ marginTop: 14 }}>
            <button type="button" onClick={handleSave} disabled={saving}>
              저장
            </button>
            <button type="button" className="secondary" onClick={() => setEditing(false)} disabled={saving}>
              취소
            </button>
          </div>
          {saveError && <p className="login-form-error">{saveError}</p>}
        </div>
      </section>
    )
  }

  return (
    <section className="skills-section">
      <h2 className="education-title">스킬</h2>
      <div className="skills-tags">
        {skills.tech.map((t) => (
          <span className="tag" key={t}>
            {t}
          </span>
        ))}
      </div>
      {skills.languages.length > 0 && (
        <div className="skills-tags" style={{ marginTop: 8 }}>
          {skills.languages.map((l) => (
            <span className="tag" key={l.name}>
              {l.name} · {l.level}
            </span>
          ))}
        </div>
      )}
      {authenticated && (
        <button type="button" className="link-button" style={{ marginTop: 10 }} onClick={startEditing}>
          편집
        </button>
      )}
    </section>
  )
}
