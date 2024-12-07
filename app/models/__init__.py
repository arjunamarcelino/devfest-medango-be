# app/models/__init__.py
from .request_models import ChatRequest, ItineraryRequest, PromptRequest
from .response_models import ItineraryResponse

# Expose all models for easy import
__all__ = ["ChatRequest", "ItineraryRequest", "PromptRequest", "ItineraryResponse"]