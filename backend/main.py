from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from dotenv import load_dotenv

from database import init_db, save_generation, get_history, save_feedback
from prompts import build_prompt
from ai_service import generate_learning_content

BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR.parent / "frontend"
load_dotenv(BASE_DIR / ".env")

app = FastAPI(
    title="LearnSphere: GenAI Personalized Learning Assistant",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

class GenerateRequest(BaseModel):
    student_name: str = Field(min_length=1, max_length=80)
    course: str = Field(min_length=1, max_length=100)
    topic: str = Field(min_length=1, max_length=150)
    level: str = Field(default="Intermediate")
    mode: str = Field(default="study_plan")
    goal: str = Field(default="", max_length=300)
    study_time: str = Field(default="60", max_length=20)

class FeedbackRequest(BaseModel):
    generation_id: int
    rating: int = Field(ge=1, le=5)
    comment: str = Field(default="", max_length=500)

@app.on_event("startup")
def startup():
    init_db()

@app.get("/api/health")
def health():
    return {"status": "ok", "service": "LearnSphere"}

@app.post("/api/generate")
def generate(req: GenerateRequest):
    allowed_modes = {"study_plan", "explain", "quiz", "flashcards"}
    if req.mode not in allowed_modes:
        raise HTTPException(status_code=400, detail="Invalid learning mode.")

    try:
        prompt = build_prompt(req.model_dump())
        output = generate_learning_content(prompt)
        generation_id = save_generation(
            req.student_name, req.course, req.topic,
            req.level, req.mode, output
        )
        return {
            "success": True,
            "generation_id": generation_id,
            "mode": req.mode,
            "output": output
        }
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

@app.get("/api/history")
def history():
    return {"success": True, "items": get_history()}

@app.post("/api/feedback")
def feedback(req: FeedbackRequest):
    try:
        save_feedback(req.generation_id, req.rating, req.comment)
        return {"success": True, "message": "Feedback saved."}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

@app.get("/")
def home():
    return FileResponse(FRONTEND_DIR / "index.html")

@app.get("/{file_path:path}")
def frontend_files(file_path: str):
    target = FRONTEND_DIR / file_path
    if target.exists() and target.is_file():
        return FileResponse(target)
    return FileResponse(FRONTEND_DIR / "index.html")
