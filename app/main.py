from fastapi import FastAPI
from app.endpoints import chat, nearby, itinerary

app = FastAPI()

# Include routers
app.include_router(chat.router, prefix="/chat", tags=["Chat"])
app.include_router(nearby.router, prefix="/places", tags=["Places"])
app.include_router(itinerary.router, prefix="/itinerary", tags=["Itinerary"])