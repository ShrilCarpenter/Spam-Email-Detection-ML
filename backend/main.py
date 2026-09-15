import os
import json
import joblib
from contextlib import asynccontextmanager
from typing import Optional, Dict, Any
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, model_validator

# Global in-memory storage for loaded ML pipeline and metrics
ml_state = {
    "pipeline": None,
    "metrics": None
}

MAX_TEXT_LENGTH = 50000

def get_candidate_paths():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    candidates = [
        os.path.join(base_dir, "ml", "spam_classifier.pkl"),
        os.path.join(base_dir, "models", "spam_classifier.pkl"),
    ]
    metrics_candidates = [
        os.path.join(base_dir, "ml", "model_metrics.json"),
        os.path.join(base_dir, "models", "model_metrics.json"),
    ]
    return candidates, metrics_candidates

def load_ml_assets() -> bool:
    """Loads the trained ML pipeline and evaluation metrics into memory once."""
    model_candidates, metrics_candidates = get_candidate_paths()
    loaded_model = False

    for model_path in model_candidates:
        if os.path.exists(model_path):
            try:
                ml_state["pipeline"] = joblib.load(model_path)
                print(f"[INFO] Successfully loaded ML pipeline from: {model_path}")
                loaded_model = True
                break
            except Exception as e:
                print(f"[ERROR] Failed to load model from {model_path}: {e}")

    for metrics_path in metrics_candidates:
        if os.path.exists(metrics_path):
            try:
                with open(metrics_path, "r", encoding="utf-8") as f:
                    ml_state["metrics"] = json.load(f)
                print(f"[INFO] Successfully loaded metrics from: {metrics_path}")
                break
            except Exception as e:
                print(f"[ERROR] Failed to load metrics from {metrics_path}: {e}")

    return loaded_model

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Load ML model pipeline once
    load_ml_assets()
    yield
    # Shutdown: Clean up memory
    ml_state.clear()

app = FastAPI(
    title="SpamShield API",
    description="Production-grade Email Spam Detection API powered by TF-IDF and Logistic Regression.",
    version="2.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class EmailRequest(BaseModel):
    text: Optional[str] = Field(
        None,
        description="The email content to classify.",
        json_schema_extra={"example": "Exclusive offer: claim your free $1,000 gift card now!"}
    )
    message: Optional[str] = Field(
        None,
        description="Legacy field alias for email content."
    )

    @model_validator(mode="before")
    @classmethod
    def extract_and_validate_content(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data

        raw_content = data.get("text")
        if raw_content is None:
            raw_content = data.get("message")

        if raw_content is None or not str(raw_content).strip():
            raise ValueError("Please enter an email message.")

        trimmed = str(raw_content).strip()

        if len(trimmed) > MAX_TEXT_LENGTH:
            raise ValueError(f"Email content exceeds maximum allowed length of {MAX_TEXT_LENGTH} characters.")

        data["text"] = trimmed
        data["message"] = trimmed
        return data

class Probabilities(BaseModel):
    ham: float
    spam: float

class PredictionResponse(BaseModel):
    prediction: str
    label: str
    probability: float
    is_spam: bool
    confidence: float
    probabilities: Probabilities

class HealthResponse(BaseModel):
    status: str
    model_loaded: bool

@app.get("/api/health", response_model=HealthResponse)
@app.get("/health", response_model=HealthResponse)
def health_check():
    """Health check endpoint to verify API and model status."""
    is_loaded = ml_state.get("pipeline") is not None
    if not is_loaded:
        is_loaded = load_ml_assets()

    return {
        "status": "ok" if is_loaded else "degraded",
        "model_loaded": is_loaded
    }

@app.get("/api/metrics")
@app.get("/metrics")
def get_model_metrics() -> Dict[str, Any]:
    """Returns actual verified evaluation metrics from the trained ML pipeline."""
    metrics = ml_state.get("metrics")
    if metrics is None:
        load_ml_assets()
        metrics = ml_state.get("metrics")

    if metrics is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Evaluation metrics are not currently available."
        )

    return metrics

@app.post("/api/predict", response_model=PredictionResponse)
@app.post("/predict", response_model=PredictionResponse)
def predict_spam(request: EmailRequest):
    """
    Predict whether an email message is SPAM or NOT SPAM.
    Processes the email in memory; content is never stored.
    """
    pipeline = ml_state.get("pipeline")

    if pipeline is None:
        if not load_ml_assets():
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Spam detection model is not available. Please ensure model training has been completed."
            )
        pipeline = ml_state.get("pipeline")

    content = request.text or request.message

    try:
        # Run prediction through the unified pipeline
        pred_class = int(pipeline.predict([content])[0])
        prob_distribution = pipeline.predict_proba([content])[0]

        # Class 0: Ham (Legitimate), Class 1: Spam
        ham_prob = float(prob_distribution[0])
        spam_prob = float(prob_distribution[1])

        is_spam = bool(pred_class == 1)
        selected_probability = spam_prob if is_spam else ham_prob

        return {
            "prediction": "spam" if is_spam else "ham",
            "label": "SPAM" if is_spam else "NOT SPAM",
            "probability": round(selected_probability, 4),
            "is_spam": is_spam,
            "confidence": round(selected_probability * 100, 2),
            "probabilities": {
                "ham": round(ham_prob * 100, 2),
                "spam": round(spam_prob * 100, 2)
            }
        }
    except Exception:
        # Safe error handling: never leak stack trace to caller
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong while analyzing the email."
        )
