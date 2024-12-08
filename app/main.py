import os
from fastapi import FastAPI
from app.endpoints import chat, nearby, itinerary, auth

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(chat.router, prefix="/chat", tags=["Chat"])
app.include_router(nearby.router, prefix="/places", tags=["Places"])
app.include_router(itinerary.router, prefix="/itinerary", tags=["Itinerary"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.app:app", host="0.0.0.0", log_level="info")