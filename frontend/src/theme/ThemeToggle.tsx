import { useTheme } from './useTheme'

export function ThemeToggle() {
  const { theme, toggle } = useTheme()

  return (
    <button type="button" className="secondary theme-toggle" onClick={toggle}>
      {theme === 'dark' ? '라이트 모드' : '다크 모드'}
    </button>
  )
}
