FROM python:3.12-slim

WORKDIR /app

# Copy the entire deployment folder (both Backend and Frontend)
COPY . /app

# Install backend dependencies
WORKDIR /app/Backend
RUN pip install --no-cache-dir -r requirements.txt

# Run the app
CMD uvicorn app:app --host 0.0.0.0 --port ${PORT:-7860}
