from fastapi import APIRouter, HTTPException
from firebase_admin import auth

router = APIRouter()

@router.post("/verify-token/")
async def verify_token(token: str):
    try:
        decoded_token = auth.verify_id_token(token)
        return {"uid": decoded_token["uid"], "email": decoded_token["email"]}
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token")
