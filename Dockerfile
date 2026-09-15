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
RUN python -c "import os; os.path.exists('models/classifier.pkl') or __import__('train').train_spam_model()"

EXPOSE 8000

# Run FastAPI server on 0.0.0.0:8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
