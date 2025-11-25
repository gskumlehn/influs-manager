import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:5000/api',
  headers: {
    'Content-Type': 'application/json',
  },
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

export const authApi = {
  login: (email: string, password: string) =>
    api.post('/auth/login', { email, password }),
  register: (email: string, password: string, role: string, company_id?: number) =>
    api.post('/auth/register', { email, password, role, company_id }),
  me: () => api.get('/auth/me'),
}

export const companyApi = {
  getAll: () => api.get('/companies'),
  getById: (id: number) => api.get(`/companies/${id}`),
  create: (data: any) => api.post('/companies', data),
  update: (id: number, data: any) => api.put(`/companies/${id}`, data),
}

export const campaignApi = {
  getAll: (companyId?: number) =>
    api.get('/campaigns', { params: { company_id: companyId } }),
  getById: (id: number) => api.get(`/campaigns/${id}`),
  create: (data: any) => api.post('/campaigns', data),
  update: (id: number, data: any) => api.put(`/campaigns/${id}`, data),
}

export const influencerApi = {
  getByCampaign: (campaignId: number) =>
    api.get(`/campaigns/${campaignId}/influencers`),
  getById: (id: number) => api.get(`/influencers/${id}`),
  create: (campaignId: number, username: string, platform: string) =>
    api.post(`/campaigns/${campaignId}/influencers`, { username, platform }),
  update: (id: number, data: any) => api.put(`/influencers/${id}`, data),
  updateBudget: (id: number, budget: number) =>
    api.put(`/influencers/${id}/budget`, { budget }),
  updateStatus: (id: number, status: string) =>
    api.put(`/influencers/${id}/status`, { status }),
  delete: (id: number) => api.delete(`/influencers/${id}`),
}

export default api
