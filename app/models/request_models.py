from typing import List, Optional
from pydantic import BaseModel

class ChatRequest(BaseModel):
    message: str

class ItineraryRequestGemini(BaseModel):
    duration: str
    trip_type: str
    visitor_type: str
    activity_types: list[str]
    travel_preferences: str
    preferences: str
    budget: float

class ActivityRequest(BaseModel):
    day: int
    time: str
    location: str
    full_address: Optional[str] = None
    activity_type: str
    notes: Optional[str] = None

# Pydantic model for Itinerary
class ItineraryRequest(BaseModel):
    user_uid: str
    title: str
    duration: int
    activity_type: str
    activities: List[ActivityRequest]
