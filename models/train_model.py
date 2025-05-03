import json
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

# Load training data
with open("data/training_data.json") as f:
    samples = json.load(f)

texts = [sample["text"] for sample in samples]
labels = [sample["intent"] for sample in samples]

# Create ML pipeline
pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(ngram_range=(1, 2), stop_words='english')),
    ('clf', LogisticRegression())
])

# Train model
pipeline.fit(texts, labels)

# Save model
joblib.dump(pipeline, "models/intent_model.pkl")
print("✅ Intent model trained and saved.")
