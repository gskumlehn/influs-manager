import { useQuery } from '@tanstack/react-query'

import { InfluencerCard } from '@/components/client/InfluencerCard'
import { Header } from '@/components/shared/Header'
import { useAuth } from '@/hooks/useAuth'
import { campaignApi, influencerApi } from '@/services/api'
import { Campaign, Influencer } from '@/types'

export const ClientPage = () => {
  const { user } = useAuth()

  const { data: campaigns } = useQuery({
    queryKey: ['campaigns', user?.company_id],
    queryFn: async () => {
      const response = await campaignApi.getAll(user?.company_id)
      return response.data as Campaign[]
    },
    enabled: !!user?.company_id,
  })

  const activeCampaign = campaigns?.find(c => c.status === 'active') || campaigns?.[0]

  const { data: influencers, isLoading } = useQuery({
    queryKey: ['influencers', activeCampaign?.id],
    queryFn: async () => {
      if (!activeCampaign) return []
      const response = await influencerApi.getByCampaign(activeCampaign.id)
      return response.data as Influencer[]
    },
    enabled: !!activeCampaign,
  })

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-2">
            {activeCampaign?.name || 'Influenciadores Sugeridos'}
          </h2>
          {activeCampaign?.description && (
            <p className="text-gray-600">{activeCampaign.description}</p>
          )}
        </div>
        {isLoading ? (
          <div className="text-center py-12">Carregando influenciadores...</div>
        ) : influencers && influencers.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {influencers.map((influencer) => (
              <InfluencerCard
                key={influencer.id}
                influencer={influencer}
                campaignId={activeCampaign!.id}
              />
            ))}
          </div>
        ) : (
          <div className="text-center py-12 text-gray-500">
            Nenhum influenciador disponível para esta campanha.
          </div>
        )}
      </main>
    </div>
  )
}
