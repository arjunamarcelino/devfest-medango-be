import os
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
import google.generativeai as genai
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()

# Configure Gemini AI
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Base URL for Google Places API
GOOGLE_PLACES_URL = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"

# Create the model
generation_config = {
    "temperature": 0.5,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction=(
        "Tujuan: Menyediakan informasi komprehensif dan akurat tentang Kota Medan "
        "serta sekitarnya kepada pengguna, baik warga lokal maupun wisatawan, untuk "
        "membantu mereka merencanakan aktivitas dan perjalanan.\n\n"
        "Persona Chatbot: Seorang penduduk lokal Medan yang ramah, informatif, dan "
        "up-to-date dengan segala hal yang terjadi di kota.\n\n"
        "Fokus: Rekomendasi itinerary, tempat wisata, kuliner, aktivitas, dan informasi umum tentang Medan."
    ),
)

# Create FastAPI app
app = FastAPI()

# Define input data model
class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat(request: ChatRequest):
    """Chat endpoint that processes user messages and returns AI responses."""
    try:
        # Start a chat session
        chat_session = model.start_chat(
            history=[
                {
                    "role": "model",
                    "parts": [
                        "Halo, ada yang mau kau tanya?",
                    ],
                },
            ]
        )

        # Send the user's message
        response = chat_session.send_message(request.message)
        return {"response": response.text}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
      
@app.get("/nearby-places")
def get_nearby_places(
    location: str = Query(..., description="Location in 'latitude,longitude' format"),
    radius: int = Query(1000, description="Search radius in meters"),
    type: str = Query(None, description="Type of place (e.g., restaurant, park)"),
):
    """
    Get nearby places based on location, radius, and type.
    """
    params = {
        "key": GOOGLE_API_KEY,
        "location": location,
        "radius": radius,
        "type": type,  # Optional filter for place type
    }
    response = requests.get(GOOGLE_PLACES_URL, params=params)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch places")

    return response.json()