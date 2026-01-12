from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from backend.api.projects import router as projects_router
from backend.api.uploads import router as uploads_router
from backend.api.templates import router as templates_router

app = FastAPI(title="DMS")  # ✅ app must be defined BEFORE app.mount

ROOT = Path(__file__).resolve().parents[1]
FRONTEND_DIR = ROOT / "frontend"
INDEX_HTML = FRONTEND_DIR / "index.html"

# serve /assets/logo.png
app.mount("/assets", StaticFiles(directory=str(FRONTEND_DIR / "assets")), name="assets")

@app.get("/")
def home():
    return FileResponse(str(INDEX_HTML))

app.include_router(projects_router)
app.include_router(uploads_router, prefix="/upload")
app.include_router(templates_router, prefix="/templates")