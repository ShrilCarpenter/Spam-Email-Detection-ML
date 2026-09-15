import pytest
from fastapi.testclient import TestClient
import sys
import os

# Add backend directory to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app, load_ml_assets

@pytest.fixture(scope="module", autouse=True)
def init_models():
    # Ensure artifacts are loaded for tests
    load_ml_assets()

@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client

def test_health_endpoints(client):
    for path in ["/api/health", "/health"]:
        response = client.get(path)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert data["model_loaded"] is True

def test_metrics_endpoints(client):
    for path in ["/api/metrics", "/metrics"]:
        response = client.get(path)
        assert response.status_code == 200
        data = response.json()
        assert "metrics" in data
        assert "accuracy" in data["metrics"]
        assert "precision" in data["metrics"]
        assert "recall" in data["metrics"]
        assert "f1_score" in data["metrics"]

def test_predict_spam_with_text_field(client):
    payload = {
        "text": "CONGRATULATIONS! You have won a $1,000 Walmart Gift Card! Click here to claim your prize now: http://claim-gift-now.com"
    }
    response = client.post("/api/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["prediction"] == "spam"
    assert data["label"] == "SPAM"
    assert data["is_spam"] is True
    assert data["probability"] > 0.5
    assert data["confidence"] > 50.0
    assert data["probabilities"]["spam"] > data["probabilities"]["ham"]

def test_predict_ham_with_text_field(client):
    payload = {
        "text": "Hi Sarah, could you please review the attached slide deck before our team sync meeting at 2 PM?"
    }
    response = client.post("/api/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["prediction"] == "ham"
    assert data["label"] == "NOT SPAM"
    assert data["is_spam"] is False
    assert data["confidence"] > 50.0
    assert data["probabilities"]["ham"] > data["probabilities"]["spam"]

def test_predict_with_legacy_message_field(client):
    payload = {
        "message": "URGENT: Your account has been temporarily locked. Verify your details immediately."
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["label"] == "SPAM"

def test_predict_empty_text(client):
    payload = {"text": ""}
    response = client.post("/api/predict", json=payload)
    assert response.status_code == 422

def test_predict_whitespace_text(client):
    payload = {"text": "   \n\t  "}
    response = client.post("/api/predict", json=payload)
    assert response.status_code == 422

def test_predict_missing_text(client):
    payload = {}
    response = client.post("/api/predict", json=payload)
    assert response.status_code == 422
