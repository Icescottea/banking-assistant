import json
import joblib

# Load trained model
model = joblib.load("models/intent_model.pkl")

# Load test cases
with open("chatbot_test_cases.json", "r", encoding="utf-8") as f:
    test_cases = json.load(f)

# Evaluation
results = []
correct = 0
total_confidence = 0

for test in test_cases:
    user_input = test["user_input"]
    expected = test["expected_intent"]

    probs = model.predict_proba([user_input])[0]
    pred_index = probs.argmax()
    confidence = probs[pred_index]
    predicted = model.classes_[pred_index]

    total_confidence += confidence
    passed = predicted == expected
    if passed:
        correct += 1

    results.append({
        "input": user_input,
        "expected": expected,
        "predicted": predicted,
        "confidence": round(float(confidence), 2),
        "result": "PASS" if passed else "FAIL"
    })

# Summary
average_confidence = total_confidence / len(test_cases)
summary = {
    "total": len(test_cases),
    "passed": correct,
    "failed": len(test_cases) - correct,
    "accuracy": round(correct / len(test_cases) * 100, 2),
    "average_confidence": round(average_confidence, 2)
}

# Output results
print(json.dumps(summary, indent=2))
print()
for r in results:
    print(f"[{r['result']}] {r['input']} → {r['predicted']} (Expected: {r['expected']}, Confidence: {r['confidence']})")
