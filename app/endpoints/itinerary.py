from fastapi import APIRouter, HTTPException
from app.models.request_models import ItineraryRequest
from app.models.response_models import ItineraryResponse
import json
from app.config import model
from app.utils.helpers import generate_prompt

router = APIRouter()

@router.post("/ask-itinerary", response_model=ItineraryResponse)
async def ask_itinerary(request: ItineraryRequest):
    try:
        # Generate the prompt based on the user's request
        prompt = generate_prompt(request)
        
        # Assuming model.start_chat() and chat_session.send_message() are part of your Gemini API setup
        chat_session = model.start_chat()
        response = chat_session.send_message(prompt)
        
        print(response)  # For debugging purposes
        
        # Extract the response text containing the JSON data
        response_text = response.candidates[0].content.parts[0].text.strip()
        
        print("Raw Response Text:")
        print(response_text)  # Print the raw response for inspection
        
        # Clean the response: remove unnecessary prefixes/suffixes around JSON
        response_text = response_text.replace("```json\n", "").replace("\n```", "").strip()

        # Optionally, check if there is extra data after the JSON content (like debugging logs, etc.)
        if response_text.endswith('}') or response_text.endswith(']'):
            try:
                # Try to parse the cleaned response as JSON
                itinerary_json = json.loads(response_text)
                print("Parsed JSON:")
                print(itinerary_json)  # Print the parsed JSON to check
            except json.JSONDecodeError as e:
                raise HTTPException(status_code=500, detail=f"JSON decoding error: {str(e)}")
        else:
            raise HTTPException(status_code=500, detail="Invalid JSON structure or extra data after JSON content")

        # Extract the itinerary list
        itinerary_data = itinerary_json.get("itinerary", [])
        
        # Extract the notes (final note about budget, tips, etc.)
        notes = itinerary_json.get("notes", "")

        # If notes are missing, set a default message
        if not notes:
            notes = "No additional notes provided."

        # Return the itinerary data along with the final note
        return {"itinerary": itinerary_data, "notes": notes}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))