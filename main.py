from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from dotenv import load_dotenv
import os
from pathlib import Path

# Load .env from same directory as this file
load_dotenv(Path(__file__).parent / ".env")

from parser_engine import ResumeParser

app = FastAPI(title="Resume Parser API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Find index.html — works whether files are flat or in backend/frontend subfolders
_here = Path(__file__).parent
_candidates = [
    _here / "frontend" / "index.html",   # backend/frontend/index.html
    _here.parent / "frontend" / "index.html",  # ../frontend/index.html
    _here / "index.html",                 # flat: same folder as main.py
]
FRONTEND_HTML = next((p for p in _candidates if p.exists()), None)

parser = ResumeParser()


@app.get("/")
async def root():
    if FRONTEND_HTML:
        return FileResponse(str(FRONTEND_HTML))
    return HTMLResponse("<h2>Put index.html next to main.py or in a frontend/ subfolder.</h2>")


@app.post("/parse")
async def parse_resume(file: UploadFile = File(...)):
    ext = Path(file.filename).suffix.lower().lstrip(".")
    if ext not in ["pdf", "docx", "doc", "txt"]:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type: .{ext}. Supported: pdf, docx, doc, txt"
        )

    file_bytes = await file.read()
    if len(file_bytes) > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File too large. Max size: 10MB")

    try:
        result = await parser.parse(file_bytes, ext, file.filename)
        return {"success": True, "filename": file.filename, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "groq_configured": bool(os.getenv("GROQ_API_KEY")),
        "frontend_found": str(FRONTEND_HTML),
    }