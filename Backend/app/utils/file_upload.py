import os
import uuid
from fastapi import UploadFile, HTTPException

UPLOAD_DIR = os.path.join(os.getcwd(), "uploads", "documents")

ALLOWED_EXTENSIONS = {".pdf", ".png", ".jpg", ".jpeg", ".webp"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB


def save_upload_file(upload_file: UploadFile) -> str:
    """
    Saves an uploaded file locally and returns its public URL path.
    """
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    filename = upload_file.filename or "document"
    ext = os.path.splitext(filename)[1].lower()

    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file format '{ext}'. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
        )

    unique_filename = f"{uuid.uuid4().hex}_{filename.replace(' ', '_')}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)

    # Read and validate size
    contents = upload_file.file.read()
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail="File size exceeds maximum allowed limit (10MB)"
        )

    with open(file_path, "wb") as f:
        f.write(contents)

    # Return accessible relative path URL
    return f"/uploads/documents/{unique_filename}"
