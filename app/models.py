# models.py
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from bson import ObjectId
from pymongo import MongoClient
import os

# Reutilizamos la conexión a la BD
client = MongoClient(os.getenv("MONGO_URI"))
db = client['data']
users_collection = db.Users

class User(UserMixin):
    def __init__(self, user_data):
        self.id = str(user_data.get('_id'))
        self.email = user_data.get('email')
        self.password_hash = user_data.get('password_hash')

    def set_password(self, password):
        # NUNCA guardes la contraseña en texto plano.
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def get(user_id):
        user_data = users_collection.find_one({'_id': ObjectId(user_id)})
        if user_data:
            return User(user_data)
        return None

    @staticmethod
    def get_by_email(email):
        user_data = users_collection.find_one({'email': email})
        if user_data:
            return User(user_data)
        return None