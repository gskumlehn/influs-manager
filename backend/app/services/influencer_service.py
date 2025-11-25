import json

from app.infra.hypeauditor_client import HypeAuditorClient
from app.repositories.influencer_repository import InfluencerRepository

class InfluencerService:
    @staticmethod
    def calculate_quality_audience(followers: int, aqs: float) -> int:
        return int(followers * (aqs / 100))
    
    @staticmethod
    def calculate_roi(quality_audience: int, budget: float) -> float:
        if budget and budget > 0:
            return round(quality_audience / budget, 2)
        return None
    
    @staticmethod
    def create_influencer_from_hypeauditor(campaign_id: int, username: str, platform: str):
        client = HypeAuditorClient()
        try:
            if platform == "instagram":
                report = client.get_instagram_report(username)
            else:
                report = client.get_tiktok_report(username)
            metrics = client.extract_metrics(report)
            data = {
                "campaign_id": campaign_id,
                "username": username,
                "platform": platform,
                "full_name": metrics.get("full_name", ""),
                "followers_count": metrics.get("followers_count", 0),
                "aqs_score": metrics.get("aqs_score", 0),
                "quality_audience": metrics.get("quality_audience", 0),
                "status": "suggested",
                "hypeauditor_data": json.dumps(report)
            }
            return InfluencerRepository.create(data)
        except Exception as e:
            raise Exception(f"Erro ao buscar dados do HypeAuditor: {str(e)}")
    
    @staticmethod
    def delete_influencer(influencer_id: int):
        return InfluencerRepository.delete(influencer_id)
    
    @staticmethod
    def get_influencer_by_id(influencer_id: int):
        return InfluencerRepository.find_by_id(influencer_id)
    
    @staticmethod
    def get_influencers_by_campaign(campaign_id: int):
        return InfluencerRepository.find_by_campaign_id(campaign_id)
    
    @staticmethod
    def update_budget(influencer_id: int, budget: float):
        influencer = InfluencerRepository.find_by_id(influencer_id)
        if not influencer:
            return None
        roi = InfluencerService.calculate_roi(influencer["quality_audience"], budget)
        return InfluencerRepository.update(influencer_id, {"budget": budget, "roi": roi})
    
    @staticmethod
    def update_influencer(influencer_id: int, data: dict):
        return InfluencerRepository.update(influencer_id, data)
    
    @staticmethod
    def update_status(influencer_id: int, status: str):
        return InfluencerRepository.update(influencer_id, {"status": status})
