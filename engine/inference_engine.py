import sys
import types

# Monkeypatch to prevent unpickling error on missing 'sentence_transformers.model_card'
if 'sentence_transformers.model_card' not in sys.modules:
    dummy_module = types.ModuleType("sentence_transformers.model_card")
    dummy_module.ModelCard = type("ModelCard", (), {})
    sys.modules["sentence_transformers.model_card"] = dummy_module

import joblib
import json
from database.db_handler import (
    get_account_types, get_loan_products,
    get_fixed_deposits, get_credit_cards
)

# Load static responses
with open("data/intents.json", encoding="utf-8") as file:
    static_responses = json.load(file)

# Load trained model
model_bundle = joblib.load("models/transformer_intent_model.pkl")
embedder = model_bundle["embedder"]
classifier = model_bundle["classifier"]
label_encoder = model_bundle["label_encoder"]

# Session memory
session = {
    "last_intent": None,
    "last_topic": None
}

# Confidence thresholds
FALLBACK_THRESHOLD = 0.4
SOFT_FALLBACK_THRESHOLD = 0.3

def match_intent(user_input):
    user_input = user_input.strip().lower()

    # Encode and predict
    embedding = embedder.encode([user_input])
    probs = classifier.predict_proba(embedding)[0]
    pred_index = probs.argmax()
    confidence = probs[pred_index]
    predicted_intent = label_encoder.inverse_transform([pred_index])[0]

    print(f"[DEBUG] Intent: {predicted_intent} | Confidence: {confidence:.2f}")

    # --- Fallback handling ---
    if confidence < SOFT_FALLBACK_THRESHOLD:
        with open("logs/unknown_inputs.txt", "a", encoding="utf-8") as log:
            log.write(user_input + "\n")
        fallback_response = static_responses.get("fallback", {}).get(
            "response",
            "I'm sorry, I didn’t understand that. Could you rephrase?"
        )
        return "fallback", fallback_response

    if confidence < FALLBACK_THRESHOLD:
        return "fallback", f"Did you mean something about **{predicted_intent.replace('_', ' ')}**?"

    # Track session
    session["last_intent"] = predicted_intent
    session["last_topic"] = predicted_intent

    # --- Intent-specific logic ---
    if predicted_intent == "account_opening":
        accounts = list({(name, desc) for name, desc in get_account_types()})
        if not accounts:
            return predicted_intent, "We currently don’t have account types available."
        name, desc = accounts[0]
        return predicted_intent, f"You can open accounts like our {name} — {desc}. To apply, visit your nearest branch or register online."

    if predicted_intent == "loans":
        loans = list({(name, rate, desc) for name, rate, desc in get_loan_products()})
        if not loans:
            return predicted_intent, "We currently have no loan offers."
        name, rate, desc = loans[0]
        return predicted_intent, f"We offer loans like the {name} at {rate}% interest — {desc}. Apply online or at a branch."

    if predicted_intent == "investments":
        fds = list({(months, rate) for months, rate in get_fixed_deposits()})
        if not fds:
            return predicted_intent, "No fixed deposit options are currently available."
        months, rate = fds[0]
        return predicted_intent, f"You can invest in fixed deposits such as {months}-month terms at {rate}% interest. Visit a branch to apply."

    if predicted_intent == "cards":
        if any(word in user_input for word in ["fee", "fees", "charge", "cost"]):
            return predicted_intent, "Most credit cards have annual fees, but we also offer zero-fee options like our Student Card."
        if any(word in user_input for word in ["apply", "get", "credit card"]):
            return predicted_intent, "You can apply for a debit or credit card online or at any branch."
        return predicted_intent, "We offer a range of cards with various benefits like cashback and travel perks. Want help choosing one?"

    if predicted_intent == "offers":
        return predicted_intent, "We have seasonal cashback, discounts, and referral bonuses. Check our app or site for current deals."

    if predicted_intent == "branch_locator":
        return predicted_intent, "You can find your nearest branch or ATM using our locator tool on the website."

    if predicted_intent == "support":
        return predicted_intent, "You can contact support 24/7 via our hotline, live chat, or branch visit."

    if predicted_intent == "security":
        return predicted_intent, "We use multi-factor authentication and fraud detection. Always report suspicious activity immediately."

    if predicted_intent == "digital_banking":
        return predicted_intent, "You can access our digital banking via mobile app or web portal. Register using your customer ID."

    if predicted_intent == "regulatory":
        return predicted_intent, "We follow strict KYC and FATCA rules. Upload valid documents online or visit a branch for assistance."

    if predicted_intent == "feedback":
        return predicted_intent, "We value your feedback. Please leave a suggestion or review through our feedback form on the website."

    # --- Static fallback ---
    if predicted_intent in static_responses:
        return predicted_intent, static_responses[predicted_intent]["response"]

    return "fallback", "I'm not sure how to help with that yet. Please try rephrasing."
