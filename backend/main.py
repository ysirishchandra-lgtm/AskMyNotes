from fastapi import FastAPI

app = FastAPI(
    title="AskMyNotes Classifier API",
    version="1.0.0"
)

@app.get("/")
def home():
    return {"message": "Welcome to the AskMyNotes Classifier API"}

@app.get("/status")
def status():
    return {"status": "ok"}
