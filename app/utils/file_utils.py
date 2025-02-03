import os
from pathlib import Path
from uuid import uuid4
from fastapi import UploadFile, HTTPException
import shutil

# Define base directories
BASE_DIR = Path(__file__).resolve().parent.parent
UPLOAD_DIR = BASE_DIR / "uploads"

# Create uploads directory if it doesn't exist
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Helper function to save uploaded files
async def save_upload_file(upload_file: UploadFile) -> str:
    try:
        # Generate a unique filename
        file_extension = os.path.splitext(upload_file.filename)[1]
        unique_filename = f"{uuid4()}{file_extension}"
        file_path = UPLOAD_DIR / unique_filename

        # Save the uploaded file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(upload_file.file, buffer)

        # Return the relative URL to the uploaded file
        return f"/uploads/{unique_filename}"
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File upload failed: {str(e)}")
