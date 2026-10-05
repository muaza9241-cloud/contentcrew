from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import ollama

app = FastAPI(title="ContentCrew Backend", version="1.0")

# Enable CORS for frontend communication (Streamlit / Vite)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class GenerateRequest(BaseModel):
    prompt: str
    platform: str = "General"
    tone: str = "Professional"

@app.get("/")
def read_root():
    return {
        "status": "ok", 
        "message": "ContentCrew Backend is running successfully with Ollama!"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "backend": "online"}

@app.post("/api/generate")
def generate_content(req: GenerateRequest):
    try:
        # Constructing a structured prompt based on user inputs
        full_prompt = (
            f"Act as an expert content creator. Write a {req.tone.lower()} "
            f"content piece optimized for {req.platform} based on the following prompt:\n\n"
            f"{req.prompt}"
        )

        # Calling local Ollama model (llama3)
        response = ollama.chat(
            model='llama3',
            messages=[
                {
                    'role': 'system',
                    'content': 'You are ContentCrew AI, an advanced AI assistant specialized in marketing, coding, and content creation.'
                },
                {
                    'prompt': full_prompt,
                    'role': 'user',
                    'content': full_prompt,
                },
            ]
        )

        ai_content = response['message']['content']

        return {
            "status": "success",
            "platform": req.platform,
            "tone": req.tone,
            "generated_content": ai_content
        }

    except Exception as e:
        # Fallback error message if Ollama service isn't running
        raise HTTPException(
            status_code=500, 
            detail=f"Ollama generation failed. Make sure Ollama is running. Error: {str(e)}"
        )
