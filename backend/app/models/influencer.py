from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

from app.enums.influencer_status import InfluencerStatus
from app.enums.platform import Platform
from app.infra.database import Base

class Influencer(Base):
    __tablename__ = "influencer"
    
    id = Column(Integer, primary_key=True, index=True)
    campaign_id = Column(Integer, ForeignKey("campaign.id"), nullable=False)
    username = Column(String(100), nullable=False)
    _platform = Column("platform", String(20), nullable=False)
    full_name = Column(String(255), nullable=True)
    followers_count = Column(Integer, nullable=False, default=0)
    aqs_score = Column(Numeric(5, 2), nullable=False, default=0)
    quality_audience = Column(Integer, nullable=False, default=0)
    budget = Column(Numeric(12, 2), nullable=True)
    roi = Column(Numeric(12, 2), nullable=True)
    _status = Column("status", String(20), nullable=False, default="suggested")
    hypeauditor_data = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    campaign = relationship("Campaign", back_populates="influencers")
    
    @hybrid_property
    def platform(self):
        return Platform(self._platform) if self._platform else None
    
    @platform.setter
    def platform(self, value):
        self._platform = value.value if value else None
    
    @hybrid_property
    def status(self):
        return InfluencerStatus(self._status) if self._status else None
    
    @status.setter
    def status(self, value):
        self._status = value.value if value else None
    
    def to_dict(self):
        return {
            "id": self.id,
            "campaign_id": self.campaign_id,
            "username": self.username,
            "platform": self._platform,
            "full_name": self.full_name,
            "followers_count": self.followers_count,
            "aqs_score": float(self.aqs_score) if self.aqs_score else 0,
            "quality_audience": self.quality_audience,
            "budget": float(self.budget) if self.budget else None,
            "roi": float(self.roi) if self.roi else None,
            "status": self._status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
