import traceback
from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel, EmailStr
from fastapi import Depends
from app.db import supabase

router = APIRouter(prefix="/auth", tags=["auth"])

class SignUpRequest(BaseModel):
    email: EmailStr
    name: str
    password: str

class SignInRequest(BaseModel):
    email: EmailStr
    password: str

async def get_current_user(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid token")
    
    token = authorization.split(" ")[1]
    try:
        user = supabase.auth.get_user(token)
        if not user or not user.user:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid token \n {traceback.format_exc()}")

@router.post("/signup")
async def signup(req: SignUpRequest):
    try:
        response = supabase.auth.sign_up({
            "email": req.email,
            "password": req.password,
            "options": {
                "data": {
                    "name": req.name
                }
            }
        })
        return {"message": "User created", "user": response.user}
    except Exception as e:
        print(f"Signup error: {type(e).__name__}: {str(e)}")
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=f"Signup failed: {str(e)} \n {traceback.format_exc()}")

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
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=f"Sigin failed: {str(e)} \n {traceback.format_exc()}")


@router.post("/signout")
async def signout(authorization: str = Header(None)):
    try:
        supabase.auth.sign_out()
        return {"message": "Signed out"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"{str(e)} \n {traceback.format_exc()}")
    
@router.get("/profile")
async def get_profile(user = Depends(get_current_user)):
    return {
        "id": user.user.id,
        "email": user.user.email,
        "name": user.user.user_metadata.get("name", "no_name_found"),
    }