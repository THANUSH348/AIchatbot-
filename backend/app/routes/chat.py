from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.chat import Chat
from app.utils.helpers import load_chatbot, get_chatbot_response

chat_bp = Blueprint('chat', __name__)

# Load the chatbot model
chatbot = load_chatbot()

@chat_bp.route('/chat', methods=['POST'])
@jwt_required()
def chat():
    user_id = get_jwt_identity()
    data = request.get_json()
    message = data.get('message')

    if not message:
        return jsonify({"error": "Message is required"}), 400

    # Retrieve chat history for the user
    chat_history = Chat.get_chat_history(user_id)

    # Format chat history for the chatbot
    formatted_history = {
        "past_user_inputs": [entry["message"] for entry in chat_history],
        "generated_responses": [entry["response"] for entry in chat_history]
    } if chat_history else None

    # Get chatbot response
    response, updated_history = get_chatbot_response(chatbot, message, formatted_history)

    # Save the new chat entry
    Chat.create_chat(user_id, message, response)

    return jsonify({"message": message, "response": response}), 200

@chat_bp.route('/chat/history', methods=['GET'])
@jwt_required()
def chat_history():
    user_id = get_jwt_identity()

    # Retrieve chat history
    history = Chat.get_chat_history(user_id)

    # Format chat history
    formatted_history = [
        {"message": entry["message"], "response": entry["response"], "timestamp": entry["timestamp"]}
        for entry in history
    ]

    return jsonify({"chat_history": formatted_history}), 200