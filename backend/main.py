from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pathlib import Path
import os

ROOT = Path(__file__).resolve().parent.parent
CONTEXT_IMAGES_DIR = ROOT / "context-images"

app = FastAPI(title="ContentCrew API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:8501", "http://127.0.0.1:8501"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class GenerateRequest(BaseModel):
    prompt: str

@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "contentcrew-api"}

@app.get("/context-images")
def list_context_images() -> dict[str, list[str]]:
    CONTEXT_IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    names = sorted(
        p.name
        for p in CONTEXT_IMAGES_DIR.iterdir()
        if p.is_file() and not p.name.startswith(".")
    )
    return {"images": names}

@app.post("/api/generate")
def generate_content(payload: GenerateRequest):
    if not payload.prompt.strip():
        raise HTTPException(status_code=400, status_detail="Prompt cannot be empty")
    
    # Yahan hum AI agent response simulate kar rahe hain (apni marzi ka model ya logic yahan connect kiya ja sakta hai)
    prompt_text = payload.prompt.strip()
    generated_output = (
        f"🤖 **ContentCrew AI Engine Output**\n\n"
        f"**Topic/Prompt:** {prompt_text}\n\n"
        f"1. **Introduction:** Exploring the dynamics of {prompt_text} in modern agentic workflows.\n"
        f"2. **Key Insights:** Automated pipelines ensure high-speed delivery, modular design, and robust execution.\n"
        f"3. **Conclusion:** ContentCrew successfully processed your request with full-stack synchronization!"
    )
    
    return {
        "status": "success",
        "prompt": prompt_text,
        "content": generated_output
    }
