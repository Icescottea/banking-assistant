import json
import joblib
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

# Load training data
TRAINING_FILE = "data/training_data.json"
MODEL_OUTPUT_PATH = "models/intent_model.pkl"

if not os.path.exists(TRAINING_FILE):
    raise FileNotFoundError(f"Training data not found at: {TRAINING_FILE}")

with open(TRAINING_FILE, "r", encoding="utf-8") as f:
    samples = json.load(f)

texts = [sample["text"] for sample in samples]
labels = [sample["intent"] for sample in samples]

if not texts or not labels:
    raise ValueError("No training data found. Make sure training_data.json has valid entries.")

# Create ML pipeline
pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(ngram_range=(1, 2), stop_words='english')),
    ('clf', LogisticRegression(max_iter=1000))  # Prevent convergence warnings
])

# Train model
pipeline.fit(texts, labels)

# Save model
os.makedirs(os.path.dirname(MODEL_OUTPUT_PATH), exist_ok=True)
joblib.dump(pipeline, MODEL_OUTPUT_PATH)

print("Intent model trained and saved to:", MODEL_OUTPUT_PATH)
