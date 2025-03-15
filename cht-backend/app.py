from flask import Flask, request, jsonify, session
from flask_cors import CORS
from pymongo import MongoClient
import hashlib
from bson.objectid import ObjectId

app = Flask(__name__)
CORS(app)

# MongoDB Configuration
client = MongoClient('mongodb://localhost:27017/')
db = client['chatbot']
users_collection = db['users']
chat_history_collection = db['chat_history']

app.config['SECRET_KEY'] = 'supersecretkey'

# Helper function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# User Registration
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data['username']
    password = hash_password(data['password'])

    # Check if user already exists
    if users_collection.find_one({'username': username}):
        return jsonify({"message": "Username already exists"}), 400

    # Insert new user
    user_id = users_collection.insert_one({'username': username, 'password': password}).inserted_id
    return jsonify({"message": "User registered successfully", "user_id": str(user_id)}), 201

# User Login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = hash_password(data['password'])

    # Find user in the database
    user = users_collection.find_one({'username': username, 'password': password})

    if user:
        session['user_id'] = str(user['_id'])
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401

# Save Chat History
@app.route('/save_chat', methods=['POST'])
def save_chat():
    if 'user_id' not in session:
        return jsonify({"message": "Unauthorized"}), 401

    data = request.get_json()
    user_id = session['user_id']
    message = data['message']
    response = data['response']

    # Save chat history
    chat_history_collection.insert_one({
        'user_id': user_id,
        'message': message,
        'response': response
    })

    return jsonify({"message": "Chat saved successfully"}), 201

# Get Chat History
@app.route('/get_chat_history', methods=['GET'])
def get_chat_history():
    if 'user_id' not in session:
        return jsonify({"message": "Unauthorized"}), 401

    user_id = session['user_id']
    chat_history = list(chat_history_collection.find({'user_id': user_id}, {'_id': 0}))

    return jsonify(chat_history), 200

# AI Chat Endpoint
@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    message = data['message']

    # Simple AI response (replace with actual AI model)
    response = f"AI: You said '{message}'"

    return jsonify({"response": response}), 200

# Check Authentication
@app.route('/check_auth', methods=['GET'])
def check_auth():
    if 'user_id' in session:
        return jsonify({"message": "Authenticated"}), 200
    else:
        return jsonify({"message": "Unauthorized"}), 401

if __name__ == '__main__':
    app.run(debug=True)