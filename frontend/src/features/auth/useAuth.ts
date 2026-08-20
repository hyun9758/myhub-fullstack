import { useCallback, useEffect, useState } from 'react'
import * as authApi from './api'

export function useAuth() {
  const [authenticated, setAuthenticated] = useState(false)
  const [checking, setChecking] = useState(true)

  useEffect(() => {
    authApi
      .checkSession()
      .then((res) => setAuthenticated(res.authenticated))
      .finally(() => setChecking(false))
  }, [])

  const login = useCallback(async (passcode: string) => {
    const res = await authApi.login(passcode)
    setAuthenticated(res.authenticated)
    return res.authenticated
  }, [])

  const logout = useCallback(async () => {
    await authApi.logout()
    setAuthenticated(false)
  }, [])

  // 자식 컴포넌트가 401(세션 만료)을 감지했을 때 호출하는 콜백.
  // 로그인 상태를 바꾸는 책임은 이 훅(부모)에만 있다.
  const handleUnauthorized = useCallback(() => {
    setAuthenticated(false)
  }, [])

  return { authenticated, checking, login, logout, handleUnauthorized }
}
