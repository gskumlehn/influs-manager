from enum import Enum

class InfluencerStatus(str, Enum):
    APPROVED = "approved"
    CONTRACTED = "contracted"
    REJECTED = "rejected"
    SUGGESTED = "suggested"
