from fastapi import APIRouter, HTTPException, Depends
from supabase import create_client, Client
from pydantic import BaseModel
from .database import get_db
from sqlalchemy.orm import Session
from .crud import users_crud
from .schemas import UserLogin

router = APIRouter()

# Replace with your Supabase project URL and API key

supabase_url = "https://icwupqucbnxynldgqxaq.supabase.co"
supabase_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imljd3VwcXVjYm54eW5sZGdxeGFxIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTcyODQzMTA4NiwiZXhwIjoyMDQ0MDA3MDg2fQ.Ao-QT5dCDUVRu9KBDowcNBgUFFmsUKiQzSLAYq8RgrY"
supabase: Client = create_client(supabase_url, supabase_key)


class OTPVerify(BaseModel):
    phone: str
    token: str


@router.post("/login")
async def login(user_data: UserLogin):
    try:
        # Send OTP to the user's phone number
        response = supabase.auth.sign_in_with_otp(
            {"phone": user_data.phone_number})
        return {"message": "OTP sent successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/verify")
async def verify(verify_data: OTPVerify, db: Session = Depends(get_db)):
    try:
        # Verify the OTP
        response = supabase.auth.verify_otp({
            "phone": verify_data.phone,
            "token": verify_data.token,
            "type": "sms"
        })

        # Get the user's ID from the Supabase response
        user_id = response.user.id

        # Check if the user exists in your database
        db_user = users_crud.get_user(db, user_id)

        if not db_user:
            # If the user doesn't exist in your database, create a new user
            new_user = {
                "id": user_id,
                # You might want to use a different field for username
                "username": response.user.phone,
                "phone_number": response.user.phone,
            }
            db_user = users_crud.create_user(db, new_user)

        # Return the access token and user data
        return {
            "access_token": response.session.access_token,
            "token_type": "bearer",
            "user": db_user
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Add this router to your main FastAPI app
