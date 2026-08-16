# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the Backend and Frontend directories into the container
COPY Backend /app/Backend
COPY Frontend /app/Frontend

# Install any needed packages specified in requirements.txt
WORKDIR /app/Backend
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable for Render compatibility
ENV PORT=8000

# Run uvicorn to serve the FastAPI app
# We use sh -c to ensure the PORT environment variable from Render is picked up properly
CMD ["sh", "-c", "uvicorn app:app --host 0.0.0.0 --port ${PORT:-8000}"]
