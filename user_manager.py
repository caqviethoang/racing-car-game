import json
import hashlib
from pathlib import Path

class UserManager:
    def __init__(self):
        self.root_path = str(Path(__file__).parent)
        self.users_file = self.root_path + "/users.json"
        self.load_users()
    
    def load_users(self):
        try:
            with open(self.users_file, 'r') as f:
                self.users = json.load(f)
        except FileNotFoundError:
            self.users = {}
    
    def save_users(self):
        with open(self.users_file, 'w') as f:
            json.dump(self.users, f, indent=4)
    
    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    def register(self, username, password):
        if username in self.users:
            return False, "Username already exists!"
        
        if len(username) < 3:
            return False, "Username must be at least 3 characters long!"
        
        if len(password) < 4:
            return False, "Password must be at least 4 characters long!"
        
        self.users[username] = {
            'password_hash': self.hash_password(password),
            'high_score': 0
        }
        self.save_users()
        return True, "Registration successful!"
    
    def login(self, username, password):
        if username not in self.users:
            return False, "Username not found!", 0
        
        if self.users[username]['password_hash'] != self.hash_password(password):
            return False, "Invalid password!", 0
        
        return True, "Login successful!", self.users[username].get('high_score', 0)
    
    def update_high_score(self, username, score):
        if username in self.users and score > self.users[username].get('high_score', 0):
            self.users[username]['high_score'] = score
            self.save_users()
            return True
        return False
    
    def get_high_scores(self):
        scores = [(username, user_data.get('high_score', 0)) 
                 for username, user_data in self.users.items()]
        return sorted(scores, key=lambda x: x[1], reverse=True)