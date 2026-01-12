from fastapi import APIRouter
from fastapi.responses import FileResponse
from pathlib import Path

router = APIRouter()

TEMPLATE_PATH = Path("templates/Financial_Model_Template.xlsx")

@router.get("/financial")
def download_financial_template():
    if not TEMPLATE_PATH.exists():
        raise Exception("Financial template not found")

    return FileResponse(
        TEMPLATE_PATH,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        filename="Financial_Model_Template.xlsx"
    )