import json
import joblib
from sentence_transformers import SentenceTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

# Load data
with open("data/training_data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

texts = [item["text"] for item in data]
labels = [item["intent"] for item in data]

# Encode labels
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(labels)

# Create sentence embeddings
model = SentenceTransformer('all-MiniLM-L6-v2')
X = model.encode(texts)

# Train classifier
classifier = LogisticRegression(max_iter=1000)
classifier.fit(X, y)

# Save model components
joblib.dump({
    "embedder": model,
    "classifier": classifier,
    "label_encoder": label_encoder
}, "models/transformer_intent_model.pkl")

print("✅ Transformer-based model trained and saved.")
