from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

from app.enums.campaign_status import CampaignStatus
from app.infra.database import Base

class Campaign(Base):
    __tablename__ = "campaign"
    
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("company.id"), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    _status = Column("status", String(20), nullable=False, default="draft")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    company = relationship("Company", back_populates="campaigns")
    influencers = relationship("Influencer", back_populates="campaign")
    
    @hybrid_property
    def status(self):
        return CampaignStatus(self._status) if self._status else None
    
    @status.setter
    def status(self, value):
        self._status = value.value if value else None
    
    def to_dict(self):
        return {
            "id": self.id,
            "company_id": self.company_id,
            "name": self.name,
            "description": self.description,
            "status": self._status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
