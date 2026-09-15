"""
SpamShield Training Gateway.
Delegates to backend.ml.train_model for end-to-end TF-IDF + Logistic Regression pipeline training.
"""
from ml.train_model import train_and_evaluate

if __name__ == "__main__":
    train_and_evaluate()

