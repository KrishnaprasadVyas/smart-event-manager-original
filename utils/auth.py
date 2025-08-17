import hashlib
import json
import os

class Auth:
    USERS_FILE = "users.json"
    logged_in_user = None

    @staticmethod
    def _load_users():
        if not os.path.exists(Auth.USERS_FILE):
            return {}
        with open(Auth.USERS_FILE, "r") as f:
            return json.load(f)

    @staticmethod
    def _save_users(users):
        with open(Auth.USERS_FILE, "w") as f:
            json.dump(users, f)

    @staticmethod
    def register(username, password):
        users = Auth._load_users()
        if username in users:
            return "❌ Username already exists!"
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        users[username] = password_hash
        Auth._save_users(users)
        return "✅ User registered successfully!"

    @staticmethod
    def login(username, password):
        users = Auth._load_users()
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        if users.get(username) == password_hash:
            Auth.logged_in_user = username
            return f"✅ {username} logged in successfully!"
        return "❌ Invalid username or password."

    @staticmethod
    def logout():
        if Auth.logged_in_user:
            user = Auth.logged_in_user
            Auth.logged_in_user = None
            return f"👋 {user} logged out."
        return "⚠️ No user is currently logged in."
