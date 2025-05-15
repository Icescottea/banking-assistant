import json
import os
from datetime import datetime
from pathlib import Path

# Constants
FEEDBACK_LOG = "logs/feedback_log.jsonl"
TRAINING_DATA = "data/training_data.json"
INTENT_MODEL = "models/transformer_intent_model.pkl"
TEMP_APPEND_FILE = "data/auto_training_append.json"

# Create directory if not exists
os.makedirs("data", exist_ok=True)
os.makedirs("logs", exist_ok=True)

# Step 1: Load feedback log
def load_feedback():
    if not os.path.exists(FEEDBACK_LOG):
        return []
    with open(FEEDBACK_LOG, "r", encoding="utf-8") as f:
        return [json.loads(line) for line in f]

# Step 2: Extract negative feedback

def extract_bad_feedback(feedbacks):
    return [f for f in feedbacks if f["feedback"] == "down"]

# Step 3: Ask user for corrected intent for each

def label_intents(bad_feedback):
    corrected = []
    for item in bad_feedback:
        print("\nMessage:", item["message"])
        intent = input("Enter correct intent for this message (or press Enter to skip): ").strip()
        if intent:
            corrected.append({"text": item["message"], "intent": intent})
    return corrected

# Step 4: Append to training data

def append_to_training_data(samples):
    if not samples:
        print("No new samples added.")
        return

    with open(TRAINING_DATA, "r", encoding="utf-8") as f:
        data = json.load(f)

    data.extend(samples)

    with open(TRAINING_DATA, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print(f"✅ Added {len(samples)} samples to training_data.json")

# Step 5: Retrain model

def retrain_model():
    print("\n🔄 Retraining model...")
    os.system("python models/train_transformer_model.py")

# === Run ===
if __name__ == "__main__":
    feedbacks = load_feedback()
    bad_feedback = extract_bad_feedback(feedbacks)

    print(f"\n📥 Total feedback entries: {len(feedbacks)}")
    print(f"👎 Thumbs-down messages: {len(bad_feedback)}")

    labeled_samples = label_intents(bad_feedback)
    append_to_training_data(labeled_samples)
    retrain_model()
