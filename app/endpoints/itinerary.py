from fastapi import APIRouter, HTTPException
from app.models.request_models import PromptRequest
from app.models.response_models import ItineraryResponse
from app.utils.helpers import generate_prompt, query_openai

router = APIRouter()

@router.post("/ask-itinerary", response_model=ItineraryResponse)
async def ask_itinerary(request: PromptRequest):
    try:
        prompt = generate_prompt(request)
        itinerary_text = query_openai(prompt)
        itinerary_data = [{"day": i+1, "activity": item.strip()} for i, item in enumerate(itinerary_text.split("\n"))]
        return {"itinerary": itinerary_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
