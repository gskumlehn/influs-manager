import { useAuth } from '@/hooks/useAuth'
import { useTheme } from '@/hooks/useTheme'

export const Header = () => {
  const { user, logout } = useAuth()
  const { logoUrl, companyName, primaryColor } = useTheme()

  return (
    <header className="bg-white shadow" style={{ borderTopColor: primaryColor, borderTopWidth: '4px' }}>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex justify-between items-center">
        <div className="flex items-center space-x-4">
          {logoUrl && (
            <img src={logoUrl} alt={companyName} className="h-10 w-auto" />
          )}
          <h1 className="text-2xl font-bold text-gray-900">
            {companyName || 'Sistema de Influenciadores'}
          </h1>
        </div>
        <div className="flex items-center space-x-4">
          <span className="text-sm text-gray-600">{user?.email}</span>
          <button
            onClick={logout}
            className="px-4 py-2 text-sm font-medium text-white bg-red-600 hover:bg-red-700 rounded-md"
          >
            Sair
          </button>
        </div>
      </div>
    </header>
  )
}
