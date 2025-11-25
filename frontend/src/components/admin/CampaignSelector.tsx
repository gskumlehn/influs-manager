import { useQuery } from '@tanstack/react-query'
import { useState } from 'react'

import { campaignApi } from '@/services/api'
import { Campaign } from '@/types'

interface CampaignSelectorProps {
  onSelect: (campaign: Campaign) => void
}

export const CampaignSelector = ({ onSelect }: CampaignSelectorProps) => {
  const [selectedId, setSelectedId] = useState<number | null>(null)

  const { data: campaigns, isLoading } = useQuery({
    queryKey: ['campaigns'],
    queryFn: async () => {
      const response = await campaignApi.getAll()
      return response.data as Campaign[]
    },
  })

  const handleSelect = (campaign: Campaign) => {
    setSelectedId(campaign.id)
    onSelect(campaign)
  }

  if (isLoading) {
    return <div className="text-center py-8">Carregando campanhas...</div>
  }

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h2 className="text-xl font-bold mb-4">Selecione uma Campanha</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {campaigns?.map((campaign) => (
          <button
            key={campaign.id}
            onClick={() => handleSelect(campaign)}
            className={`p-4 border-2 rounded-lg text-left transition ${
              selectedId === campaign.id
                ? 'border-blue-500 bg-blue-50'
                : 'border-gray-200 hover:border-blue-300'
            }`}
          >
            <h3 className="font-semibold text-lg">{campaign.name}</h3>
            {campaign.description && (
              <p className="text-sm text-gray-600 mt-1">{campaign.description}</p>
            )}
            <span className={`inline-block mt-2 px-2 py-1 text-xs rounded ${
              campaign.status === 'active' ? 'bg-green-100 text-green-800' :
              campaign.status === 'draft' ? 'bg-gray-100 text-gray-800' :
              'bg-blue-100 text-blue-800'
            }`}>
              {campaign.status}
            </span>
          </button>
        ))}
      </div>
    </div>
  )
}
