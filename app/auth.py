from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel, EmailStr
from app.db import supabase

router = APIRouter(prefix="/auth", tags=["auth"])

class SignUpRequest(BaseModel):
    email: EmailStr
    name: str
    password: str

class SignInRequest(BaseModel):
    email: EmailStr
    name: str
    password: str

@router.post("/signup")
async def signup(req: SignUpRequest):
    try:
        response = supabase.auth.sign_up({
            "email": req.email,
            "name": req.name,
            "password": req.password
        })
        return {"message": "User created", "user": response.user}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/signin")
async def signin(req: SignInRequest):
    try:
        response = supabase.auth.sign_in_with_password({
            "email": req.email,
            "password": req.password
        })
        return {
            "access_token": response.session.access_token,
            "refresh_token": response.session.refresh_token,
            "user": response.user
        }
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid credentials")

@router.post("/signout")
async def signout(authorization: str = Header(None)):
    try:
        supabase.auth.sign_out()
        return {"message": "Signed out"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Dependency to verify token
async def get_current_user(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid token")
    
    token = authorization.split(" ")[1]
    try:
        user = supabase.auth.get_user(token)
        return user
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token")