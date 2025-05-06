🏦 GolfWang Bank Chatbot – Project Overview

This project is a smart, machine learning-powered banking assistant built with Python and Flask. It provides a web-based chat interface that allows users to interact using natural language. The system uses a trained intent classifier, a relational database for dynamic information, and a simple feedback system to improve over time.
✅ Key Features

    Natural language understanding with machine learning (Logistic Regression + TF-IDF)

    Text-based chat UI built using Flask and HTML/CSS

    Real-time responses using static and dynamic knowledge (from SQLite)

    Context handling for follow-up questions (e.g., “what’s the interest rate?”)

    Thumbs-up/down feedback system to rate responses

    Logging unknown inputs and retraining pipeline for continuous improvement

📂 Folder Structure

- app/                → Flask routes and templates
- static/             → CSS files
- database/           → DB schema, seed data, and queries
- data/               → intents.json + training_data.json
- engine/             → inference engine with ML model
- models/             → training and retraining scripts
- logs/               → feedback and unknown input logs
- run.py              → Flask entry point
- requirements.txt

▶️ How to Run

    Install dependencies
    pip install -r requirements.txt

    Initialize DB and train model

    python database/seed_data.py  
    python models/train_model.py

    Run the app
    python run.py

    Access in browser
    http://127.0.0.1:5000/

🚀 Deployment

Push to GitHub → Deploy to Render.com
Set start command: gunicorn run:app