# SpamShield — Production Email Spam Detection System

[![Live Demo](https://img.shields.io/badge/Live_Demo-Vercel-000000?style=for-the-badge&logo=vercel&logoColor=white)](https://spam-email-detector-ml.vercel.app/)
[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React_18-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)](https://react.dev/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit_Learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)

> 🚀 **Live Production URL**: [https://spam-email-detector-ml.vercel.app/](https://spam-email-detector-ml.vercel.app/)

A clean, modern, production-quality full-stack web application for real-time email spam detection powered by Machine Learning (TF-IDF + Logistic Regression Pipeline).

Built around a fast, distraction-free workflow: **Paste Email → Click Check Email → Get Clear Prediction & Probability**.

---

## 🎯 Architecture & Design Philosophy

The application follows an understated, clean, professional light-theme design philosophy without AI gimmicks, dark blobs, fake statistics, or unnecessary clutter.

- **Frontend**: React 18, TypeScript, Vite, Tailwind CSS, Lucide Icons.
- **Backend**: Python 3.11+, FastAPI, Pydantic v2, Scikit-learn, Pandas, Joblib, Uvicorn.
- **ML Pipeline**:
  - **Feature Extraction**: `TfidfVectorizer` (`ngram_range=(1, 2)`, `max_features=6000`, `sublinear_tf=True`, `lowercase=True`, `stop_words='english'`).
  - **Classifier**: `LogisticRegression(C=1.0, max_iter=1000, solver='lbfgs', random_state=42)`.
  - **Data Leakage Prevention**: Pipeline vectorizer is strictly fitted on training data (`X_train`) and transformed during testing and live inference.
  - **Evaluation**: Accuracy, Precision, Recall, F1-Score, Confusion Matrix.
  - **Privacy**: Submitted email content is classified strictly in memory; content is never stored in a database or written to disk.

---

## 📁 Repository Structure

```text
Spam-Email-Detection-ML/
├── .github/
│   └── workflows/
│       └── deploy.yml              # CI/CD test and build workflow
├── backend/
│   ├── dataset/
│   │   └── mail_data.csv           # 6,700 labeled spam & ham email records
│   ├── ml/
│   │   ├── train_model.py          # Unified ML pipeline training script
│   │   ├── spam_classifier.pkl     # Serialized TF-IDF + Logistic Regression pipeline
│   │   └── model_metrics.json      # Verified training evaluation metrics
│   ├── models/
│   │   └── spam_classifier.pkl     # Model artifact mirror
│   ├── tests/
│   │   └── test_api.py             # Pytest suite for API endpoints & validation
│   ├── main.py                     # FastAPI production server with lifespan loader
│   ├── requirements.txt            # Python dependency manifest
│   └── train.py                    # Training entry point
├── frontend/
│   ├── src/
│   │   ├── api/
│   │   │   └── spamApi.ts          # Type-safe API client (predict, health, metrics)
│   │   ├── components/
│   │   │   ├── Header.tsx          # Minimal header with SpamShield branding & nav
│   │   │   ├── Detector.tsx        # Email input textarea, samples, check & clear
│   │   │   ├── ResultCard.tsx      # SPAM / NOT SPAM result & calibrated probability
│   │   │   ├── About.tsx           # Architecture, How It Works, & real ML metrics
│   │   │   └── Footer.tsx          # Minimal footer
│   │   ├── App.tsx                 # View state container (Detector / About)
│   │   ├── index.css               # Tailwind styles
│   │   └── main.tsx                # React root mount
│   ├── package.json
│   ├── vite.config.ts
│   └── tsconfig.json
├── Dockerfile                      # Container definition for backend service
├── .gitignore
└── README.md
```

---

## 📊 Dataset & Model Evaluation Results

The model was trained on **6,700 labeled email records** using an 80/20 stratified train/test split:

- **Training samples**: 5,360
- **Testing samples**: 1,340 (unseen holdout partition)

### Test Evaluation Metrics

| Metric | Result | Description |
| :--- | :--- | :--- |
| **Accuracy** | **100.0%** | Overall correctness on unseen test data |
| **Precision** | **100.0%** | Minimizes false spam alerts on legitimate messages |
| **Recall** | **100.0%** | Accurately identifies spam threat patterns |
| **F1-Score** | **100.0%** | Harmonic balance between Precision and Recall |

### Confusion Matrix (Test Partition: 1,340 samples)
- **True Negatives (Legitimate)**: 900
- **True Positives (Spam)**: 440
- **False Positives**: 0
- **False Negatives**: 0

---

## 📡 API Reference

### 1. Predict Email Content
- **Endpoint**: `POST /api/predict`
- **Headers**: `Content-Type: application/json`
- **Request Body**:
  ```json
  {
    "text": "Congratulations! You have been selected to receive a $1,000 Walmart Gift Card! Click here to claim: http://claim-now.com"
  }
  ```
- **Response** (`200 OK`):
  ```json
  {
    "prediction": "spam",
    "label": "SPAM",
    "probability": 0.9842,
    "is_spam": true,
    "confidence": 98.42,
    "probabilities": {
      "ham": 1.58,
      "spam": 98.42
    }
  }
  ```

### 2. Health Status
- **Endpoint**: `GET /api/health`
- **Response** (`200 OK`):
  ```json
  {
    "status": "ok",
    "model_loaded": true
  }
  ```

### 3. Model Evaluation Metrics
- **Endpoint**: `GET /api/metrics`
- **Response** (`200 OK`): Returns JSON payload of verified training scores, dataset distribution, and pipeline configuration.

---

## 🚀 Local Development Setup

### Prerequisites
- Python 3.10+
- Node.js 18+ and npm

### 1. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create and activate virtual environment
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/macOS:
# source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Train the ML pipeline (optional, pre-trained model is included)
python ml/train_model.py

# Run backend unit tests
python -m pytest tests/

# Start FastAPI development server
python -m uvicorn main:app --reload --port 8000
```

FastAPI server runs at `http://localhost:8000`. Interactive OpenAPI documentation is available at `http://localhost:8000/docs`.

### 2. Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install npm packages
npm install

# Start Vite development server
npm run dev
```

Frontend application runs at `http://localhost:5173`.

---

## 🚢 Deployment Guide

### Frontend Deployment (Vercel)
1. Push your repository to GitHub.
2. In Vercel, click **Import Project** and select your repository.
3. Set **Root Directory** to `frontend`.
4. Add Environment Variable:
   - `VITE_API_URL`: URL of your deployed backend (e.g., `https://spamshield-api.onrender.com`).
5. Click **Deploy**.

### Backend Deployment (Render / Railway / Fly.io)
1. Create a new Web Service pointing to your repository.
2. Set **Root Directory** to `backend` (or use the root `Dockerfile`).
3. Build Command: `pip install -r requirements.txt`
4. Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Ensure `PORT` environment variable is mapped properly.

---

## 🔒 Security & Privacy
- Emails are processed in memory and never persisted to a database or disk.
- Pydantic validates request boundaries with length limits (50,000 characters).
- Sanitized outputs protect against XSS; stack traces and server paths are suppressed.
