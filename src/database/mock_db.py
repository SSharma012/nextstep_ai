# src/database/mock_db.py
import json
import os
import hashlib
from datetime import datetime
from typing import List, Dict, Any, Optional

DATA_FILE_DEFAULT = os.path.join("data", "mock_db.json")


class MockDatabase:
    """
    Simple JSON-backed mock database that exposes the same methods
    used by the app's Database class.
    """

    def __init__(self, file_path: str = DATA_FILE_DEFAULT):
        self.file_path = file_path
        self._data: Dict[str, Any] = {
            "users": [],
            "profiles": {},
            "chat_history": [],
            "counters": {"user_id": 0}
        }
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        self._load()
        self._ensure_demo_user()

    def _load(self):
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, "r", encoding="utf-8") as f:
                    self._data = json.load(f)
            except Exception:
                self._data = {
                    "users": [],
                    "profiles": {},
                    "chat_history": [],
                    "counters": {"user_id": 0}
                }
                self._save()
        else:
            self._save()

    def _save(self):
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(self._data, f, indent=2, default=str)

    def _now(self) -> str:
        return datetime.utcnow().isoformat()

    def _hash(self, password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    def _ensure_demo_user(self):
        demo_exists = any(u["username"] == "demo" for u in self._data["users"])
        if not demo_exists:
            self.register_user("demo", "demo@example.com", "demo123", "Demo User")

    def connect(self) -> bool:
        return True

    def create_tables(self):
        return True

    def hash_password(self, password: str) -> str:
        return self._hash(password)

    def register_user(self, username: str, email: str, password: str, full_name: str) -> bool:
        try:
            if self.user_exists(username, email):
                return False
            new_id = self._data["counters"].get("user_id", 0) + 1
            self._data["counters"]["user_id"] = new_id
            user = {
                "id": new_id,
                "username": username,
                "email": email,
                "password": self._hash(password),
                "full_name": full_name,
                "created_at": self._now()
            }
            self._data["users"].append(user)
            self._data["profiles"][str(new_id)] = {
                "education_level": None,
                "skills": [],
                "interests": [],
                "career_goal": None,
                "created_at": self._now()
            }
            self._save()
            return True
        except Exception:
            return False

    def login_user(self, username: str, password: str) -> Optional[Dict[str, Any]]:
        hashed = self._hash(password)
        for u in self._data["users"]:
            if u["username"] == username and u["password"] == hashed:
                return {
                    "id": u["id"],
                    "username": u["username"],
                    "email": u["email"],
                    "full_name": u.get("full_name", "")
                }
        return None

    def user_exists(self, username: str, email: str) -> bool:
        for u in self._data["users"]:
            if u["username"] == username or u["email"] == email:
                return True
        return False

    def save_profile(self, user_id: int, education, skills, interests, goal) -> bool:
        try:
            uid = str(user_id)
            if uid not in self._data["profiles"]:
                self._data["profiles"][uid] = {
                    "education_level": education,
                    "skills": skills if isinstance(skills, list) else (skills or []),
                    "interests": interests if isinstance(interests, list) else (interests or []),
                    "career_goal": goal,
                    "created_at": self._now()
                }
            else:
                self._data["profiles"][uid].update({
                    "education_level": education,
                    "skills": skills if isinstance(skills, list) else (skills or []),
                    "interests": interests if isinstance(interests, list) else (interests or []),
                    "career_goal": goal,
                })
            self._save()
            return True
        except Exception:
            return False

    def get_profile(self, user_id: int):
        try:
            uid = str(user_id)
            p = self._data["profiles"].get(uid)
            if not p:
                return {
                    "education": None,
                    "skills": [],
                    "interests": [],
                    "goal": None
                }
            return {
                "education": p.get("education_level"),
                "skills": p.get("skills") or [],
                "interests": p.get("interests") or [],
                "goal": p.get("career_goal")
            }
        except Exception:
            return {
                "education": None,
                "skills": [],
                "interests": [],
                "goal": None
            }

    def save_chat(self, user_id: int, user_message: str, ai_response: str) -> bool:
        try:
            self._data["chat_history"].append({
                "user_id": user_id,
                "user_message": user_message,
                "ai_response": ai_response,
                "created_at": self._now()
            })
            self._save()
            return True
        except Exception:
            return False

    def get_chat_history(self, user_id: int, limit: int = 50) -> List:
        try:
            items = [ (c["user_message"], c["ai_response"], c["created_at"]) for c in reversed(self._data["chat_history"]) if c["user_id"] == user_id ]
            return items[:limit]
        except Exception:
            return []

    def close(self):
        return True
