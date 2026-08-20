import { useState, type FormEvent } from 'react'

interface Props {
  onLogin: (passcode: string) => Promise<boolean>
  onCancel: () => void
}

export function LoginForm({ onLogin, onCancel }: Props) {
  const [passcode, setPasscode] = useState('')
  const [error, setError] = useState<string | null>(null)
  const [submitting, setSubmitting] = useState(false)

  async function handleSubmit(e: FormEvent) {
    e.preventDefault()
    setSubmitting(true)
    setError(null)
    try {
      const ok = await onLogin(passcode)
      if (!ok) setError('비밀 코드가 올바르지 않습니다.')
    } catch (err) {
      setError(err instanceof Error ? err.message : '로그인에 실패했습니다.')
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <form className="login-form" onSubmit={handleSubmit}>
      <input
        type="password"
        className="editable"
        placeholder="관리자 비밀 코드"
        value={passcode}
        onChange={(e) => setPasscode(e.target.value)}
        autoFocus
      />
      <div className="login-form-actions">
        <button type="submit" disabled={submitting}>
          로그인
        </button>
        <button type="button" onClick={onCancel}>
          취소
        </button>
      </div>
      {error && <p className="login-form-error">{error}</p>}
    </form>
  )
}
