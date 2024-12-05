import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini AI
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

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