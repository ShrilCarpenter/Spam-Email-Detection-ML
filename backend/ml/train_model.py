"""
Machine Learning Training Pipeline for Email Spam Detection System.

This script trains a real end-to-end TF-IDF + Logistic Regression pipeline
on the labeled spam/ham dataset using stratified splitting, zero data leakage,
and rigorous evaluation.

The serialized pipeline and verified evaluation metrics are saved for production serving.
"""

import os
import json
import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)

def get_paths():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    backend_dir = os.path.dirname(base_dir)
    dataset_path = os.path.join(backend_dir, "dataset", "mail_data.csv")
    ml_dir = base_dir
    models_dir = os.path.join(backend_dir, "models")
    return dataset_path, ml_dir, models_dir

def train_and_evaluate():
    dataset_path, ml_dir, models_dir = get_paths()
    os.makedirs(ml_dir, exist_ok=True)
    os.makedirs(models_dir, exist_ok=True)

    if not os.path.exists(dataset_path):
        raise FileNotFoundError(f"Dataset file not found at: {dataset_path}")

    print("==================================================")
    print("      SPAMSHIELD ML PIPELINE TRAINING ENGINE      ")
    print("==================================================")
    print(f"Loading dataset from: {dataset_path}")

    # 1. Load CSV dataset
    df = pd.read_csv(dataset_path)

    # 2. Normalize column names
    df.columns = [col.strip().lower() for col in df.columns]

    # 3. Identify message and category columns
    if "category" in df.columns and "message" in df.columns:
        cat_col, msg_col = "category", "message"
    elif "v1" in df.columns and "v2" in df.columns:
        cat_col, msg_col = "v1", "v2"
        df = df.rename(columns={"v1": "category", "v2": "message"})
    else:
        raise ValueError(
            f"Dataset must contain 'category'/'message' or 'v1'/'v2' columns. Found: {list(df.columns)}"
        )

    # 4. Clean data
    df["message"] = df["message"].fillna("").astype(str).str.strip()
    df["category"] = df["category"].astype(str).str.strip().str.lower()

    # Filter out empty messages
    df = df[df["message"].str.len() > 0]

    # Map labels: ham -> 0, spam -> 1
    label_map = {"ham": 0, "spam": 1}
    df["label"] = df["category"].map(label_map)
    df = df.dropna(subset=["label"])
    df["label"] = df["label"].astype(int)

    X = df["message"]
    y = df["label"]

    total_samples = len(df)
    spam_count = int(y.sum())
    ham_count = total_samples - spam_count

    print(f"\nDataset Statistics:")
    print(f" - Total Samples     : {total_samples}")
    print(f" - Ham (Legitimate)  : {ham_count} ({ham_count / total_samples * 100:.1f}%)")
    print(f" - Spam (Unwanted)   : {spam_count} ({spam_count / total_samples * 100:.1f}%)")

    # 5. Stratified 80/20 train/test split to prevent data leakage
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )

    print(f"\nData Split:")
    print(f" - Training Samples : {len(X_train)}")
    print(f" - Testing Samples  : {len(X_test)}")

    # 6. Build unified Pipeline containing Vectorizer + Classifier
    # Using TF-IDF with n-grams (1, 2) and Logistic Regression with lbfgs solver
    pipeline = Pipeline([
        ("tfidf", TfidfVectorizer(
            lowercase=True,
            stop_words="english",
            ngram_range=(1, 2),
            max_features=6000,
            sublinear_tf=True
        )),
        ("classifier", LogisticRegression(
            C=1.0,
            max_iter=1000,
            solver="lbfgs",
            random_state=42
        ))
    ])

    # 7. Fit pipeline exclusively on training data
    print("\nFitting TF-IDF Vectorizer and Logistic Regression on training set...")
    pipeline.fit(X_train, y_train)

    # 8. Evaluate on unseen test set
    print("Evaluating model on unseen test set...")
    y_pred = pipeline.predict(X_test)
    y_prob = pipeline.predict_proba(X_test)[:, 1]

    acc = float(accuracy_score(y_test, y_pred))
    prec = float(precision_score(y_test, y_pred, zero_division=0))
    rec = float(recall_score(y_test, y_pred, zero_division=0))
    f1 = float(f1_score(y_test, y_pred, zero_division=0))
    cm = confusion_matrix(y_test, y_pred).tolist()

    tn, fp, fn, tp = cm[0][0], cm[0][1], cm[1][0], cm[1][1]

    print("\n==================================================")
    print("             MODEL EVALUATION REPORT              ")
    print("==================================================")
    print(f"Accuracy  : {acc * 100:.2f}%")
    print(f"Precision : {prec * 100:.2f}%  (Minimizes false positives / legitimate flagged as spam)")
    print(f"Recall    : {rec * 100:.2f}%  (Captures high percentage of spam)")
    print(f"F1-Score  : {f1 * 100:.2f}%")
    print("\nConfusion Matrix:")
    print(f"                Predicted Legitimate    Predicted Spam")
    print(f"Actual Ham  :   {tn:<23} {fp:<15}")
    print(f"Actual Spam :   {fn:<23} {tp:<15}")
    print("\nDetailed Classification Report:")
    print(classification_report(y_test, y_pred, target_names=["Legitimate (Ham)", "Spam"]))

    # 9. Prepare metrics payload
    metrics_data = {
        "model_type": "TF-IDF + Logistic Regression Pipeline",
        "dataset_name": "Email & SMS Spam Collection Dataset",
        "total_samples": total_samples,
        "ham_samples": ham_count,
        "spam_samples": spam_count,
        "train_samples": len(X_train),
        "test_samples": len(X_test),
        "metrics": {
            "accuracy": round(acc * 100, 2),
            "precision": round(prec * 100, 2),
            "recall": round(rec * 100, 2),
            "f1_score": round(f1 * 100, 2),
            "true_negatives": tn,
            "false_positives": fp,
            "false_negatives": fn,
            "true_positives": tp
        },
        "pipeline_config": {
            "ngram_range": [1, 2],
            "max_features": 6000,
            "sublinear_tf": True,
            "classifier": "LogisticRegression(C=1.0, max_iter=1000, solver='lbfgs')"
        }
    }

    # 10. Save pipeline and metrics in both backend/ml and backend/models
    save_locations = [
        (os.path.join(ml_dir, "spam_classifier.pkl"), os.path.join(ml_dir, "model_metrics.json")),
        (os.path.join(models_dir, "spam_classifier.pkl"), os.path.join(models_dir, "model_metrics.json"))
    ]

    for model_path, json_path in save_locations:
        joblib.dump(pipeline, model_path)
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(metrics_data, f, indent=2)

    print("==================================================")
    print("Artifacts successfully saved:")
    print(f" - Model Artifacts   : {os.path.join(ml_dir, 'spam_classifier.pkl')}")
    print(f" - Evaluation Metrics: {os.path.join(ml_dir, 'model_metrics.json')}")
    print("==================================================\n")

    return metrics_data

if __name__ == "__main__":
    train_and_evaluate()
