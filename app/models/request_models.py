from pydantic import BaseModel

class ChatRequest(BaseModel):
    message: str

class ItineraryRequest(BaseModel):
    duration: str
    trip_type: str
    visitor_type: str
    activity_types: list[str]
    travel_preferences: str
    preferences: str
    budget: float
