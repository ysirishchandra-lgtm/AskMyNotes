from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import time
import asyncio

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
    
    mock_answer = f"This is a mocked answer for the question: '{question}'. "
    if notes:
        mock_answer += f"I have read your notes file '{notes.filename}'."
    else:
        mock_answer += "You did not upload any notes."

    return {"answer": mock_answer}
