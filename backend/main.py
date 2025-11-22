import os
import uuid
from typing import Dict, List

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import Response
from pydantic import BaseModel
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# -------------------------------------------------------------
# ⭐ CREATE APP FIRST
# -------------------------------------------------------------
app = FastAPI(title="Interview Practice Partner - Free Groq API")

# -------------------------------------------------------------
# ⭐ ABSOLUTE CORS FIX (Windows + Live Server)
# -------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],              # allow all origins
    allow_methods=["*"],              # allow all HTTP methods
    allow_headers=["*"],              # allow all headers
)

# ⭐ Force CORS headers manually for browsers that ignore middleware
@app.middleware("http")
async def add_cors_headers(request: Request, call_next):
    response: Response = await call_next(request)
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "*"
    return response

# -------------------------------------------------------------
# MODELS
# -------------------------------------------------------------
class StartRequest(BaseModel):
    role: str
    level: str
    mode: str

class StartResponse(BaseModel):
    sessionId: str
    botMessage: str

class MessageRequest(BaseModel):
    sessionId: str
    userMessage: str

class MessageResponse(BaseModel):
    botMessage: str
    done: bool = False

class FinishRequest(BaseModel):
    sessionId: str

class FeedbackSummary(BaseModel):
    strengths: List[str]
    areasToImprove: List[str]
    tips: List[str]
    overallRating: float

class FeedbackResponse(BaseModel):
    botMessage: str
    summary: FeedbackSummary

# -------------------------------------------------------------
# MEMORY STORE
# -------------------------------------------------------------
SESSIONS: Dict[str, Dict] = {}

# -------------------------------------------------------------
# LLM LOGIC
# -------------------------------------------------------------
def call_llm(system_prompt, user_prompt):
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.7,
        max_tokens=500
    )
    return response.choices[0].message.content.strip()


INTERVIEWER_PROMPT = """
You are an AI interviewer. Ask one question at a time.
Keep questions natural and conversational.
"""

FEEDBACK_PROMPT = """
Give structured interview feedback with sections:
Strengths:
Areas to Improve:
Tips:
Rating: x.x
"""

# -------------------------------------------------------------
# HELPERS
# -------------------------------------------------------------
def build_interviewer_prompt(session, latest_answer):
    text = f"Role: {session['role']}\nExperience: {session['level']}\nMode: {session['mode']}\n"
    text += "Conversation:\n"
    for qa in session["qa"]:
        text += f"Q: {qa['question']}\nA: {qa['answer']}\n"
    text += f"\nLatest answer: {latest_answer}\n"
    text += "Ask the next question."
    return text

def format_transcript(session):
    text = ""
    for qa in session["qa"]:
        text += f"Q: {qa['question']}\nA: {qa['answer']}\n\n"
    return text

# -------------------------------------------------------------
# ENDPOINTS
# -------------------------------------------------------------
@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/start", response_model=StartResponse)
def start_interview(req: StartRequest):
    session_id = str(uuid.uuid4())
    SESSIONS[session_id] = {
        "role": req.role,
        "level": req.level,
        "mode": req.mode,
        "qa": [],
    }
    question = "Hi! Let's begin. Can you introduce yourself?"
    SESSIONS[session_id]["qa"].append({"question": question, "answer": ""})
    return StartResponse(sessionId=session_id, botMessage=question)

@app.post("/message", response_model=MessageResponse)
def send_message(req: MessageRequest):
    session = SESSIONS.get(req.sessionId)
    if not session:
        raise HTTPException(404, "Invalid session ID")

    session["qa"][-1]["answer"] = req.userMessage
    prompt = build_interviewer_prompt(session, req.userMessage)
    next_q = call_llm(INTERVIEWER_PROMPT, prompt)
    session["qa"].append({"question": next_q, "answer": ""})

    return MessageResponse(botMessage=next_q)

@app.post("/finish", response_model=FeedbackResponse)
def finish(req: FinishRequest):
    session = SESSIONS.get(req.sessionId)
    if not session:
        raise HTTPException(404, "Invalid session ID")

    # Build transcript for LLM
    transcript = format_transcript(session)

    full_prompt = f"""
You are a senior interview evaluator.

Analyze this interview transcript and generate feedback with this EXACT structure:

Strengths:
- point 1
- point 2
- point 3
- point 4

Areas to Improve:
- point 1
- point 2
- point 3
- point 4

Tips:
- point 1
- point 2
- point 3

Rating:
A number between 0 and 5. Only give the number.

Transcript:
{transcript}
"""

    feedback_text = call_llm("You are an expert interview evaluator.", full_prompt)

    strengths, areas, tips = [], [], []
    rating = 4.0  # default safe rating

    section = ""

    for line in feedback_text.splitlines():
        l = line.strip().lower()

        if l.startswith("strengths"):
            section = "s"
            continue
        if l.startswith("areas to improve"):
            section = "a"
            continue
        if l.startswith("tips"):
            section = "t"
            continue
        if l.startswith("rating"):
            import re
            match = re.search(r"(\d+(\.\d+)?)", l)
            if match:
                rating = float(match.group(1))
                if rating > 5:
                    rating = 5.0
                if rating < 0:
                    rating = 0.0
            continue

        if line.startswith("-"):
            point = line[1:].strip()
            if section == "s":
                strengths.append(point)
            elif section == "a":
                areas.append(point)
            elif section == "t":
                tips.append(point)

    # Ensure minimum 1 item per category
    if not strengths:
        strengths = ["Good communication", "Positive attitude"]
    if not areas:
        areas = ["Provide more detailed explanations", "Improve structure of answers"]
    if not tips:
        tips = ["Use STAR method", "Give examples from real projects"]

    summary = FeedbackSummary(
        strengths=strengths,
        areasToImprove=areas,
        tips=tips,
        overallRating=rating
    )

    return FeedbackResponse(
        botMessage="Here is your detailed professional interview feedback!",
        summary=summary
    )

