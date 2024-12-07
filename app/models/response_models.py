from pydantic import BaseModel

class ItineraryResponse(BaseModel):
    itinerary: list[dict]
