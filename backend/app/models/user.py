from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

from app.enums.user_role import UserRole
from app.infra.database import Base

class User(Base):
    __tablename__ = "user"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    _role = Column("role", String(20), nullable=False)
    company_id = Column(Integer, ForeignKey("company.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    company = relationship("Company", back_populates="users")
    
    @hybrid_property
    def role(self):
        return UserRole(self._role) if self._role else None
    
    @role.setter
    def role(self, value):
        self._role = value.value if value else None
    
    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "role": self._role,
            "company_id": self.company_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
