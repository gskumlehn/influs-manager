import { useMutation, useQueryClient } from '@tanstack/react-query'

import { influencerApi } from '@/services/api'
import { Influencer } from '@/types'

interface InfluencerCardProps {
  influencer: Influencer
  campaignId: number
}

export const InfluencerCard = ({ influencer, campaignId }: InfluencerCardProps) => {
  const queryClient = useQueryClient()

  const updateStatusMutation = useMutation({
    mutationFn: (status: string) => influencerApi.updateStatus(influencer.id, status),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['influencers', campaignId] })
    },
  })

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <div className="flex justify-between items-start mb-4">
        <div>
          <h3 className="text-lg font-semibold">@{influencer.username}</h3>
          {influencer.full_name && (
            <p className="text-sm text-gray-600">{influencer.full_name}</p>
          )}
        </div>
        <span className={`px-3 py-1 text-xs rounded ${
          influencer.platform === 'instagram' ? 'bg-pink-100 text-pink-800' : 'bg-black text-white'
        }`}>
          {influencer.platform}
        </span>
      </div>
      <div className="space-y-2 mb-4">
        <div className="flex justify-between text-sm">
          <span className="text-gray-600">Seguidores:</span>
          <span className="font-medium">{influencer.followers_count.toLocaleString()}</span>
        </div>
        <div className="flex justify-between text-sm">
          <span className="text-gray-600">AQS:</span>
          <span className="font-medium">{influencer.aqs_score}%</span>
        </div>
        <div className="flex justify-between text-sm">
          <span className="text-gray-600">Público de Qualidade:</span>
          <span className="font-medium">{influencer.quality_audience.toLocaleString()}</span>
        </div>
        {influencer.budget && (
          <>
            <div className="flex justify-between text-sm">
              <span className="text-gray-600">Orçamento:</span>
              <span className="font-medium">R$ {influencer.budget.toLocaleString()}</span>
            </div>
            <div className="flex justify-between text-sm">
              <span className="text-gray-600">ROI:</span>
              <span className="font-medium">{influencer.roi?.toFixed(2)}</span>
            </div>
          </>
        )}
      </div>
      <div className="flex space-x-2">
        <button
          onClick={() => updateStatusMutation.mutate('approved')}
          disabled={influencer.status === 'approved'}
          className="flex-1 px-4 py-2 text-sm font-medium text-white bg-green-600 hover:bg-green-700 rounded-md disabled:opacity-50"
        >
          Aprovar
        </button>
        <button
          onClick={() => updateStatusMutation.mutate('rejected')}
          disabled={influencer.status === 'rejected'}
          className="flex-1 px-4 py-2 text-sm font-medium text-white bg-red-600 hover:bg-red-700 rounded-md disabled:opacity-50"
        >
          Rejeitar
        </button>
      </div>
      <div className="mt-3 text-center">
        <span className={`inline-block px-3 py-1 text-xs rounded ${
          influencer.status === 'approved' ? 'bg-green-100 text-green-800' :
          influencer.status === 'rejected' ? 'bg-red-100 text-red-800' :
          influencer.status === 'contracted' ? 'bg-blue-100 text-blue-800' :
          'bg-yellow-100 text-yellow-800'
        }`}>
          Status: {influencer.status}
        </span>
      </div>
    </div>
  )
}
