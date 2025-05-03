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

    # Debugging line (optional)
    print(f"[DEBUG] Predicted: {predicted_intent}, Confidence: {confidence:.2f}")

    # Reject low confidence predictions
    if confidence < 0.3:
        with open("logs/unknown_inputs.txt", "a", encoding="utf-8") as log:
            log.write(user_input + "\n")
        return "unknown", "Hmm, I didn’t quite get that. Could you say it another way?"

    # Save to session after confidence confirmed
    session["last_intent"] = predicted_intent
    if predicted_intent in ["loan_products", "account_types", "fixed_deposits", "credit_cards"]:
        session["last_topic"] = predicted_intent

    # Respond with static responses
    if predicted_intent in static_responses:
        return predicted_intent, static_responses[predicted_intent]["response"]

    # Respond dynamically
    if predicted_intent == "account_types":
        types = get_account_types()
        response = "We offer the following account types:\n"
        for name, desc in types:
            response += f"- {name}: {desc}\n"
        return predicted_intent, response

    if predicted_intent == "loan_products":
        loans = get_loan_products()
        response = "Here are our loan products:\n"
        for name, rate, desc in loans:
            response += f"- {name} (Interest: {rate}%) - {desc}\n"
        return predicted_intent, response

    if predicted_intent == "fixed_deposits":
        fds = get_fixed_deposits()
        response = "Here are our Fixed Deposit options:\n"
        for duration, rate in fds:
            response += f"- {duration} months at {rate}% interest\n"
        return predicted_intent, response

    if predicted_intent == "credit_cards":
        cards = get_credit_cards()
        response = "Our credit cards include:\n"
        for name, fee, benefits in cards:
            response += f"- {name} (Fee: Rs. {fee}) - {benefits}\n"
        return predicted_intent, response

    # Fallback to context-aware follow-up
    if "rate" in user_input or "interest" in user_input:
        if session["last_topic"] == "loan_products":
            loans = get_loan_products()
            response = "Here are the current interest rates on our loans:\n"
            for name, rate, _ in loans:
                response += f"- {name}: {rate}%\n"
            return "loan_rate_followup", response

        elif session["last_topic"] == "fixed_deposits":
            fds = get_fixed_deposits()
            response = "Here are our FD interest rates:\n"
            for months, rate in fds:
                response += f"- {months} months: {rate}%\n"
            return "fd_rate_followup", response

    return "unknown", "I'm not sure how to help with that yet. Could you try rephrasing?"
