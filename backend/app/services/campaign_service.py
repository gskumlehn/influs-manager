from app.enums.campaign_status import CampaignStatus
from app.models.campaign import Campaign
from app.repositories.campaign_repository import CampaignRepository

class CampaignService:
    @staticmethod
    def create_campaign(company_id: int, name: str, description: str = None, 
                       status: CampaignStatus = CampaignStatus.DRAFT):
        campaign = Campaign()
        campaign.company_id = company_id
        campaign.name = name
        campaign.description = description
        campaign.status = status
        created = CampaignRepository.create(campaign)
        return created.to_dict()
    
    @staticmethod
    def get_all_campaigns():
        return CampaignRepository.find_all()
    
    @staticmethod
    def get_campaign_by_id(campaign_id: int):
        return CampaignRepository.find_by_id(campaign_id)
    
    @staticmethod
    def get_campaigns_by_company(company_id: int):
        return CampaignRepository.find_by_company_id(company_id)
    
    @staticmethod
    def update_campaign(campaign_id: int, data: dict):
        return CampaignRepository.update(campaign_id, data)
