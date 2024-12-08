from pydantic import BaseModel
from typing import List, Optional

# Pydantic model for Activity
class ActivityResponse(BaseModel):
    id: int
    day: int
    time: str
    location: str
    full_address: str
    activity_type: str
    notes: Optional[str] = None

    class Config:
        from_attributes = True  # Use from_attributes for serializing SQLAlchemy models


# Pydantic model for Itinerary
class ItineraryResponse(BaseModel):
    id: int
    title: str
    duration: int
    activity_type: str
    activities: List[ActivityResponse]  # List of activities for each itinerary

    class Config:
        from_attributes = True  # Use from_attributes for serializing SQLAlchemy models
