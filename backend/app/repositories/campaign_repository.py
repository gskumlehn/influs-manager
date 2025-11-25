from app.infra.database import get_session
from app.models.campaign import Campaign

class CampaignRepository:
    @staticmethod
    def create(campaign: Campaign) -> Campaign:
        with get_session() as session:
            session.add(campaign)
            session.flush()
            session.refresh(campaign)
            return campaign
    
    @staticmethod
    def find_all():
        with get_session() as session:
            campaigns = session.query(Campaign).all()
            return [c.to_dict() for c in campaigns]
    
    @staticmethod
    def find_by_company_id(company_id: int):
        with get_session() as session:
            campaigns = session.query(Campaign).filter(Campaign.company_id == company_id).all()
            return [c.to_dict() for c in campaigns]
    
    @staticmethod
    def find_by_id(campaign_id: int):
        with get_session() as session:
            campaign = session.query(Campaign).filter(Campaign.id == campaign_id).first()
            return campaign.to_dict() if campaign else None
    
    @staticmethod
    def update(campaign_id: int, data: dict):
        with get_session() as session:
            campaign = session.query(Campaign).filter(Campaign.id == campaign_id).first()
            if not campaign:
                return None
            for key, value in data.items():
                if hasattr(campaign, key):
                    setattr(campaign, key, value)
            session.flush()
            session.refresh(campaign)
            return campaign.to_dict()
