# Production Dockerfile for Backend ML & API Service
FROM python:3.11-slim

WORKDIR /app

# Install system utilities
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY backend/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code, dataset and model artifacts
COPY backend /app

# Ensure model artifacts exist (run training if not present)
RUN python -c "import os; os.path.exists('ml/spam_classifier.pkl') or __import__('ml.train_model').train_and_evaluate()"

EXPOSE 8000

# Run FastAPI server on dynamic $PORT (defaulting to 8000)
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"]
