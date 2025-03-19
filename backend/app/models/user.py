from app import db
import bcrypt

class User:
    collection = db.users

#Creates a new user in the database with a hashed password.
    @staticmethod
    def create_user(email, password):
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        user = {
            "email": email,
            "password": hashed_password
        }
        User.collection.insert_one(user)
        return user

#Finds a user in the database by their email address.
    @staticmethod
    def find_user_by_email(email):
        return User.collection.find_one({"email": email})
        
#Verifies if the provided password matches the hashed password in the database.
    @staticmethod
    def verify_password(user, password):
        return bcrypt.checkpw(password.encode('utf-8'), user["password"])