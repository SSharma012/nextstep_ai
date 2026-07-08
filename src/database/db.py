import mysql.connector
from mysql.connector import Error
import hashlib

class Database:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
    
    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            print("✅ Database connected successfully!")
            return True
        except Error as e:
            print(f"❌ Connection Error: {e}")
            return False
    
    def create_tables(self):
        """Create all required tables"""
        try:
            cursor = self.connection.cursor()
            
            # Users table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(255) UNIQUE NOT NULL,
                    email VARCHAR(255) UNIQUE NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    full_name VARCHAR(255),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # User profiles table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_profiles (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL UNIQUE,
                    education_level VARCHAR(100),
                    skills VARCHAR(1000),
                    interests VARCHAR(1000),
                    career_goal VARCHAR(500),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                )
            """)
            
            # Chat history table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS chat_history (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL,
                    user_message TEXT NOT NULL,
                    ai_response TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                )
            """)
            
            self.connection.commit()
            cursor.close()
            print("✅ Tables created successfully!")
        except Error as e:
            print(f"❌ Error creating tables: {e}")
    
    def hash_password(self, password):
        """Hash password using SHA256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def register_user(self, username, email, password, full_name):
        """Register a new user"""
        try:
            cursor = self.connection.cursor()
            hashed_password = self.hash_password(password)
            
            cursor.execute("""
                INSERT INTO users (username, email, password, full_name)
                VALUES (%s, %s, %s, %s)
            """, (username, email, hashed_password, full_name))
            
            self.connection.commit()
            user_id = cursor.lastrowid
            
            # Create user profile
            cursor.execute("""
                INSERT INTO user_profiles (user_id)
                VALUES (%s)
            """, (user_id,))
            
            self.connection.commit()
            cursor.close()
            print(f"✅ User {username} registered successfully!")
            return True
        except Error as e:
            print(f"❌ Registration Error: {e}")
            return False
    
    def login_user(self, username, password):
        """Login user and return user data"""
        try:
            cursor = self.connection.cursor()
            hashed_password = self.hash_password(password)
            
            cursor.execute("""
                SELECT id, username, email, full_name FROM users
                WHERE username = %s AND password = %s
            """, (username, hashed_password))
            
            user = cursor.fetchone()
            cursor.close()
            
            if user:
                print(f"✅ User {username} logged in successfully!")
                return {
                    'id': user[0], 
                    'username': user[1], 
                    'email': user[2], 
                    'full_name': user[3]
                }
            print(f"❌ Invalid credentials for {username}")
            return None
        except Error as e:
            print(f"❌ Login Error: {e}")
            return None
    
    def user_exists(self, username, email):
        """Check if user already exists"""
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                "SELECT id FROM users WHERE username = %s OR email = %s", 
                (username, email)
            )
            result = cursor.fetchone()
            cursor.close()
            return result is not None
        except Error as e:
            print(f"❌ Error checking user: {e}")
            return False
    
    def save_profile(self, user_id, education, skills, interests, goal):
        """Save/Update user profile"""
        try:
            cursor = self.connection.cursor()
            
            # Convert lists to comma-separated strings
            skills_str = ','.join(skills) if isinstance(skills, list) else skills
            interests_str = ','.join(interests) if isinstance(interests, list) else interests
            
            cursor.execute("""
                UPDATE user_profiles
                SET education_level = %s, skills = %s, interests = %s, career_goal = %s
                WHERE user_id = %s
            """, (education, skills_str, interests_str, goal, user_id))
            
            self.connection.commit()
            cursor.close()
            print(f"✅ Profile saved for user {user_id}!")
            return True
        except Error as e:
            print(f"❌ Error saving profile: {e}")
            return False
    
    def get_profile(self, user_id):
        """Get user profile"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                SELECT education_level, skills, interests, career_goal
                FROM user_profiles WHERE user_id = %s
            """, (user_id,))
            result = cursor.fetchone()
            cursor.close()
            
            if result:
                return {
                    'education': result[0],
                    'skills': result[1].split(',') if result[1] else [],
                    'interests': result[2].split(',') if result[2] else [],
                    'goal': result[3]
                }
            
            # Return empty profile if not found
            return {
                'education': None,
                'skills': [],
                'interests': [],
                'goal': None
            }
        except Error as e:
            print(f"❌ Error getting profile: {e}")
            return None
    
    def save_chat(self, user_id, user_message, ai_response):
        """Save chat message to history"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                INSERT INTO chat_history (user_id, user_message, ai_response)
                VALUES (%s, %s, %s)
            """, (user_id, user_message, ai_response))
            
            self.connection.commit()
            cursor.close()
            return True
        except Error as e:
            print(f"❌ Error saving chat: {e}")
            return False
    
    def get_chat_history(self, user_id, limit=50):
        """Get user's chat history"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                SELECT user_message, ai_response, created_at
                FROM chat_history WHERE user_id = %s
                ORDER BY created_at DESC LIMIT %s
            """, (user_id, limit))
            
            results = cursor.fetchall()
            cursor.close()
            return results
        except Error as e:
            print(f"❌ Error getting chat history: {e}")
            return []
    
    def close(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
            print("✅ Database connection closed!")