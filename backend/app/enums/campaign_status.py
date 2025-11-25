from enum import Enum

class CampaignStatus(str, Enum):
    ACTIVE = "active"
    ARCHIVED = "archived"
    COMPLETED = "completed"
    DRAFT = "draft"
