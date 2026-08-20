import { useEffect, useState } from 'react'
import { fetchProfile, updateProfile } from './api'
import { LoginForm } from '../auth/LoginForm'
import { ApiError } from '../../api/httpClient'
import type { Profile } from '../../api/types'
import './profile.css'

interface Props {
  authenticated: boolean
  onLogin: (passcode: string) => Promise<boolean>
  onLogout: () => Promise<void>
  onUnauthorized: () => void
}

type FormState = { full_name: string; headline: string; summary: string }

export function ProfileSection({ authenticated, onLogin, onLogout, onUnauthorized }: Props) {
  const [profile, setProfile] = useState<Profile | null>(null)
  const [error, setError] = useState<string | null>(null)

  const [editing, setEditing] = useState(false)
  const [showLoginForm, setShowLoginForm] = useState(false)
  const [form, setForm] = useState<FormState>({ full_name: '', headline: '', summary: '' })
  const [saving, setSaving] = useState(false)
  const [saveError, setSaveError] = useState<string | null>(null)

  useEffect(() => {
    fetchProfile()
      .then((res) => setProfile(res.profile))
      .catch((e) => setError(e.message))
  }, [])

  // 세션이 풀리면(로그아웃 or 만료) 편집 중이었더라도 읽기 모드로 되돌린다.
  useEffect(() => {
    if (!authenticated) {
      setEditing(false)
      setShowLoginForm(false)
    }
  }, [authenticated])

  function startEditing() {
    if (!profile) return
    setForm({
      full_name: profile.full_name,
      headline: profile.headline,
      summary: profile.summary ?? '',
    })
    setSaveError(null)
    setEditing(true)
  }

  async function handleSave() {
    setSaving(true)
    setSaveError(null)
    try {
      const res = await updateProfile({
        full_name: form.full_name,
        headline: form.headline,
        summary: form.summary,
      })
      setProfile(res.profile)
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
    return <div className="profile-card profile-error">프로필을 불러오지 못했습니다: {error}</div>
  }

  if (!profile) {
    return <div className="profile-card profile-loading">불러오는 중...</div>
  }

  if (editing) {
    return (
      <section className="profile-card">
        <input
          className="editable profile-name"
          value={form.full_name}
          onChange={(e) => setForm((f) => ({ ...f, full_name: e.target.value }))}
        />
        <input
          className="editable profile-headline"
          value={form.headline}
          onChange={(e) => setForm((f) => ({ ...f, headline: e.target.value }))}
        />
        <textarea
          className="editable profile-summary"
          value={form.summary}
          onChange={(e) => setForm((f) => ({ ...f, summary: e.target.value }))}
          rows={3}
        />
        <div className="profile-footer">
          <div className="profile-actions">
            <button type="button" onClick={handleSave} disabled={saving}>
              저장
            </button>
            <button type="button" className="secondary" onClick={() => setEditing(false)} disabled={saving}>
              취소
            </button>
          </div>
        </div>
        {saveError && <p className="login-form-error">{saveError}</p>}
      </section>
    )
  }

  return (
    <section className="profile-card">
      <h1 className="profile-name">{profile.full_name}</h1>
      <p className="profile-headline">{profile.headline}</p>
      {profile.summary && <p className="profile-summary">{profile.summary}</p>}
      <div className="profile-footer">
        <p className="profile-updated">마지막 수정: {new Date(profile.updated_at).toLocaleString('ko-KR')}</p>
        {authenticated ? (
          <div className="profile-actions">
            <button type="button" className="link-button" onClick={startEditing}>
              편집
            </button>
            <button type="button" className="link-button" onClick={() => onLogout()}>
              로그아웃
            </button>
          </div>
        ) : showLoginForm ? (
          <LoginForm onLogin={onLogin} onCancel={() => setShowLoginForm(false)} />
        ) : (
          <button type="button" className="link-button profile-login-link" onClick={() => setShowLoginForm(true)}>
            관리자 로그인
          </button>
        )}
      </div>
    </section>
  )
}
