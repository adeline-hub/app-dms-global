from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List

from backend.services.upload_service import save_file
from backend.services.pipeline_service import run as run_pipeline

router = APIRouter()

@router.post("/{project_id}")
def upload_files(
    project_id: str,
    files: List[UploadFile] = File(...)
):
    if not files:
        raise HTTPException(status_code=400, detail="No files uploaded")

    results = []
    for file in files:
        results.append(save_file(project_id, file))

    # Run pipeline AFTER successful upload
    try:
        pipeline_result = run_pipeline(project_id)
    except Exception as e:
        pipeline_result = {
            "status": "pipeline_failed",
            "error": str(e)
        }

    return {
        "project_id": project_id,
        "uploaded": results,
        "pipeline": pipeline_result
    }