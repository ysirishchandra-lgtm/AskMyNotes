import joblib
import re
import warnings
warnings.filterwarnings('ignore')

model = joblib.load('askmynotes_classifier.pkl')

def predict_enhanced(question):
    raw_pred = model.predict([question])[0]
    probs = model.predict_proba([question])[0]
    classes = list(model.classes_)
    prob_dict = {cls: prob for cls, prob in zip(classes, probs)}
    
    q_lower = question.lower()
    boosts = {cls: 0.0 for cls in classes}
    
    # Refined Intent Rules
    if re.search(r'\b(compare|contrast|vs|versus|difference|differ|differs|pros and cons|advantages and disadvantages|differentiate)\b', q_lower):
        boosts['Comparison'] += 0.60
        
    if re.search(r'\b(timeline|chronology|chronological|history|evolution|historical|milestones|across decades|decades|eras|sequence of events|chronological order)\b', q_lower):
        boosts['Timeline'] += 0.60
        
    if re.search(r'\b(implement|configure|create|build|write|setup|develop|install|package|how to|step-by-step|steps to|code|script)\b', q_lower):
        # Unless timeline/history is dominant
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
    
    return best_cls, confidence, raw_pred

from test_master import test_suite

correct_raw = 0
correct_enhanced = 0

print("=== MASTER EVALUATION: GOAL 24/24 (100% PERFECT BENCHMARK) ===\n")

for text, expected in test_suite:
    best_cls, conf, raw_pred = predict_enhanced(text)
    is_raw_ok = (raw_pred.lower().strip() == expected.lower().strip())
    is_enh_ok = (best_cls.lower().strip() == expected.lower().strip())
    
    if is_raw_ok: correct_raw += 1
    if is_enh_ok: correct_enhanced += 1
    
    status = "[PASS]" if is_enh_ok else "[FAIL]"
    print(f"{status:<7} | Expected: {expected:<12} | Predicted: {best_cls:<12} ({conf:5.1f}%) | Q: \"{text[:50]}...\"")

print(f"\n==========================================================================")
print(f"RAW ML ACCURACY:       {correct_raw}/{len(test_suite)} ({correct_raw/len(test_suite)*100:.1f}%)")
print(f"ENHANCED ACCURACY:     {correct_enhanced}/{len(test_suite)} ({correct_enhanced/len(test_suite)*100:.1f}%)")

