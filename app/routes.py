import csv
import json, os
from datetime import datetime
from flask import Blueprint, render_template, request, jsonify
from engine.inference_engine import match_intent

chatbot = Blueprint("chatbot", __name__)

@chatbot.route("/")
def index():
    return render_template("chat.html")

@chatbot.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "")
    intent, response = match_intent(user_input)

    with open("logs/feedback.csv", "a", newline='', encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([datetime.now(), user_input, intent, response])

    return jsonify({"response": response})

@chatbot.route("/feedback", methods=["POST"])
def feedback_route():
    from datetime import datetime
    import os, json

    data = request.get_json()

    if not data or "message" not in data or "feedback" not in data:
        return jsonify({"error": "Invalid payload"}), 400

    feedback_entry = {
        "message": data["message"],
        "feedback": data["feedback"],
        "timestamp": datetime.utcnow().isoformat()
    }

    log_path = os.path.join(os.getcwd(), "logs", "feedback_log.jsonl")

    try:
        os.makedirs(os.path.dirname(log_path), exist_ok=True)

        with open(log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(feedback_entry) + "\n")

        print("✅ Logged feedback:", feedback_entry)
        return jsonify({"status": "logged"})
    
    except Exception as e:
        print("❌ Failed to log feedback:", e)
        return jsonify({"error": "Could not log feedback"}), 500

