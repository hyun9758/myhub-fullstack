import { ProfileSection } from './features/profile/ProfileSection'
import { useAuth } from './features/auth/useAuth'
import './App.css'

function App() {
  const { authenticated, login, logout, handleUnauthorized } = useAuth()

  return (
    <main className="page">
      <ProfileSection
        authenticated={authenticated}
        onLogin={login}
        onLogout={logout}
        onUnauthorized={handleUnauthorized}
      />
    </main>
  )
}

export default App
