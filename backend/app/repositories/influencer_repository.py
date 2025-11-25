from app.infra.database import get_session
from app.models.influencer import Influencer

class InfluencerRepository:
    @staticmethod
    def create(influencer: Influencer) -> Influencer:
        with get_session() as session:
            session.add(influencer)
            session.flush()
            session.refresh(influencer)
            return influencer
    
    @staticmethod
    def delete(influencer_id: int):
        with get_session() as session:
            influencer = session.query(Influencer).filter(Influencer.id == influencer_id).first()
            if influencer:
                session.delete(influencer)
                return True
            return False
    
    @staticmethod
    def find_by_campaign_id(campaign_id: int):
        with get_session() as session:
            influencers = session.query(Influencer).filter(Influencer.campaign_id == campaign_id).all()
            return [i.to_dict() for i in influencers]
    
    @staticmethod
    def find_by_id(influencer_id: int):
        with get_session() as session:
            influencer = session.query(Influencer).filter(Influencer.id == influencer_id).first()
            return influencer.to_dict() if influencer else None
    
    @staticmethod
    def update(influencer_id: int, data: dict):
        with get_session() as session:
            influencer = session.query(Influencer).filter(Influencer.id == influencer_id).first()
            if not influencer:
                return None
            for key, value in data.items():
                if hasattr(influencer, key):
                    setattr(influencer, key, value)
            session.flush()
            session.refresh(influencer)
            return influencer.to_dict()
