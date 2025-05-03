import csv
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
import joblib

# Load original training data
with open("data/training_data.json", "r", encoding="utf-8") as f:
    training_data = json.load(f)

# Add new labeled examples (manually or pre-labeled)
with open("logs/feedback.csv", "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    for row in reader:
        if len(row) == 4:
            _, user_input, intent, _ = row
            training_data.append({"intent": intent, "text": user_input})

# Save back to training_data.json
with open("data/training_data.json", "w", encoding="utf-8") as f:
    json.dump(training_data, f, indent=2)

# Train updated model
texts = [item["text"] for item in training_data]
labels = [item["intent"] for item in training_data]

pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(ngram_range=(1, 2), stop_words='english')),
    ('clf', LogisticRegression())
])

pipeline.fit(texts, labels)
joblib.dump(pipeline, "models/intent_model.pkl")
print("✅ Model retrained with feedback + saved.")
