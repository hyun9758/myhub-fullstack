import { useEffect, useState } from 'react'
import { fetchProfile, updateProfile } from './api'
import { LoginForm } from '../auth/LoginForm'
import { ApiError } from '../../api/httpClient'
import type { Profile, SocialLink } from '../../api/types'
import './profile.css'

interface Props {
  authenticated: boolean
  onLogin: (passcode: string) => Promise<boolean>
  onLogout: () => Promise<void>
  onUnauthorized: () => void
}

type FormState = {
  full_name: string
  headline: string
  summary: string
  photo: string
  badgesInput: string
  birth: string
  address: string
  military_service: string
  email: string
  mobile: string
  affiliation: string
  social: SocialLink[]
}

export function ProfileSection({ authenticated, onLogin, onLogout, onUnauthorized }: Props) {
  const [profile, setProfile] = useState<Profile | null>(null)
  const [error, setError] = useState<string | null>(null)

  const [editing, setEditing] = useState(false)
  const [showLoginForm, setShowLoginForm] = useState(false)
  const [form, setForm] = useState<FormState | null>(null)
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
      photo: profile.photo ?? '',
      badgesInput: profile.badges.join(', '),
      birth: profile.birth ?? '',
      address: profile.address ?? '',
      military_service: profile.military_service ?? '',
      email: profile.email ?? '',
      mobile: profile.mobile ?? '',
      affiliation: profile.affiliation ?? '',
      social: profile.social.map((s) => ({ ...s })),
    })
    setSaveError(null)
    setEditing(true)
  }

  async function handleSave() {
    if (!form) return
    setSaving(true)
    setSaveError(null)
    try {
      const res = await updateProfile({
        full_name: form.full_name,
        headline: form.headline,
        summary: form.summary || null,
        photo: form.photo || null,
        badges: form.badgesInput
          .split(',')
          .map((b) => b.trim())
          .filter(Boolean),
        birth: form.birth || null,
        address: form.address || null,
        military_service: form.military_service || null,
        email: form.email || null,
        mobile: form.mobile || null,
        affiliation: form.affiliation || null,
        social: form.social.filter((s) => s.platform.trim() && s.label.trim() && s.url.trim()),
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

  if (editing && form) {
    return (
      <section className="profile-card">
        <input
          className="editable profile-name"
          value={form.full_name}
          onChange={(e) => setForm({ ...form, full_name: e.target.value })}
        />
        <input
          className="editable profile-headline"
          value={form.headline}
          onChange={(e) => setForm({ ...form, headline: e.target.value })}
        />
        <textarea
          className="editable profile-summary"
          value={form.summary}
          onChange={(e) => setForm({ ...form, summary: e.target.value })}
          rows={3}
        />

        <div className="profile-field-label">사진 URL</div>
        <input className="editable" value={form.photo} onChange={(e) => setForm({ ...form, photo: e.target.value })} />

        <div className="profile-field-label">직무 뱃지 (쉼표로 구분)</div>
        <input
          className="editable"
          value={form.badgesInput}
          onChange={(e) => setForm({ ...form, badgesInput: e.target.value })}
        />

        <div className="profile-field-label">소속</div>
        <input
          className="editable"
          value={form.affiliation}
          onChange={(e) => setForm({ ...form, affiliation: e.target.value })}
        />

        <div className="profile-field-row">
          <div style={{ flex: 1 }}>
            <div className="profile-field-label">이메일</div>
            <input className="editable" value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} />
          </div>
          <div style={{ flex: 1 }}>
            <div className="profile-field-label">모바일</div>
            <input className="editable" value={form.mobile} onChange={(e) => setForm({ ...form, mobile: e.target.value })} />
          </div>
        </div>

        <div className="profile-field-label">생년월일 · 주소 · 병역 (소유자에게만 보임)</div>
        <div className="profile-field-row">
          <input
            className="editable"
            type="date"
            style={{ flex: 1 }}
            value={form.birth}
            onChange={(e) => setForm({ ...form, birth: e.target.value })}
          />
          <input
            className="editable"
            placeholder="주소(구까지)"
            style={{ flex: 1 }}
            value={form.address}
            onChange={(e) => setForm({ ...form, address: e.target.value })}
          />
          <input
            className="editable"
            placeholder="병역"
            style={{ flex: 1 }}
            value={form.military_service}
            onChange={(e) => setForm({ ...form, military_service: e.target.value })}
          />
        </div>

        <div className="profile-field-label">소셜 링크</div>
        {form.social.map((s, idx) => (
          <div className="profile-field-row" key={idx}>
            <input
              className="editable"
              placeholder="플랫폼(github 등)"
              style={{ flex: 1 }}
              value={s.platform}
              onChange={(e) =>
                setForm({
                  ...form,
                  social: form.social.map((l, i) => (i === idx ? { ...l, platform: e.target.value } : l)),
                })
              }
            />
            <input
              className="editable"
              placeholder="표시 이름"
              style={{ flex: 1 }}
              value={s.label}
              onChange={(e) =>
                setForm({ ...form, social: form.social.map((l, i) => (i === idx ? { ...l, label: e.target.value } : l)) })
              }
            />
            <input
              className="editable"
              placeholder="URL"
              style={{ flex: 2 }}
              value={s.url}
              onChange={(e) =>
                setForm({ ...form, social: form.social.map((l, i) => (i === idx ? { ...l, url: e.target.value } : l)) })
              }
            />
            <button
              type="button"
              className="link-button danger"
              onClick={() => setForm({ ...form, social: form.social.filter((_, i) => i !== idx) })}
            >
              삭제
            </button>
          </div>
        ))}
        <button
          type="button"
          className="link-button"
          onClick={() => setForm({ ...form, social: [...form.social, { platform: '', label: '', url: '' }] })}
        >
          + 링크 추가
        </button>

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

  const hasSensitive = profile.birth || profile.address || profile.military_service

  return (
    <section className="profile-card">
      <div className="profile-header">
        <div className="profile-photo">
          {profile.photo ? <img src={profile.photo} alt={profile.full_name} /> : <span>{profile.full_name.slice(0, 1)}</span>}
        </div>
        <div>
          <h1 className="profile-name">{profile.full_name}</h1>
          <p className="profile-headline">{profile.headline}</p>
        </div>
      </div>

      {profile.badges.length > 0 && (
        <div className="profile-badges">
          {profile.badges.map((b) => (
            <span className="chip" key={b}>
              {b}
            </span>
          ))}
        </div>
      )}

      {profile.summary && <p className="profile-summary">{profile.summary}</p>}

      {(profile.affiliation || profile.email || profile.mobile) && (
        <div className="profile-meta">
          {profile.affiliation && <div>{profile.affiliation}</div>}
          {profile.email && <div>{profile.email}</div>}
          {profile.mobile && <div>{profile.mobile}</div>}
        </div>
      )}

      {hasSensitive && (
        <div className="profile-meta profile-meta-sensitive">
          {profile.birth && <div>생년월일 {profile.birth}</div>}
          {profile.address && <div>주소 {profile.address}</div>}
          {profile.military_service && <div>병역 {profile.military_service}</div>}
        </div>
      )}

      {profile.social.length > 0 && (
        <div className="social-links">
          {profile.social.map((s) => (
            <a href={s.url} target="_blank" rel="noopener" key={s.platform}>
              {s.label}
            </a>
          ))}
        </div>
      )}

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
