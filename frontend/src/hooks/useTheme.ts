import { useEffect } from 'react'

import { useAuth } from './useAuth'

export const useTheme = () => {
  const { company } = useAuth()

  useEffect(() => {
    if (company?.primary_color) {
      document.documentElement.style.setProperty('--primary-color', company.primary_color)
    }
    if (company?.secondary_color) {
      document.documentElement.style.setProperty('--secondary-color', company.secondary_color)
    }
  }, [company])

  return {
    primaryColor: company?.primary_color || '#3b82f6',
    secondaryColor: company?.secondary_color || '#10b981',
    logoUrl: company?.logo_url,
    companyName: company?.name,
  }
}
