import csv
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
def feedback():
    data = request.get_json()
    message = data.get("message", "")
    rating = data.get("feedback", "")

    with open("logs/thumbs_feedback.csv", "a", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([datetime.now(), message, rating])

    return jsonify({"status": "logged"})
