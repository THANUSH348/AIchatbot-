from flask import Flask
from pymongo import MongoClient
from app.config import Config
from flask_jwt_extended import JWTManager
from flask_cors import CORS 

# Initialize MongoDB client
client = MongoClient(Config.MONGO_URI)
db = client[Config.DATABASE_NAME]

jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)
    jwt.init_app(app)

    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.chat import chat_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(chat_bp)

    return app