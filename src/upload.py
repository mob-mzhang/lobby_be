from fastapi import APIRouter, File, UploadFile, Depends, HTTPException
from sqlalchemy.orm import Session
from src.database import get_db
from src.crud import users_crud
from supabase import create_client, Client
import os
import uuid

router = APIRouter()

# Initialize Supabase client
supabase_url ="https://icwupqucbnxynldgqxaq.supabase.co"
supabase_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imljd3VwcXVjYm54eW5sZGdxeGFxIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTcyODQzMTA4NiwiZXhwIjoyMDQ0MDA3MDg2fQ.Ao-QT5dCDUVRu9KBDowcNBgUFFmsUKiQzSLAYq8RgrY"
supabase: Client = create_client(supabase_url, supabase_key)

@router.post("/{user_id}")
async def upload_image(user_id: str, file: UploadFile = File(...), db: Session = Depends(get_db)):
    # Check if user exists
    user = users_crud.get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    try:
        # Read file content
        content = await file.read()
        
        # Generate a unique filename
        file_extension = os.path.splitext(file.filename)[1]
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        
        # Upload file to Supabase Storage
        bucket_name = "avatars"  # Replace with your actual bucket name
        file_path = f"{user_id}/{unique_filename}"
        
        response = supabase.storage.from_(bucket_name).upload(file_path, content)
        
        # Check if the upload was successful
        if not response:
            raise HTTPException(status_code=500, detail="Failed to upload image")
        
        # Get the public URL of the uploaded file
        public_url = supabase.storage.from_(bucket_name).get_public_url(file_path)
        
        # Ensure we have a valid public URL
        if not public_url:
            raise HTTPException(status_code=500, detail="Failed to get public URL for uploaded image")
        
        # Here you might want to save the public_url to your database, associated with the user
        # For example:
        # users_crud.update_user_image(db, user_id=user_id, image_url=public_url)
        
        return {"message": "Image uploaded successfully", "image_url": public_url}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
