# app/endpoints/__init__.py
from .chat import router as chat_router
from .nearby import router as nearby_places_router
from .itinerary import router as itinerary_router

# Expose all routers for easy import
__all__ = ["chat_router", "nearby_places_router", "itinerary_router"]
