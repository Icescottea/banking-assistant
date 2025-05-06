import joblib
import json
from database.db_handler import (
    get_account_types, get_loan_products,
    get_fixed_deposits, get_credit_cards
)

# Load static responses
with open("data/intents.json") as file:
    static_responses = json.load(file)

# Load trained model
intent_model = joblib.load("models/intent_model.pkl")

# Session memory (to enable conversational memory later)
session = {
    "last_intent": None,
    "last_topic": None
}

def match_intent(user_input):
    user_input = user_input.lower().strip()

    # Predict intent and get confidence
    probs = intent_model.predict_proba([user_input])[0]
    pred_index = probs.argmax()
    confidence = probs[pred_index]
    predicted_intent = intent_model.classes_[pred_index]

    print(f"[DEBUG] Intent: {predicted_intent} | Confidence: {confidence:.2f}")

    if confidence < 0.1:
        with open("logs/unknown_inputs.txt", "a", encoding="utf-8") as log:
            log.write(user_input + "\n")
        return "unknown", "Hmm, I’m not sure I got that. Can you rephrase?"

    session["last_intent"] = predicted_intent
    session["last_topic"] = predicted_intent

    # --- Dynamic Responses ---

    if predicted_intent == "account_opening":
        accounts = get_account_types()
        response = "Here are the types of accounts you can open:\n"
        for name, desc in accounts:
            response += f"- {name}: {desc}\n"
        return predicted_intent, response

    if predicted_intent == "loans":
        loans = get_loan_products()
        response = "We offer the following loan products:\n"
        for name, rate, desc in loans:
            response += f"- {name} (Interest: {rate}%) - {desc}\n"
        return predicted_intent, response

    if predicted_intent == "investments":
        fds = get_fixed_deposits()
        response = "We offer the following fixed deposit options:\n"
        for months, rate in fds:
            response += f"- {months} months at {rate}% interest\n"
        return predicted_intent, response

    if predicted_intent == "cards":
        cards = get_credit_cards()
        response = "Here are our available cards:\n"
        for name, fee, benefits in cards:
            response += f"- {name} (Fee: Rs. {fee}) - {benefits}\n"
        return predicted_intent, response

    # --- Static fallback from intents.json ---
    if predicted_intent in static_responses:
        return predicted_intent, static_responses[predicted_intent]["response"]

    return "unknown", "I'm not sure how to help with that yet. Try rephrasing?"