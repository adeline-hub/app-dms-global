import os
from fastapi import UploadFile, HTTPException

ALLOWED_EXTENSIONS = {".pdf", ".docx", ".xlsx", ".pptx"}
MAX_FILE_SIZE_MB = 20

def save_file(project_id: str, file: UploadFile):
    base = f"projects/{project_id}"

    # 1️⃣ Project exists
    if not os.path.isdir(base):
        raise HTTPException(status_code=404, detail="Project not found")

    # 2️⃣ Extension check
    _, ext = os.path.splitext(file.filename.lower())
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type: {ext}"
        )

    # 3️⃣ Size check
    file.file.seek(0, os.SEEK_END)
    size_mb = file.file.tell() / (1024 * 1024)
    file.file.seek(0)

    if size_mb > MAX_FILE_SIZE_MB:
        raise HTTPException(
            status_code=413,
            detail=f"File too large ({size_mb:.1f}MB)"
        )

    # 4️⃣ Save
    raw = f"{base}/raw_docs"
    os.makedirs(raw, exist_ok=True)

    path = f"{raw}/{file.filename}"
    with open(path, "wb") as f:
        f.write(file.file.read())

    return {
        "filename": file.filename,
        "size_mb": round(size_mb, 2),
        "status": "uploaded"
    }