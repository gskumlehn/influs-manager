from app.repositories.campaign_repository import CampaignRepository

class CampaignService:
    @staticmethod
    def create_campaign(company_id: int, name: str, description: str = None, 
                       status: str = "draft"):
        data = {
            "company_id": company_id,
            "name": name,
            "description": description,
            "status": status
        }
        return CampaignRepository.create(data)
    
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
