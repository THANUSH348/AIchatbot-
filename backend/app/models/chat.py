from datetime import datetime
from app import db

class Chat:
    collection = db.chats
    
    # Create a chat entry dictionary with user ID, message, response, and timestamp
    @staticmethod
    def create_chat(user_id, message, response):
        chat_entry = {
            "user_id": user_id,
            "message": message,
            "response": response,
            "timestamp": datetime.utcnow()
        }
        Chat.collection.insert_one(chat_entry)
        return chat_entry

    @staticmethod
    def get_chat_history(user_id):
        # Retrieve chat history sorted by timestamp
        history = Chat.collection.find({"user_id": user_id}).sort("timestamp", 1)
        return list(history)