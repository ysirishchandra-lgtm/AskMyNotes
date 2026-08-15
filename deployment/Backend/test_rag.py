import time
import requests
import os

pdf_content = b"%PDF-1.4\n1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R /Resources << /Font << /F1 << /Type /Font /Subtype /Type1 /BaseFont /Helvetica >> >> >> >>\nendobj\n4 0 obj\n<< /Length 53 >>\nstream\nBT /F1 24 Tf 100 700 Td (The secret is 42.) Tj ET\nendstream\nendobj\nxref\n0 5\n0000000000 65535 f \n0000000009 00000 n \n0000000058 00000 n \n0000000115 00000 n \n0000000288 00000 n \ntrailer\n<< /Size 5 /Root 1 0 R >>\nstartxref\n390\n%%EOF"

pdf_path = "test_document.pdf"
with open(pdf_path, "wb") as f:
    f.write(pdf_content)

url_base = "http://127.0.0.1:8000"

print("Waiting for backend server to become available (it is downloading AI models in the background)...")
for _ in range(60): # wait up to 5 minutes
    try:
        res = requests.get(f"{url_base}/status", timeout=2)
        if res.status_code == 200:
            print("Backend server is fully loaded and online!")
            break
    except requests.exceptions.ConnectionError:
        pass
    time.sleep(5)
else:
    print("Backend server did not start in time. It might still be downloading models.")
    exit(1)

print("\n--- Test 1: Upload PDF ---")
with open(pdf_path, 'rb') as f:
    res = requests.post(f"{url_base}/upload", files={"file": f})
print("Upload response:", res.json())

print("\n--- Test 2: Ask Question ---")
print("Question: What is the secret?")
res = requests.post(f"{url_base}/ask", json={"question": "What is the secret?"})
print("Ask response:", res.json())
