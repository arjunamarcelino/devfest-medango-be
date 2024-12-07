from fastapi import APIRouter, HTTPException
from app.config import model
from app.models.request_models import ChatRequest

router = APIRouter()

@router.post("/chat")
async def chat(request: ChatRequest):
    """Chat endpoint that processes user messages and returns AI responses."""
    try:
        chat_session = model.start_chat(
            history=[
                {
                    "role": "model",
                    "parts": [
                        "Saya LekGo, pemandu wisata virtual yang sangat berpengetahuan, ramah, dan menarik untuk Medan. Saya ahli dalam hal objek wisata, makanan, budaya, sejarah, dan harta karun tersembunyi di Medan.",
                    ],
                },
            ]
        )
        response = chat_session.send_message(request.message)
        return {"response": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
