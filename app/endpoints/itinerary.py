import re
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from requests import Session
from app.models.db_models import User, Itinerary, Activity  # Ensure your models are imported
from app.models.request_models import ItineraryRequest  # Pydantic models
from app.database import get_db  # Your database session dependency
from app.models.request_models import ItineraryRequestGemini
import json
from app.config import model
from app.models.response_models import ItineraryResponse
from app.utils.helpers import generate_prompt

router = APIRouter()

@router.post("/ask-itinerary")
async def ask_itinerary(request: ItineraryRequestGemini):
    try:
        # Generate the prompt based on the user's request
        prompt = generate_prompt(request)
        
        # Assuming model.start_chat() and chat_session.send_message() are part of your Gemini API setup
        chat_session = model.start_chat()
        response = chat_session.send_message(prompt)
        
        # print(response)  # For debugging purposes
        
        # Extract the response text containing the JSON data
        response_text = response.candidates[0].content.parts[0].text.strip()
        
        # print("Raw Response Text:")
        # print(response_text)  # Print the raw response for inspection
        
        # Clean the response: remove unnecessary prefixes/suffixes around JSON
        response_text = response_text.replace("```json\n", "").replace("\n```", "").strip()

        # Optionally, check if there is extra data after the JSON content (like debugging logs, etc.)
        if response_text.endswith('}') or response_text.endswith(']'):
            try:
                # Try to parse the cleaned response as JSON
                itinerary_json = json.loads(response_text)
                # print("Parsed JSON:")
                # print(itinerary_json)  # Print the parsed JSON to check
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
    
@router.post("/save")
async def save_itinerary(itinerary: ItineraryRequest, db: Session = Depends(get_db)):
    try:
        # Step 1: Check if user exists
        user = db.query(User).filter(User.uid == itinerary.user_uid).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Step 2: Create new Itinerary record
        new_itinerary = Itinerary(
            user_id=user.id,
            title=itinerary.title,
            duration=itinerary.duration,
            activity_type=itinerary.activity_type
        )
        db.add(new_itinerary)
        db.commit()
        db.refresh(new_itinerary)

        # Step 3: Create new Activity records for the itinerary
        activities = []
        for activity in itinerary.activities:
            new_activity = Activity(
                itinerary_id=new_itinerary.id,
                day=activity.day,
                time=activity.time,
                location=activity.location,
                full_address=activity.full_address,
                activity_type=activity.activity_type,
                notes=activity.notes
            )
            activities.append(new_activity)
        
        # Save activities to the database
        db.add_all(activities)
        db.commit()

        # Step 4: Return the created itinerary as a response
        return itinerary

    except Exception as e:
        db.rollback()  # Rollback in case of any error
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/user/{user_uid}", response_model=List[ItineraryResponse])
async def get_itineraries_by_user_uid(user_uid: str, db: Session = Depends(get_db)):
    # Find the user by UID
    user = db.query(User).filter(User.uid == user_uid).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Get the itineraries for the user
    itineraries = db.query(Itinerary).filter(Itinerary.user_id == user.id).all()
    if not itineraries:
        raise HTTPException(status_code=404, detail="No itineraries found for this user")

    # Fetch activities for each itinerary and format the response
    result = []
    for itinerary in itineraries:
        activities = db.query(Activity).filter(Activity.itinerary_id == itinerary.id).all()
        
        # Extract only the numeric part of the duration using regex
        duration_match = re.search(r"\d+", itinerary.duration)
        duration = int(duration_match.group()) if duration_match else 0 
        
        itinerary_with_activities = {
            "id": itinerary.id,
            "title": itinerary.title,
            "duration": duration,
            "activity_type": itinerary.activity_type,
            "activities": activities,
        }
        result.append(itinerary_with_activities)

    return result
