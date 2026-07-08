import logging
from typing import Dict, List, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class ContextManager:
    """Manages conversation context and agent state"""
    
    def __init__(self, user_id: int, tools):
        self.user_id = user_id
        self.tools = tools
        self.conversation_history = []
        self.user_profile = {}
        self.current_career_focus = None
        self.recommendations_given = []
        self.session_start = datetime.now()
        self.agent_state = "initialized"
        
        logger.info(f"✅ Context Manager initialized for user {user_id}")
    
    # ============ CONTEXT INITIALIZATION ============
    
    def initialize_context(self) -> Dict[str, Any]:
        """
        Initialize context by loading user profile and history
        
        Returns:
            Initial context dictionary
        """
        try:
            # Load user profile
            self.user_profile = self.tools.get_user_profile(self.user_id)
            
            # Load chat history
            history = self.tools.get_chat_history(self.user_id, limit=5)
            self.conversation_history = history
            
            context = {
                "user_id": self.user_id,
                "profile": self.user_profile,
                "recent_history": history,
                "session_start": self.session_start.isoformat(),
                "state": "ready"
            }
            
            self.agent_state = "ready"
            logger.info(f"✅ Context initialized for user {self.user_id}")
            return context
        except Exception as e:
            logger.error(f"❌ Error initializing context: {e}")
            return {"error": str(e)}
    
    # ============ CONVERSATION MANAGEMENT ============
    
    def add_message(self, role: str, content: str, metadata: Dict[str, Any] = None) -> None:
        """
        Add message to conversation history
        
        Args:
            role: "user" or "assistant"
            content: Message content
            metadata: Optional metadata
        """
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata or {}
        }
        self.conversation_history.append(message)
        logger.info(f"✅ Message added: {role}")
    
    def get_conversation_summary(self, last_n: int = 5) -> str:
        """
        Get summary of last n messages for context
        
        Args:
            last_n: Number of recent messages
            
        Returns:
            Formatted conversation summary
        """
        recent = self.conversation_history[-last_n:]
        summary = ""
        
        for msg in recent:
            role = msg["role"].upper()
            content = msg["content"][:100]  # First 100 chars
            summary += f"\n{role}: {content}..."
        
        return summary
    
    def get_full_history(self) -> List[Dict[str, Any]]:
        """Get full conversation history"""
        return self.conversation_history
    
    # ============ USER PROFILE MANAGEMENT ============
    
    def update_user_profile(self, education: str = None, skills: List[str] = None,
                           interests: List[str] = None, goal: str = None) -> bool:
        """
        Update user profile
        
        Args:
            education: Education level
            skills: List of skills
            interests: List of interests
            goal: Career goal
            
        Returns:
            Success status
        """
        try:
            # Use existing values if not provided
            edu = education or self.user_profile.get('education')
            skls = skills or self.user_profile.get('skills', [])
            ints = interests or self.user_profile.get('interests', [])
            gol = goal or self.user_profile.get('goal')
            
            # Save to database
            success = self.tools.save_user_profile(self.user_id, edu, skls, ints, gol)
            
            if success:
                self.user_profile = {
                    'education': edu,
                    'skills': skls,
                    'interests': ints,
                    'goal': gol
                }
                logger.info(f"✅ Profile updated for user {self.user_id}")
            
            return success
        except Exception as e:
            logger.error(f"❌ Error updating profile: {e}")
            return False
    
    def get_user_profile(self) -> Dict[str, Any]:
        """Get current user profile"""
        return self.user_profile
    
    # ============ CAREER FOCUS MANAGEMENT ============
    
    def set_career_focus(self, career: str) -> None:
        """Set current career focus"""
        self.current_career_focus = career
        logger.info(f"✅ Career focus set to: {career}")
    
    def get_career_focus(self) -> Optional[str]:
        """Get current career focus"""
        return self.current_career_focus
    
    # ============ RECOMMENDATION TRACKING ============
    
    def add_recommendation(self, recommendation_type: str, content: Dict[str, Any]) -> None:
        """
        Track given recommendations
        
        Args:
            recommendation_type: Type of recommendation
            content: Recommendation content
        """
        rec = {
            "type": recommendation_type,
            "content": content,
            "timestamp": datetime.now().isoformat()
        }
        self.recommendations_given.append(rec)
        logger.info(f"✅ Recommendation tracked: {recommendation_type}")
    
    def get_recommendations_given(self) -> List[Dict[str, Any]]:
        """Get all recommendations given in this session"""
        return self.recommendations_given
    
    # ============ AGENT STATE MANAGEMENT ============
    
    def set_state(self, state: str) -> None:
        """
        Set agent state
        
        States:
        - initialized: Agent just initialized
        - gathering_info: Collecting user information
        - analyzing: Analyzing user profile
        - recommending: Providing recommendations
        - teaching: Teaching/explaining
        - ready: Ready for next interaction
        - error: Error occurred
        """
        self.agent_state = state
        logger.info(f"✅ Agent state changed to: {state}")
    
    def get_state(self) -> str:
        """Get current agent state"""
        return self.agent_state
    
    # ============ CONTEXT RETRIEVAL ============
    
    def get_agent_context(self) -> Dict[str, Any]:
        """
        Get complete agent context for decision making
        
        Returns:
            Complete context dictionary
        """
        return {
            "user_id": self.user_id,
            "profile": self.user_profile,
            "career_focus": self.current_career_focus,
            "recent_history": self.conversation_history[-5:],
            "recommendations_given": len(self.recommendations_given),
            "session_duration": (datetime.now() - self.session_start).total_seconds() / 60,
            "state": self.agent_state,
            "session_start": self.session_start.isoformat()
        }
    
    def should_ask_for_profile(self) -> bool:
        """
        Determine if agent should ask for profile information
        
        Returns:
            True if profile is incomplete
        """
        profile = self.user_profile
        return not profile or \
               not profile.get('education') or \
               not profile.get('skills') or \
               not profile.get('interests')
    
    def should_recommend_careers(self) -> bool:
        """
        Determine if agent should recommend careers
        
        Returns:
            True if enough information collected
        """
        profile = self.user_profile
        return profile and \
               profile.get('skills') and \
               profile.get('interests') and \
               len(self.recommendations_given) == 0
    
    def should_provide_learning_path(self) -> bool:
        """
        Determine if agent should provide learning path
        
        Returns:
            True if career focus selected
        """
        return self.current_career_focus is not None
    
    # ============ SESSION SUMMARY ============
    
    def generate_session_summary(self) -> Dict[str, Any]:
        """
        Generate summary of this session
        
        Returns:
            Session summary dictionary
        """
        session_duration = (datetime.now() - self.session_start).total_seconds() / 60
        
        summary = {
            "user_id": self.user_id,
            "session_start": self.session_start.isoformat(),
            "session_duration_minutes": round(session_duration, 2),
            "messages_exchanged": len(self.conversation_history),
            "recommendations_given": len(self.recommendations_given),
            "career_focus": self.current_career_focus,
            "profile_completed": not self.should_ask_for_profile(),
            "final_state": self.agent_state
        }
        
        logger.info(f"✅ Session summary generated: {summary}")
        return summary
    
    def clear_session(self) -> None:
        """Clear session data (for new session)"""
        self.conversation_history = []
        self.current_career_focus = None
        self.recommendations_given = []
        self.session_start = datetime.now()
        self.agent_state = "initialized"
        logger.info(f"✅ Session cleared for user {self.user_id}")
