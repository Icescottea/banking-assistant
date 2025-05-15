import json
import joblib
from sklearn.metrics import accuracy_score
from collections import defaultdict

# Load the trained transformer model bundle
model_bundle = joblib.load("models/transformer_intent_model.pkl")
embedder = model_bundle["embedder"]
classifier = model_bundle["classifier"]
label_encoder = model_bundle["label_encoder"]

# Load test cases
with open("test_cases.json", "r", encoding="utf-8") as f:
    test_cases = json.load(f)

CONFIDENCE_THRESHOLD = 0.4

# Tracking
passed = 0
failed = 0
confidence_scores = []
intent_stats = defaultdict(lambda: {"total": 0, "correct": 0})

# Test loop
print("\n=== Test Results ===")
for case in test_cases:
    user_input = case["user_input"].strip().lower()
    expected_intent = case["expected_intent"]

    embedding = embedder.encode([user_input])
    probs = classifier.predict_proba(embedding)[0]
    pred_index = probs.argmax()
    confidence = probs[pred_index]
    predicted_intent = label_encoder.inverse_transform([pred_index])[0]

    confidence_scores.append(confidence)
    intent_stats[expected_intent]["total"] += 1

    if confidence < CONFIDENCE_THRESHOLD:
        predicted_intent = "fallback"

    if predicted_intent == expected_intent:
        passed += 1
        intent_stats[expected_intent]["correct"] += 1
        result = "✅ PASS"
    else:
        failed += 1
        result = "❌ FAIL"

    print(f"{result} | {case['id']:>20} | Predicted: {predicted_intent:>18} | Expected: {expected_intent:>18} | Confidence: {confidence:.2f}")

# Summary
print("\n📊 Summary")
print(f"✅ Passed: {passed}")
print(f"❌ Failed: {failed}")
print(f"🎯 Accuracy: {round((passed / len(test_cases)) * 100, 2)}%")
print(f"📈 Average Confidence: {round(sum(confidence_scores) / len(confidence_scores), 3)}")

# Per-intent accuracy
print("\n📌 Per-Intent Accuracy:")
for intent, stats in sorted(intent_stats.items()):
    total = stats["total"]
    correct = stats["correct"]
    accuracy = round((correct / total) * 100, 2) if total > 0 else 0.0
    print(f"- {intent:20} : {accuracy}% ({correct}/{total})")