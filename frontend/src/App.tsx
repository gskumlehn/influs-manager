import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom'

import { Login } from '@/components/shared/Login'
import { useAuth } from '@/hooks/useAuth'
import { useTheme } from '@/hooks/useTheme'
import { AdminPage } from '@/pages/AdminPage'
import { ClientPage } from '@/pages/ClientPage'

const queryClient = new QueryClient()

const ProtectedRoute = ({ children, role }: { children: React.ReactNode; role?: string }) => {
  const { isAuthenticated, user } = useAuth()

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />
  }

  if (role && user?.role !== role) {
    return <Navigate to={user?.role === 'admin' ? '/admin' : '/client'} replace />
  }

  return <>{children}</>
}

const AppContent = () => {
  useTheme()

  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route
        path="/admin"
        element={
          <ProtectedRoute role="admin">
            <AdminPage />
          </ProtectedRoute>
        }
      />
      <Route
        path="/client"
        element={
          <ProtectedRoute role="client">
            <ClientPage />
          </ProtectedRoute>
        }
      />
      <Route path="/" element={<Navigate to="/login" replace />} />
    </Routes>
  )
}

export const App = () => {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <AppContent />
      </BrowserRouter>
    </QueryClientProvider>
  )
}
