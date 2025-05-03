from flask import Flask

def create_app():
    app = Flask(__name__)
    from .routes import chatbot
    app.register_blueprint(chatbot)
    return app
