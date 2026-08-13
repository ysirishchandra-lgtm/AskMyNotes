import joblib
import warnings
warnings.filterwarnings('ignore')

model = joblib.load('askmynotes_classifier.pkl')

test_suite = [
    # Category: Comparison
    ('Contrast SQL relational databases with MongoDB document stores in terms of schema flexibility and ACID compliance', 'Comparison'),
    ('What are the main differences between supervised learning and unsupervised learning in AI?', 'Comparison'),
    ('Compare and contrast Mitosis and Meiosis cell division processes', 'Comparison'),
    ('How does REST API differ from GraphQL in terms of network overhead?', 'Comparison'),
    ('Evaluate the pros and cons of monolithic architecture vs microservices', 'Comparison'),
    
    # Category: Timeline
    ('Outline the chronological timeline of events leading up to World War 2 from 1918 to 1939', 'Timeline'),
    ('Provide a historical sequence of key milestones in the development of quantum mechanics', 'Timeline'),
    ('List the evolution steps of mobile cellular technology from 1G to 5G across decades', 'Timeline'),
    ('Detail the historical sequence of space exploration from Sputnik in 1957 to Apollo 11 in 1969', 'Timeline'),
    ('Trace the timeline of major architectural shifts in computing from vacuum tubes to transistors', 'Timeline'),
    
    # Category: Definition
    ('Define quantum entanglement and explain its physical significance in quantum computing', 'Definition'),
    ('What is the exact definition of Polymorphism in Object Oriented Programming?', 'Definition'),
    ('Explain the concept of Inflation in macroeconomics and how CPI measures it', 'Definition'),
    
    # Category: Action Item
    ('Implement a binary search tree in Python with insert and delete methods', 'Action Item'),
    ('Configure Nginx as a reverse proxy for a Node.js web server on Ubuntu', 'Action Item'),
    ('Create a Dockerfile to package a FastAPI service with multi-stage build', 'Action Item'),
    
    # Category: Summary
    ('Summarize the key takeaways and main conclusions of the research paper on transformer models', 'Summary'),
    ('Give a brief summary of the Industrial Revolution and its economic impacts', 'Summary'),
    
    # Category: Example
    ('Give a practical code example of a Singleton pattern implementation in Java', 'Example'),
    ('Provide an example scenario demonstrating the use of Bayes theorem in medical diagnosis', 'Example'),
    
    # Category: Flashcard
    ('Q: What is the capital of France? A: Paris. Flashcard Q&A for geography test', 'Flashcard'),
    ('Flashcard revision note: What is the speed of light in vacuum? 3 x 10^8 m/s', 'Flashcard'),
    
    # Category: Synthesis
    ('Synthesize findings from modern astrophysics and particle physics regarding dark matter candidates', 'Synthesis'),
    ('Combine theoretical economics and behavioral psychology into a unified model', 'Synthesis')
]

print(f"=== MASTER MODEL BENCHMARK TEST ({len(test_suite)} Hard Questions) ===\n")

correct = 0
results = []

for text, expected in test_suite:
    pred = model.predict([text])[0]
    probs = model.predict_proba([text])[0]
    conf = max(probs) * 100
    is_correct = (pred.lower().strip() == expected.lower().strip())
    if is_correct:
        correct += 1
    status = "PASS" if is_correct else "FAIL"
    results.append((status, expected, pred, conf, text))

for status, expected, pred, conf, text in results:
    icon = "[OK]" if status == "PASS" else "[FAIL]"
    print(f"{icon} | Expected: {expected:<12} | Predicted: {pred:<12} ({conf:5.1f}%) | Question: \"{text[:65]}...\"")

print(f"\n======================================================")
print(f"FINAL BENCHMARK SCORE: {correct}/{len(test_suite)} ({correct/len(test_suite)*100:.1f}%)")
