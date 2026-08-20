import { ProfileSection } from './features/profile/ProfileSection'
import { EducationSection } from './features/education/EducationSection'
import { CareerSection } from './features/career/CareerSection'
import { SkillsSection } from './features/skills/SkillsSection'
import { useAuth } from './features/auth/useAuth'
import { ThemeToggle } from './theme/ThemeToggle'
import './App.css'

function App() {
  const { authenticated, login, logout, handleUnauthorized } = useAuth()

  return (
    <main className="page">
      <div className="page-toolbar">
        <ThemeToggle />
      </div>
      <ProfileSection
        authenticated={authenticated}
        onLogin={login}
        onLogout={logout}
        onUnauthorized={handleUnauthorized}
      />
      <EducationSection authenticated={authenticated} onUnauthorized={handleUnauthorized} />
      <CareerSection authenticated={authenticated} onUnauthorized={handleUnauthorized} />
      <SkillsSection authenticated={authenticated} onUnauthorized={handleUnauthorized} />
    </main>
  )
}

export default App
