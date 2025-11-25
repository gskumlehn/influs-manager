import { useMutation, useQueryClient } from '@tanstack/react-query'
import { useState } from 'react'

import { influencerApi } from '@/services/api'

interface InfluencerFormProps {
  campaignId: number
}

export const InfluencerForm = ({ campaignId }: InfluencerFormProps) => {
  const [username, setUsername] = useState('')
  const [platform, setPlatform] = useState<'instagram' | 'tiktok'>('instagram')
  const [error, setError] = useState('')
  const queryClient = useQueryClient()

  const createMutation = useMutation({
    mutationFn: () => influencerApi.create(campaignId, username, platform),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['influencers', campaignId] })
      setUsername('')
      setError('')
    },
    onError: (err: any) => {
      setError(err.response?.data?.error || 'Erro ao adicionar influenciador')
    },
  })

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (!username.trim()) {
      setError('Username é obrigatório')
      return
    }
    createMutation.mutate()
  }

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h3 className="text-lg font-semibold mb-4">Adicionar Influenciador</h3>
      <form onSubmit={handleSubmit} className="space-y-4">
        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded text-sm">
            {error}
          </div>
        )}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Username (sem @)
          </label>
          <input
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            placeholder="papelitobrasil"
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Plataforma
          </label>
          <select
            value={platform}
            onChange={(e) => setPlatform(e.target.value as 'instagram' | 'tiktok')}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="instagram">Instagram</option>
            <option value="tiktok">TikTok</option>
          </select>
        </div>
        <button
          type="submit"
          disabled={createMutation.isPending}
          className="w-full px-4 py-2 text-white bg-blue-600 hover:bg-blue-700 rounded-md disabled:opacity-50"
        >
          {createMutation.isPending ? 'Adicionando...' : 'Adicionar'}
        </button>
      </form>
    </div>
  )
}
