import { create } from 'zustand'
import { persist } from 'zustand/middleware'

import { authApi } from '@/services/api'
import { Company, User } from '@/types'

interface AuthState {
  token: string | null
  user: User | null
  company: Company | null
  isAuthenticated: boolean
  login: (email: string, password: string) => Promise<void>
  logout: () => void
  setUser: (user: User, company?: Company) => void
}

export const useAuth = create<AuthState>()(
  persist(
    (set) => ({
      token: null,
      user: null,
      company: null,
      isAuthenticated: false,
      login: async (email: string, password: string) => {
        const response = await authApi.login(email, password)
        const { token, user, company } = response.data
        localStorage.setItem('token', token)
        set({ token, user, company, isAuthenticated: true })
      },
      logout: () => {
        localStorage.removeItem('token')
        set({ token: null, user: null, company: null, isAuthenticated: false })
      },
      setUser: (user: User, company?: Company) => {
        set({ user, company })
      },
    }),
    {
      name: 'auth-storage',
    }
  )
)
