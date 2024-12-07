from pydantic import BaseModel

class ChatRequest(BaseModel):
    message: str

class ItineraryRequest(BaseModel):
    duration: str
    activity_types: list[str]
    travel_preferences: str

class PromptRequest(BaseModel):
    duration: str
    activity_types: list[str]
    travel_preferences: str
