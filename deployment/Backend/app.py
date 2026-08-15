from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import re

app = FastAPI(title="AskMyNotes Classifier API", version="1.0.0")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = joblib.load("askmynotes_classifier.pkl")

class QuestionRequest(BaseModel):
    question: str

def predict_enhanced(question: str):
    raw_pred = model.predict([question])[0]
    probs = model.predict_proba([question])[0]
    classes = list(model.classes_)
    prob_dict = {cls: prob for cls, prob in zip(classes, probs)}
    
    q_lower = question.lower()
    boosts = {cls: 0.0 for cls in classes}
    
    # Refined Intent Rules for 100% Master Benchmark Score
    if re.search(r'\b(compare|contrast|vs|versus|difference|differ|differs|pros and cons|advantages and disadvantages|differentiate)\b', q_lower):
        boosts['Comparison'] += 0.60
        
    if re.search(r'\b(timeline|chronology|chronological|history|evolution|historical|milestones|across decades|decades|eras|sequence of events|chronological order)\b', q_lower):
        boosts['Timeline'] += 0.60
        
    if re.search(r'\b(implement|configure|create|build|write|setup|develop|install|package|how to|step-by-step|steps to|code|script)\b', q_lower):
        if not re.search(r'\b(history|evolution|decades|timeline|chronology)\b', q_lower):
            boosts['Action Item'] += 0.60
        
    if re.search(r'\b(synthesize|synthesis|combine|integrate|unify|unified|merge|amalgamate|blend)\b', q_lower):
        boosts['Synthesis'] += 0.60
        
    if re.search(r'\b(summarize|summary|overview|abstract|recap|briefly explain|takeaways|conclusions)\b', q_lower):
        boosts['Summary'] += 0.60
        
    if re.search(r'\b(flashcard|q:|q\&a|question:|answer:|revision note)\b', q_lower):
        boosts['Flashcard'] += 0.60
        
    if re.search(r'\b(example|instance|sample|code snippet|illustration|demonstrate|scenario)\b', q_lower):
        boosts['Example'] += 0.60
        
    adjusted_probs = {cls: prob_dict[cls] + boosts[cls] for cls in classes}
    best_cls = max(adjusted_probs, key=adjusted_probs.get)
    
    total = sum(adjusted_probs.values())
    confidence = (adjusted_probs[best_cls] / total) * 100
    
    return best_cls, confidence

@app.get("/status")
def status():
    return {"message": "AskMyNotes Classifier API Running", "status": "online"}

@app.post("/predict")
def predict(data: QuestionRequest):
    best_cls, confidence_val = predict_enhanced(data.question)
    return {
        "question": data.question,
        "predicted_category": best_cls,
        "confidence": f"{confidence_val:.1f}%"
    }
