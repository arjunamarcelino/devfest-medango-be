from fastapi import APIRouter, Query, HTTPException
import requests
from app.config import GOOGLE_API_KEY, GOOGLE_PLACES_URL

router = APIRouter()

@router.get("/nearby")
def get_nearby(
    location: str = Query(..., description="Location in 'latitude,longitude' format"),
    radius: int = Query(3000, description="Search radius in meters"),
    type: str = Query(None, description="Type of place (e.g., restaurant, tourist_attraction)"),
    keyword: str = Query('populer', description="Search keyword (e.g., populer, favorit, viral)"),
    language: str = Query("id", description="Language of the response")
):
    """
    Get nearby places based on location, radius, and type.
    """
    params = {
        "key": GOOGLE_API_KEY,
        "location": location,
        "radius": radius,
        "type": type,
        "keyword": keyword,
        "language": language,
        "rankby": "prominence",
    }
    response = requests.get(GOOGLE_PLACES_URL, params=params)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch places")
    
    places = response.json().get("results", [])
    filtered_places = [place for place in places if place.get("rating", 0) >= 4.0]
    return {"places": filtered_places}
