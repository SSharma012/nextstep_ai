"""Database models for NextStep AI"""
from datetime import datetime
from typing import Optional, List

class User:
    """User model"""
    
    def __init__(self, user_id: int, username: str, email: str, full_name: str, 
                 password_hash: str, created_at: datetime = None, updated_at: datetime = None):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.full_name = full_name
        self.password_hash = password_hash
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        return {
            'user_id': self.user_id,
            'username': self.username,
            'email': self.email,
            'full_name': self.full_name,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }


class UserProfile:
    """User career profile"""
    
    def __init__(self, profile_id: int, user_id: int, education: Optional[str] = None,
                 skills: Optional[List[str]] = None, interests: Optional[List[str]] = None,
                 career_goal: Optional[str] = None, current_level: str = "beginner",
                 created_at: datetime = None, updated_at: datetime = None):
        self.profile_id = profile_id
        self.user_id = user_id
        self.education = education
        self.skills = skills or []
        self.interests = interests or []
        self.career_goal = career_goal
        self.current_level = current_level  # beginner, intermediate, advanced
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        return {
            'profile_id': self.profile_id,
            'user_id': self.user_id,
            'education': self.education,
            'skills': self.skills,
            'interests': self.interests,
            'career_goal': self.career_goal,
            'current_level': self.current_level,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }


class ChatMessage:
    """Chat message model"""
    
    def __init__(self, message_id: int, user_id: int, role: str, content: str,
                 metadata: Optional[dict] = None, created_at: datetime = None):
        self.message_id = message_id
        self.user_id = user_id
        self.role = role  # 'user' or 'assistant'
        self.content = content
        self.metadata = metadata or {}
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        return {
            'message_id': self.message_id,
            'user_id': self.user_id,
            'role': self.role,
            'content': self.content,
            'metadata': self.metadata,
            'created_at': self.created_at.isoformat()
        }


class Recommendation:
    """Recommendation model"""
    
    def __init__(self, rec_id: int, user_id: int, recommendation_type: str,
                 content: dict, created_at: datetime = None):
        self.rec_id = rec_id
        self.user_id = user_id
        self.recommendation_type = recommendation_type  # career, skill, learning_path, etc
        self.content = content
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        return {
            'rec_id': self.rec_id,
            'user_id': self.user_id,
            'recommendation_type': self.recommendation_type,
            'content': self.content,
            'created_at': self.created_at.isoformat()
        }


class Session:
    """User session model"""
    
    def __init__(self, session_id: int, user_id: int, token: str,
                 created_at: datetime = None, expires_at: datetime = None):
        self.session_id = session_id
        self.user_id = user_id
        self.token = token
        self.created_at = created_at or datetime.now()
        self.expires_at = expires_at
    
    def to_dict(self) -> dict:
        return {
            'session_id': self.session_id,
            'user_id': self.user_id,
            'created_at': self.created_at.isoformat(),
            'expires_at': self.expires_at.isoformat() if self.expires_at else None
        }
