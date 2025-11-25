import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { useState } from 'react'

import { influencerApi } from '@/services/api'
import { Influencer } from '@/types'

interface InfluencerListProps {
  campaignId: number
}

export const InfluencerList = ({ campaignId }: InfluencerListProps) => {
  const [editingBudget, setEditingBudget] = useState<number | null>(null)
  const [budgetValue, setBudgetValue] = useState('')
  const queryClient = useQueryClient()

  const { data: influencers, isLoading } = useQuery({
    queryKey: ['influencers', campaignId],
    queryFn: async () => {
      const response = await influencerApi.getByCampaign(campaignId)
      return response.data as Influencer[]
    },
  })

  const updateBudgetMutation = useMutation({
    mutationFn: ({ id, budget }: { id: number; budget: number }) =>
      influencerApi.updateBudget(id, budget),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['influencers', campaignId] })
      setEditingBudget(null)
      setBudgetValue('')
    },
  })

  const deleteMutation = useMutation({
    mutationFn: (id: number) => influencerApi.delete(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['influencers', campaignId] })
    },
  })

  const handleSaveBudget = (id: number) => {
    const budget = parseFloat(budgetValue)
    if (!isNaN(budget)) {
      updateBudgetMutation.mutate({ id, budget })
    }
  }

  if (isLoading) {
    return <div className="text-center py-8">Carregando influenciadores...</div>
  }

  return (
    <div className="bg-white rounded-lg shadow overflow-hidden">
      <div className="px-6 py-4 border-b border-gray-200">
        <h3 className="text-lg font-semibold">Influenciadores</h3>
      </div>
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Username</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Plataforma</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Seguidores</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">AQS</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Público Qualidade</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Orçamento</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">ROI</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Ações</th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {influencers?.map((influencer) => (
              <tr key={influencer.id}>
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                  @{influencer.username}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {influencer.platform}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {influencer.followers_count.toLocaleString()}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {influencer.aqs_score}%
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {influencer.quality_audience.toLocaleString()}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {editingBudget === influencer.id ? (
                    <div className="flex items-center space-x-2">
                      <input
                        type="number"
                        value={budgetValue}
                        onChange={(e) => setBudgetValue(e.target.value)}
                        className="w-24 px-2 py-1 border border-gray-300 rounded"
                      />
                      <button
                        onClick={() => handleSaveBudget(influencer.id)}
                        className="text-green-600 hover:text-green-800"
                      >
                        ✓
                      </button>
                      <button
                        onClick={() => setEditingBudget(null)}
                        className="text-red-600 hover:text-red-800"
                      >
                        ✗
                      </button>
                    </div>
                  ) : (
                    <button
                      onClick={() => {
                        setEditingBudget(influencer.id)
                        setBudgetValue(influencer.budget?.toString() || '')
                      }}
                      className="text-blue-600 hover:text-blue-800"
                    >
                      {influencer.budget ? `R$ ${influencer.budget.toLocaleString()}` : 'Adicionar'}
                    </button>
                  )}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {influencer.roi ? influencer.roi.toFixed(2) : '-'}
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <span className={`px-2 py-1 text-xs rounded ${
                    influencer.status === 'approved' ? 'bg-green-100 text-green-800' :
                    influencer.status === 'rejected' ? 'bg-red-100 text-red-800' :
                    influencer.status === 'contracted' ? 'bg-blue-100 text-blue-800' :
                    'bg-yellow-100 text-yellow-800'
                  }`}>
                    {influencer.status}
                  </span>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm">
                  <button
                    onClick={() => deleteMutation.mutate(influencer.id)}
                    className="text-red-600 hover:text-red-800"
                  >
                    Remover
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
