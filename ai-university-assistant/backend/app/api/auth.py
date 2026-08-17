from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import jwt
import os
from datetime import datetime, timedelta

router = APIRouter()

class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    username: str

# Simple credentials (in production, use database)
VALID_CREDENTIALS = {
    "student": "password123",
    "admin": "admin123"
}

SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")

@router.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest):
    """Login user"""
    
    # Validate credentials
    if request.username not in VALID_CREDENTIALS:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    if VALID_CREDENTIALS[request.username] != request.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Create token
    payload = {
        "username": request.username,
        "exp": datetime.utcnow() + timedelta(hours=24)
    }
    
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    
    return LoginResponse(
        access_token=token,
        token_type="bearer",
        username=request.username
    )

@router.post("/logout")
async def logout():
    """Logout user"""
    return {"message": "Logged out successfully"}

@router.get("/me")
async def get_current_user(token: str = None):
    """Get current user info"""
    
    if not token:
        raise HTTPException(status_code=401, detail="No token provided")
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        username = payload.get("username")
        return {"username": username}
    
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
