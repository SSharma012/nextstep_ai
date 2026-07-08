import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class KnowledgeBase:
    def __init__(self, kb_path="data/knowledge_base"):
        self.kb_path = Path(kb_path)
        self.kb_path.mkdir(parents=True, exist_ok=True)
        self.documents = {
            "careers": {
                "data_scientist": {
                    "name": "Data Scientist",
                    "description": "Extract insights from data using ML and statistics",
                    "skills": ["Python", "SQL", "Machine Learning", "Statistics"],
                    "salary": "$80,000 - $150,000"
                },
                "ml_engineer": {
                    "name": "Machine Learning Engineer",
                    "description": "Build and deploy ML models",
                    "skills": ["Python", "TensorFlow", "PyTorch", "Cloud"],
                    "salary": "$90,000 - $160,000"
                },
                "ai_engineer": {
                    "name": "AI Engineer",
                    "description": "Develop AI solutions using LLMs",
                    "skills": ["Python", "Prompt Engineering", "LLMs", "RAG"],
                    "salary": "$100,000 - $180,000"
                }
            }
        }
        print("✅ Knowledge Base initialized")
    
    def search(self, query, limit=3):
        results = []
        query_lower = query.lower()
        
        for doc_type, doc_content in self.documents.items():
            if isinstance(doc_content, dict):
                for key, value in doc_content.items():
                    if self._matches_query(value, query_lower):
                        results.append({
                            "type": doc_type,
                            "key": key,
                            "content": value
                        })
        
        return results[:limit]
    
    def _matches_query(self, obj, query):
        if isinstance(obj, dict):
            for value in obj.values():
                if self._matches_query(value, query):
                    return True
        elif isinstance(obj, list):
            for item in obj:
                if self._matches_query(item, query):
                    return True
        elif isinstance(obj, str):
            return query in obj.lower()
        return False