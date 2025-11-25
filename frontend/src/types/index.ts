export interface Company {
  id: number
  name: string
  slug: string
  logo_url?: string
  primary_color?: string
  secondary_color?: string
  instagram_handle?: string
  created_at: string
  updated_at: string
}

export interface Campaign {
  id: number
  company_id: number
  name: string
  description?: string
  status: 'draft' | 'active' | 'completed' | 'archived'
  created_at: string
  updated_at: string
}

export interface Influencer {
  id: number
  campaign_id: number
  username: string
  platform: 'instagram' | 'tiktok'
  full_name?: string
  followers_count: number
  aqs_score: number
  quality_audience: number
  budget?: number
  roi?: number
  status: 'suggested' | 'approved' | 'rejected' | 'contracted'
  created_at: string
  updated_at: string
}

export interface User {
  id: number
  email: string
  role: 'admin' | 'client'
  company_id?: number
  created_at: string
  updated_at: string
}

export interface AuthResponse {
  token: string
  user: User
  company?: Company
}
