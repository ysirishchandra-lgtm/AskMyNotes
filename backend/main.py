from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import time
import asyncio

from fastapi.staticfiles import StaticFiles
import os

app = FastAPI()

# Allow frontend to make requests to this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, this should be restricted
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SignupRequest(BaseModel):
    fullName: str
    email: str
    password: str

@app.post("/api/signup")
async def signup(request: SignupRequest):
    # Mock registration process
    # In a real app, save to database and hash password
    print(f"User signed up: {request.email} - {request.fullName}")
    return {"message": "Sign Up successful!", "user": {"email": request.email, "name": request.fullName}}

@app.post("/api/ask")
async def ask_question(
    question: str = Form(...),
    notes: UploadFile = File(None)
):
    # Mock the answering process
    # In a real app, this would process the uploaded file, extract text, 
    # and send it to an LLM (e.g., Gemini/OpenAI) along with the question
    print(f"Received question: {question}")
    if notes:
        print(f"Received file: {notes.filename}")
        
    # Simulate some processing delay
    await asyncio.sleep(1.2)
    
    mock_answer = f"Based on my analysis, here is the information regarding: '{question}'."
    if notes:
        mock_answer += f" I found relevant details in your uploaded document: '{notes.filename}'."

    return {"answer": mock_answer}

# Serve the static files from the Frontend directory
frontend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Frontend")
app.mount("/", StaticFiles(directory=frontend_path, html=True), name="static")
