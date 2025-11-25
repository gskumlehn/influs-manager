import { useState } from 'react'

import { CampaignSelector } from '@/components/admin/CampaignSelector'
import { InfluencerForm } from '@/components/admin/InfluencerForm'
import { InfluencerList } from '@/components/admin/InfluencerList'
import { Header } from '@/components/shared/Header'
import { Campaign } from '@/types'

export const AdminPage = () => {
  const [selectedCampaign, setSelectedCampaign] = useState<Campaign | null>(null)

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-2">Painel Administrativo</h2>
          <p className="text-gray-600">Gerencie campanhas e influenciadores</p>
        </div>
        <CampaignSelector onSelect={setSelectedCampaign} />
        {selectedCampaign && (
          <div className="mt-8 space-y-6">
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
              <h3 className="font-semibold text-blue-900">
                Campanha Selecionada: {selectedCampaign.name}
              </h3>
              {selectedCampaign.description && (
                <p className="text-sm text-blue-700 mt-1">{selectedCampaign.description}</p>
              )}
            </div>
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              <div className="lg:col-span-1">
                <InfluencerForm campaignId={selectedCampaign.id} />
              </div>
              <div className="lg:col-span-2">
                <InfluencerList campaignId={selectedCampaign.id} />
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  )
}
