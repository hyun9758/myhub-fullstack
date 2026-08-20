import { useEffect, useState } from 'react'
import { fetchProfile } from './api'
import type { Profile } from '../../api/types'
import './profile.css'

export function ProfileSection() {
  const [profile, setProfile] = useState<Profile | null>(null)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetchProfile()
      .then((res) => setProfile(res.profile))
      .catch((e) => setError(e.message))
  }, [])

  if (error) {
    return <div className="profile-card profile-error">프로필을 불러오지 못했습니다: {error}</div>
  }

  if (!profile) {
    return <div className="profile-card profile-loading">불러오는 중...</div>
  }

  return (
    <section className="profile-card">
      <h1 className="profile-name">{profile.full_name}</h1>
      <p className="profile-headline">{profile.headline}</p>
      {profile.summary && <p className="profile-summary">{profile.summary}</p>}
      <p className="profile-updated">마지막 수정: {new Date(profile.updated_at).toLocaleString('ko-KR')}</p>
    </section>
  )
}
