from flask import Blueprint, request, jsonify
from app.models.user import User
from flask_jwt_extended import create_access_token

auth_bp = Blueprint('auth', __name__)

#Handles user registration (signup)
@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    if User.find_user_by_email(email):
        return jsonify({"error": "User already exists"}), 400

    User.create_user(email, password)
    return jsonify({"message": "User created successfully"}), 201

#Handles user Login (Login)
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    user = User.find_user_by_email(email)
    if not user or not User.verify_password(user, password):
        return jsonify({"error": "Invalid credentials"}), 401

    # Create JWT token
    access_token = create_access_token(identity=str(user["_id"]))
    return jsonify({"message": "Login successful", "access_token": access_token}), 200
