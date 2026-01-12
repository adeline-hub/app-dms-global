from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pathlib import Path

from backend.models.project import ProjectCreate
from backend.services.project_service import create_project

router = APIRouter()

@router.post("/projects")
def create_project_endpoint(project: ProjectCreate):
    return create_project(project)

@router.get("/projects/{project_id}/deck")
def download_deck(project_id: str, audience: str = "investor"):
    deck_path = Path(f"outputs/{project_id}-{audience}.pptx")

    if not deck_path.exists():
        raise HTTPException(
            status_code=404,
            detail="Deck not found. Upload files to run pipeline and generate deck first."
        )

    return FileResponse(
        deck_path,
        media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
        filename=f"{project_id}-{audience}.pptx"
    )