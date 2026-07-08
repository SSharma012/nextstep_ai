import logging
from typing import List, Dict, Any, Optional
import json

logger = logging.getLogger(__name__)

class AgentTools:
    """Tools that AI Agent uses to make decisions"""
    
    def __init__(self, knowledge_base, database):
        self.kb = knowledge_base
        self.db = database
        logger.info("✅ Agent Tools initialized")
    
    # ============ KNOWLEDGE BASE TOOLS ============
    
    def search_knowledge_base(self, query: str, limit: int = 3) -> List[Dict[str, Any]]:
        """
        Search knowledge base for relevant information
        
        Args:
            query: Search query
            limit: Number of results to return
            
        Returns:
            List of relevant documents
        """
        try:
            results = self.kb.search(query, limit=limit)
            logger.info(f"✅ Found {len(results)} KB results for: {query}")
            return results
        except Exception as e:
            logger.error(f"❌ KB Search Error: {e}")
            return []
    
    def get_career_details(self, career_name: str) -> Dict[str, Any]:
        """
        Get detailed information about a specific career
        
        Args:
            career_name: Name of the career
            
        Returns:
            Career details dictionary
        """
        try:
            career_info = self.kb.get_career_info(career_name)
            if career_info:
                logger.info(f"✅ Retrieved details for: {career_name}")
                return career_info
            logger.warning(f"⚠️ Career not found: {career_name}")
            return {}
        except Exception as e:
            logger.error(f"❌ Error getting career details: {e}")
            return {}
    
    def get_skill_details(self, skill_name: str) -> Dict[str, Any]:
        """
        Get detailed information about a specific skill
        
        Args:
            skill_name: Name of the skill
            
        Returns:
            Skill details dictionary
        """
        try:
            skill_info = self.kb.get_skill_info(skill_name)
            if skill_info:
                logger.info(f"✅ Retrieved details for skill: {skill_name}")
                return skill_info
            logger.warning(f"⚠️ Skill not found: {skill_name}")
            return {}
        except Exception as e:
            logger.error(f"❌ Error getting skill details: {e}")
            return {}
    
    def get_all_careers(self) -> List[str]:
        """Get list of all available careers"""
        try:
            careers = self.kb.get_all_careers()
            logger.info(f"✅ Retrieved {len(careers)} careers")
            return careers
        except Exception as e:
            logger.error(f"❌ Error getting careers: {e}")
            return []
    
    def get_all_skills(self) -> List[str]:
        """Get list of all available skills"""
        try:
            skills = self.kb.get_all_skills()
            logger.info(f"✅ Retrieved {len(skills)} skills")
            return skills
        except Exception as e:
            logger.error(f"❌ Error getting skills: {e}")
            return []
    
    # ============ USER PROFILE TOOLS ============
    
    def get_user_profile(self, user_id: int) -> Dict[str, Any]:
        """
        Get user's profile from database
        
        Args:
            user_id: User ID
            
        Returns:
            User profile dictionary
        """
        try:
            profile = self.db.get_profile(user_id)
            if profile:
                logger.info(f"✅ Retrieved profile for user: {user_id}")
                return profile
            logger.warning(f"⚠️ No profile found for user: {user_id}")
            return {
                'education': None,
                'skills': [],
                'interests': [],
                'goal': None
            }
        except Exception as e:
            logger.error(f"❌ Error getting user profile: {e}")
            return {}
    
    def save_user_profile(self, user_id: int, education: str, skills: List[str], 
                         interests: List[str], goal: str) -> bool:
        """
        Save user profile to database
        
        Args:
            user_id: User ID
            education: Education level
            skills: List of skills
            interests: List of interests
            goal: Career goal
            
        Returns:
            Success status
        """
        try:
            success = self.db.save_profile(user_id, education, skills, interests, goal)
            if success:
                logger.info(f"✅ Profile saved for user: {user_id}")
            return success
        except Exception as e:
            logger.error(f"❌ Error saving profile: {e}")
            return False
    
    # ============ SKILL ANALYSIS TOOLS ============
    
    def calculate_skill_gap(self, user_skills: List[str], career_name: str) -> Dict[str, Any]:
        """
        Calculate skill gap between user's current skills and required skills for a career
        
        Args:
            user_skills: User's current skills
            career_name: Target career
            
        Returns:
            Dictionary with skill gap analysis
        """
        try:
            career_info = self.kb.get_career_info(career_name)
            if not career_info:
                return {"error": f"Career '{career_name}' not found"}
            
            required_skills = career_info.get('skills', [])
            user_skills_lower = [s.lower() for s in user_skills]
            required_skills_lower = [s.lower() for s in required_skills]
            
            # Calculate skills
            existing_skills = [s for s in required_skills if s.lower() in user_skills_lower]
            missing_skills = [s for s in required_skills if s.lower() not in user_skills_lower]
            
            coverage = len(existing_skills) / len(required_skills) * 100 if required_skills else 0
            
            result = {
                "career": career_name,
                "existing_skills": existing_skills,
                "missing_skills": missing_skills,
                "coverage_percentage": round(coverage, 2),
                "required_skills": required_skills,
                "recommendation": self._generate_skill_gap_recommendation(coverage)
            }
            
            logger.info(f"✅ Calculated skill gap for {career_name}: {coverage}%")
            return result
        except Exception as e:
            logger.error(f"❌ Error calculating skill gap: {e}")
            return {"error": str(e)}
    
    def _generate_skill_gap_recommendation(self, coverage: float) -> str:
        """Generate recommendation based on coverage percentage"""
        if coverage >= 80:
            return "🟢 Excellent! You have most required skills. Ready to apply!"
        elif coverage >= 60:
            return "🟡 Good! Learn 2-3 missing skills to be job-ready."
        elif coverage >= 40:
            return "🟠 Fair. You need to learn 3-4 more skills."
        else:
            return "🔴 Start with foundational skills first."
    
    # ============ CAREER RECOMMENDATION TOOLS ============
    
    def recommend_careers(self, user_skills: List[str], interests: List[str]) -> List[Dict[str, Any]]:
        """
        Recommend suitable careers based on user's skills and interests
        
        Args:
            user_skills: User's current skills
            interests: User's interests
            
        Returns:
            List of recommended careers with scores
        """
        try:
            recommended = self.kb.get_recommendations(user_skills, interests)
            
            # Get detailed info and calculate scores
            careers_with_scores = []
            for career_name in recommended:
                career_info = self.kb.get_career_info(career_name)
                if career_info:
                    # Calculate match score
                    skill_match = sum(1 for skill in user_skills 
                                    if skill.lower() in [s.lower() for s in career_info.get('skills', [])])
                    score = (skill_match / len(career_info.get('skills', [])) * 100) if career_info.get('skills') else 0
                    
                    careers_with_scores.append({
                        "name": career_name,
                        "description": career_info.get('description', ''),
                        "salary": career_info.get('salary', ''),
                        "demand": career_info.get('demand', ''),
                        "match_score": round(score, 2),
                        "required_skills": career_info.get('skills', [])
                    })
            
            # Sort by match score
            careers_with_scores.sort(key=lambda x: x['match_score'], reverse=True)
            logger.info(f"✅ Generated {len(careers_with_scores)} career recommendations")
            return careers_with_scores
        except Exception as e:
            logger.error(f"❌ Error recommending careers: {e}")
            return []
    
    # ============ SKILL RECOMMENDATION TOOLS ============
    
    def recommend_skills(self, target_career: str, user_skills: List[str]) -> Dict[str, Any]:
        """
        Recommend skills to learn for a target career
        
        Args:
            target_career: Target career
            user_skills: Current skills
            
        Returns:
            Dictionary with skill recommendations
        """
        try:
            career_info = self.kb.get_career_info(target_career)
            if not career_info:
                return {"error": f"Career '{target_career}' not found"}
            
            required_skills = career_info.get('skills', [])
            user_skills_lower = [s.lower() for s in user_skills]
            
            # Categorize skills
            priority_skills = []
            advanced_skills = []
            
            for i, skill in enumerate(required_skills):
                if skill.lower() not in user_skills_lower:
                    if i < 3:  # First few are priorities
                        priority_skills.append(skill)
                    else:
                        advanced_skills.append(skill)
            
            result = {
                "career": target_career,
                "priority_skills": priority_skills,
                "advanced_skills": advanced_skills,
                "learning_roadmap": career_info.get('roadmap', ''),
                "estimated_time": "3-6 months"
            }
            
            logger.info(f"✅ Generated skill recommendations for {target_career}")
            return result
        except Exception as e:
            logger.error(f"❌ Error recommending skills: {e}")
            return {"error": str(e)}
    
    # ============ LEARNING PATH TOOLS ============
    
    def generate_learning_roadmap(self, target_career: str, user_level: str = "beginner") -> Dict[str, Any]:
        """
        Generate personalized learning roadmap
        
        Args:
            target_career: Target career
            user_level: Current level (beginner/intermediate/advanced)
            
        Returns:
            Detailed learning roadmap
        """
        try:
            career_info = self.kb.get_career_info(target_career)
            if not career_info:
                return {"error": f"Career '{target_career}' not found"}
            
            roadmap = {
                "career": target_career,
                "level": user_level,
                "skills": career_info.get('skills', []),
                "roadmap": career_info.get('roadmap', ''),
                "projects": career_info.get('projects', []),
                "certifications": career_info.get('certifications', []),
                "timeline": self._generate_timeline(target_career, user_level)
            }
            
            logger.info(f"✅ Generated learning roadmap for {target_career}")
            return roadmap
        except Exception as e:
            logger.error(f"❌ Error generating roadmap: {e}")
            return {"error": str(e)}
    
    def _generate_timeline(self, career: str, level: str) -> Dict[str, str]:
        """Generate learning timeline based on career and level"""
        timelines = {
            "beginner": {
                "phase1": "Month 1-2: Foundation (Basic skills, fundamentals)",
                "phase2": "Month 3-4: Intermediate (Advanced concepts, mini-projects)",
                "phase3": "Month 5-6: Advanced (Major projects, certifications)",
                "phase4": "Month 6-8: Mastery (Portfolio building, job search)"
            },
            "intermediate": {
                "phase1": "Week 1-2: Foundations (Quick refresher)",
                "phase2": "Week 3-8: Advanced Topics (Deep learning)",
                "phase3": "Week 9-12: Projects & Practice (Real-world applications)",
                "phase4": "Week 13-16: Specialization & Job Search"
            },
            "advanced": {
                "phase1": "Week 1-4: Advanced Concepts (Cutting edge topics)",
                "phase2": "Week 5-8: Industry Projects (Real problems)",
                "phase3": "Week 9-12: Leadership & Mentoring",
                "phase4": "Week 13+: Specialization & Expert Path"
            }
        }
        
        return timelines.get(level, timelines["beginner"])
    
    # ============ PROJECT RECOMMENDATION TOOLS ============
    
    def get_projects(self, career: str, level: str = "beginner") -> List[Dict[str, Any]]:
        """
        Get project recommendations for a career and level
        
        Args:
            career: Career name
            level: Project level (beginner/intermediate/advanced)
            
        Returns:
            List of projects
        """
        try:
            projects_data = self.kb.documents.get("projects", {})
            level_projects = projects_data.get(level, [])
            
            result = {
                "career": career,
                "level": level,
                "projects": level_projects,
                "total": len(level_projects)
            }
            
            logger.info(f"✅ Retrieved {len(level_projects)} projects for {level} level")
            return result
        except Exception as e:
            logger.error(f"❌ Error getting projects: {e}")
            return {"error": str(e)}
    
    # ============ CERTIFICATION TOOLS ============
    
    def get_certifications(self, career: str) -> List[Dict[str, Any]]:
        """
        Get certification recommendations for a career
        
        Args:
            career: Career name
            
        Returns:
            List of relevant certifications
        """
        try:
            certifications = self.kb.documents.get("certifications", {})
            
            result = {
                "career": career,
                "certifications": list(certifications.values()),
                "total": len(certifications)
            }
            
            logger.info(f"✅ Retrieved {len(certifications)} certifications for {career}")
            return result
        except Exception as e:
            logger.error(f"❌ Error getting certifications: {e}")
            return {"error": str(e)}
    
    # ============ INTERVIEW PREPARATION TOOLS ============
    
    def get_interview_prep(self, role: str) -> Dict[str, Any]:
        """
        Get interview preparation materials
        
        Args:
            role: Job role
            
        Returns:
            Interview preparation guide
        """
        try:
            interview_data = self.kb.documents.get("interview_prep", {})
            
            result = {
                "role": role,
                "technical": interview_data.get("technical", {}),
                "behavioral": interview_data.get("behavioral", []),
                "preparation_strategy": interview_data.get("preparation_strategy", [])
            }
            
            logger.info(f"✅ Retrieved interview prep for {role}")
            return result
        except Exception as e:
            logger.error(f"❌ Error getting interview prep: {e}")
            return {"error": str(e)}
    
    # ============ RESOURCES TOOLS ============
    
    def get_learning_resources(self) -> Dict[str, Any]:
        """Get all available learning resources"""
        try:
            resources = self.kb.documents.get("resources", {})
            
            result = {
                "learning_platforms": resources.get("learning_platforms", []),
                "coding_practice": resources.get("coding_practice", []),
                "communities": resources.get("communities", [])
            }
            
            logger.info(f"✅ Retrieved learning resources")
            return result
        except Exception as e:
            logger.error(f"❌ Error getting resources: {e}")
            return {"error": str(e)}
    
    # ============ CHAT HISTORY TOOLS ============
    
    def save_recommendation(self, user_id: int, recommendation_type: str, 
                           content: Dict[str, Any]) -> bool:
        """
        Save recommendation to chat history
        
        Args:
            user_id: User ID
            recommendation_type: Type of recommendation
            content: Content to save
            
        Returns:
            Success status
        """
        try:
            summary = f"{recommendation_type}: {json.dumps(content)[:100]}..."
            success = self.db.save_chat(user_id, recommendation_type, summary)
            if success:
                logger.info(f"✅ Recommendation saved for user {user_id}")
            return success
        except Exception as e:
            logger.error(f"❌ Error saving recommendation: {e}")
            return False
    
    def get_chat_history(self, user_id: int, limit: int = 10) -> List[tuple]:
        """
        Get user's chat history
        
        Args:
            user_id: User ID
            limit: Number of messages to retrieve
            
        Returns:
            List of chat messages
        """
        try:
            history = self.db.get_chat_history(user_id, limit=limit)
            logger.info(f"✅ Retrieved {len(history)} messages for user {user_id}")
            return history
        except Exception as e:
            logger.error(f"❌ Error getting chat history: {e}")
            return []
