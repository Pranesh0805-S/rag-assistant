from fastapi import APIRouter, HTTPException, status, Depends
from datetime import datetime, timedelta
from pydantic import BaseModel, EmailStr

from app.models.user import UserCreate, UserLogin, UserOut
from app.core.database import users_collection
from app.core.security import hash_password, verify_password, create_access_token
from app.core.otp import generate_otp, send_otp_email
from app.core.deps import get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])


class OTPVerify(BaseModel):
    email: EmailStr
    otp: str


@router.post("/signup", status_code=status.HTTP_201_CREATED)
def signup(user: UserCreate):
    existing = users_collection.find_one({"email": user.email})
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pw = hash_password(user.password)
    otp = generate_otp()
    otp_expiry = datetime.utcnow() + timedelta(minutes=10)

    new_user = {
        "name": user.name,
        "email": user.email,
        "password": hashed_pw,
        "is_verified": False,
        "otp": otp,
        "otp_expiry": otp_expiry,
        "created_at": datetime.utcnow()
    }
    result = users_collection.insert_one(new_user)

    send_otp_email(user.email, otp)

    return {"message": "Signup successful, OTP sent to email", "user_id": str(result.inserted_id)}


@router.post("/verify-otp")
def verify_otp(data: OTPVerify):
    user = users_collection.find_one({"email": data.email})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.get("is_verified"):
        return {"message": "Already verified"}

    if user.get("otp") != data.otp:
        raise HTTPException(status_code=400, detail="Invalid OTP")

    if datetime.utcnow() > user.get("otp_expiry"):
        raise HTTPException(status_code=400, detail="OTP expired")

    users_collection.update_one(
        {"email": data.email},
        {"$set": {"is_verified": True}, "$unset": {"otp": "", "otp_expiry": ""}}
    )
    return {"message": "Email verified successfully"}


@router.post("/login")
def login(credentials: UserLogin):
    user = users_collection.find_one({"email": credentials.email})
    if not user or not verify_password(credentials.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    if not user.get("is_verified"):
        raise HTTPException(status_code=403, detail="Email not verified. Please verify OTP first.")

    token = create_access_token({"sub": str(user["_id"]), "email": user["email"]})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me")
def get_me(current_user: dict = Depends(get_current_user)):
    return {
        "id": str(current_user["_id"]),
        "name": current_user["name"],
        "email": current_user["email"],
        "is_verified": current_user["is_verified"]
    }