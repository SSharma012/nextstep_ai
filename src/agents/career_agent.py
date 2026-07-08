import logging
from typing import Dict, List, Any, Optional
import json
from src.agents.tools import AgentTools
from src.agents.context_manager import ContextManager

logger = logging.getLogger(__name__)

class CareerAgent:
    """Intelligent Career Counselor Agent
    
    Multi-step reasoning agent that:
    - Analyzes user profiles
    - Recommends careers
    - Generates learning paths
    - Provides interview prep
    - Tracks progress
    """
    
    def __init__(self, user_id: int, tools: AgentTools, context_manager: ContextManager, watsonx_client):
        self.user_id = user_id
        self.tools = tools
        self.context = context_manager
        self.watsonx = watsonx_client
        self.reasoning_steps = []
        
        logger.info(f"✅ Career Agent initialized for user {user_id}")
    
    # ============ MAIN AGENT LOOP ============
    
    async def process_user_input(self, user_input: str) -> Dict[str, Any]:
        """
        Process user input through multi-step agent reasoning
        
        Args:
            user_input: User's message
            
        Returns:
            Agent response with reasoning
        """
        self.reasoning_steps = []
        
        try:
            # Step 1: Parse intent
            intent = self._parse_intent(user_input)
            self._add_reasoning_step(f"Intent parsed: {intent}")
            
            # Step 2: Get agent context
            agent_context = self.context.get_agent_context()
            self._add_reasoning_step(f"Context loaded: user has {len(agent_context['profile'])} profile fields")
            
            # Step 3: Route based on intent
            if intent == "profile_setup":
                response = await self._handle_profile_setup(user_input)
            elif intent == "career_exploration":
                response = await self._handle_career_exploration(user_input)
            elif intent == "career_recommendation":
                response = await self._handle_career_recommendation()
            elif intent == "learning_path":
                response = await self._handle_learning_path(user_input)
            elif intent == "skill_assessment":
                response = await self._handle_skill_assessment()
            elif intent == "interview_prep":
                response = await self._handle_interview_prep()
            elif intent == "general_guidance":
                response = await self._handle_general_guidance(user_input)
            else:
                response = await self._handle_unknown_intent(user_input)
            
            # Step 4: Add response to context
            self.context.add_message("assistant", response["message"])
            self.context.add_message("user", user_input)
            
            # Step 5: Save if recommendation given
            if response.get("recommendation"):
                self.tools.save_recommendation(
                    self.user_id,
                    intent,
                    response["recommendation"]
                )
            
            response["reasoning_steps"] = self.reasoning_steps
            self.context.set_state("ready")
            
            return response
        
        except Exception as e:
            logger.error(f"❌ Error processing input: {e}")
            self.context.set_state("error")
            return {
                "message": f"Sorry, I encountered an error: {str(e)}",
                "error": str(e),
                "reasoning_steps": self.reasoning_steps
            }
    
    # ============ INTENT DETECTION ============
    
    def _parse_intent(self, user_input: str) -> str:
        """
        Parse user intent from input
        
        Args:
            user_input: User's message
            
        Returns:
            Detected intent
        """
        user_lower = user_input.lower()
        
        # Intent keywords
        intents = {
            "profile_setup": ["setup", "profile", "about me", "tell you", "education", "skills"],
            "career_exploration": ["explore", "career", "jobs", "roles", "what", "interested"],
            "career_recommendation": ["recommend", "suitable", "best", "match", "suggest"],
            "learning_path": ["learn", "roadmap", "path", "course", "study", "prepare"],
            "skill_assessment": ["gap", "assess", "skills", "missing", "need"],
            "interview_prep": ["interview", "prepare", "questions", "practice"],
            "general_guidance": ["help", "guide", "advice", "tip", "how", "can"]
        }
        
        for intent, keywords in intents.items():
            for keyword in keywords:
                if keyword in user_lower:
                    return intent
        
        return "general_guidance"
    
    # ============ INTENT HANDLERS ============
    
    async def _handle_profile_setup(self, user_input: str) -> Dict[str, Any]:
        """Handle profile setup/update"""
        self.context.set_state("gathering_info")
        self._add_reasoning_step("Profile setup handler activated")
        
        # Ask Watsonx to extract information from user input
        prompt = f"""Extract career-related information from this text:
        
        User input: {user_input}
        
        Extract: education level, skills mentioned, interests, career goals
        Return as JSON."""
        
        response = await self.watsonx.generate_text(prompt)
        self._add_reasoning_step(f"Watsonx extracted: {response[:50]}...")
        
        # Parse extracted information
        try:
            info = json.loads(response)
            self.context.update_user_profile(
                education=info.get('education'),
                skills=info.get('skills', []),
                interests=info.get('interests', []),
                goal=info.get('goal')
            )
            self._add_reasoning_step("Profile updated in database")
            
            message = f"✅ Great! I've saved your profile:\n"
            message += f"📚 Education: {info.get('education', 'Not specified')}\n"
            message += f"💻 Skills: {', '.join(info.get('skills', []))}\n"
            message += f"🎯 Interests: {', '.join(info.get('interests', []))}\n"
            message += f"🎪 Goal: {info.get('goal', 'Not specified')}\n\n"
            message += "Now I can help you explore careers that match your profile!"
            
        except:
            message = f"I'm updating your profile based on what you shared. Tell me more details about your education, skills, or career interests."
        
        return {
            "message": message,
            "type": "profile_setup",
            "action": "profile_updated"
        }
    
    async def _handle_career_exploration(self, user_input: str) -> Dict[str, Any]:
        """Handle career exploration queries"""
        self.context.set_state("analyzing")
        self._add_reasoning_step("Career exploration handler activated")
        
        # Search knowledge base
        results = self.tools.search_knowledge_base(user_input, limit=3)
        self._add_reasoning_step(f"Found {len(results)} KB results")
        
        if not results:
            return {
                "message": "I couldn't find specific information about that career. Can you tell me which career you're interested in?",
                "type": "career_exploration"
            }
        
        # Get details of top result
        career_name = results[0]["content"]["name"]
        self.context.set_career_focus(career_name)
        self._add_reasoning_step(f"Career focus set to: {career_name}")
        
        career_info = self.tools.get_career_details(career_name)
        
        # Generate response using Watsonx
        prompt = f"""Provide an engaging explanation about this career:
        
        Career: {career_name}
        Description: {career_info.get('description')}
        Skills: {', '.join(career_info.get('skills', []))}
        Salary: {career_info.get('salary')}
        Demand: {career_info.get('demand')}
        
        Make it motivating and include why this career is in demand."""
        
        message = await self.watsonx.generate_text(prompt)
        self._add_reasoning_step("Watsonx generated career explanation")
        
        return {
            "message": message,
            "type": "career_exploration",
            "career": career_name,
            "recommendation": career_info
        }
    
    async def _handle_career_recommendation(self) -> Dict[str, Any]:
        """Handle career recommendations"""
        self.context.set_state("recommending")
        self._add_reasoning_step("Career recommendation handler activated")
        
        profile = self.context.get_user_profile()
        
        # Check if profile is complete
        if not profile.get('skills') or not profile.get('interests'):
            return {
                "message": "I need more information to recommend careers. Please tell me about your skills and interests first.",
                "type": "career_recommendation",
                "action": "need_profile"
            }
        
        # Get recommendations
        recommendations = self.tools.recommend_careers(
            profile.get('skills', []),
            profile.get('interests', [])
        )
        self._add_reasoning_step(f"Generated {len(recommendations)} recommendations")
        
        if not recommendations:
            return {
                "message": "Based on your profile, I couldn't find specific matches. Let's explore different career paths together!",
                "type": "career_recommendation"
            }
        
        # Generate message using Watsonx
        prompt = f"""Create an encouraging message recommending these careers to someone based on their skills and interests:
        
        Recommendations:
        {json.dumps(recommendations, indent=2)}
        
        For each, briefly explain why it's a good match and what the salary range is."""
        
        message = await self.watsonx.generate_text(prompt)
        self._add_reasoning_step("Watsonx generated recommendations message")
        
        # Track recommendation
        self.context.add_recommendation("career_recommendations", {
            "count": len(recommendations),
            "top_match": recommendations[0] if recommendations else None
        })
        
        return {
            "message": message,
            "type": "career_recommendation",
            "recommendations": recommendations,
            "recommendation": {"type": "careers", "data": recommendations}
        }
    
    async def _handle_learning_path(self, user_input: str) -> Dict[str, Any]:
        """Handle learning path generation"""
        self.context.set_state("teaching")
        self._add_reasoning_step("Learning path handler activated")
        
        profile = self.context.get_user_profile()
        career = self.context.get_career_focus()
        
        if not career:
            return {
                "message": "Which career would you like to learn more about? Tell me the career name, and I'll create a personalized learning path for you.",
                "type": "learning_path",
                "action": "need_career_focus"
            }
        
        # Determine user level
        user_level = self._determine_user_level(profile)
        self._add_reasoning_step(f"User level determined: {user_level}")
        
        # Generate roadmap
        roadmap = self.tools.generate_learning_roadmap(career, user_level)
        self._add_reasoning_step(f"Generated {user_level} level roadmap")
        
        # Get projects
        projects = self.tools.get_projects(career, user_level)
        
        # Get certifications
        certs = self.tools.get_certifications(career)
        
        # Generate response using Watsonx
        prompt = f"""Create a motivating learning roadmap for someone wanting to become a {career}:
        
        Current Level: {user_level}
        Roadmap: {roadmap.get('roadmap')}
        Timeline: {json.dumps(roadmap.get('timeline'), indent=2)}
        
        Include practical tips and why each phase is important."""
        
        message = await self.watsonx.generate_text(prompt)
        self._add_reasoning_step("Watsonx generated learning path")
        
        return {
            "message": message,
            "type": "learning_path",
            "career": career,
            "roadmap": roadmap,
            "projects": projects,
            "certifications": certs,
            "recommendation": {"type": "learning_path", "data": roadmap}
        }
    
    async def _handle_skill_assessment(self) -> Dict[str, Any]:
        """Handle skill gap assessment"""
        self.context.set_state("analyzing")
        self._add_reasoning_step("Skill assessment handler activated")
        
        profile = self.context.get_user_profile()
        career = self.context.get_career_focus()
        
        if not career:
            return {
                "message": "Please tell me which career you're interested in, and I'll analyze your skill gaps.",
                "type": "skill_assessment",
                "action": "need_career_focus"
            }
        
        # Calculate skill gap
        gap = self.tools.calculate_skill_gap(
            profile.get('skills', []),
            career
        )
        self._add_reasoning_step(f"Skill gap: {gap.get('coverage_percentage')}%")
        
        # Get skill recommendations
        skill_recs = self.tools.recommend_skills(
            career,
            profile.get('skills', [])
        )
        self._add_reasoning_step(f"Recommended {len(skill_recs.get('priority_skills', []))} priority skills")
        
        # Generate response using Watsonx
        prompt = f"""Analyze this skill gap and provide encouraging guidance:
        
        Current Skills: {', '.join(profile.get('skills', []))}
        Target Career: {career}
        Skill Coverage: {gap.get('coverage_percentage')}%
        Existing Skills: {', '.join(gap.get('existing_skills', []))}
        Missing Skills: {', '.join(gap.get('missing_skills', []))}
        
        Provide a motivating assessment and prioritize what to learn first."""
        
        message = await self.watsonx.generate_text(prompt)
        self._add_reasoning_step("Watsonx generated skill assessment")
        
        return {
            "message": message,
            "type": "skill_assessment",
            "skill_gap": gap,
            "recommendations": skill_recs,
            "recommendation": {"type": "skill_gap", "data": gap}
        }
    
    async def _handle_interview_prep(self) -> Dict[str, Any]:
        """Handle interview preparation"""
        self.context.set_state("teaching")
        self._add_reasoning_step("Interview prep handler activated")
        
        career = self.context.get_career_focus()
        
        if not career:
            return {
                "message": "Which position would you like to interview for? Tell me the career/role.",
                "type": "interview_prep",
                "action": "need_career_focus"
            }
        
        # Get interview prep materials
        prep = self.tools.get_interview_prep(career)
        self._add_reasoning_step(f"Retrieved interview prep for {career}")
        
        # Generate response using Watsonx
        prompt = f"""Create an interview preparation guide for a {career} position:
        
        Technical Topics: {json.dumps(prep.get('technical'), indent=2)}
        Behavioral Questions: {json.dumps(prep.get('behavioral')[:5], indent=2)}
        Preparation Strategy: {json.dumps(prep.get('preparation_strategy')[:5], indent=2)}
        
        Provide practical tips, what to study, and sample questions with tips for answering."""
        
        message = await self.watsonx.generate_text(prompt)
        self._add_reasoning_step("Watsonx generated interview guidance")
        
        return {
            "message": message,
            "type": "interview_prep",
            "career": career,
            "prep_materials": prep,
            "recommendation": {"type": "interview_prep", "data": prep}
        }
    
    async def _handle_general_guidance(self, user_input: str) -> Dict[str, Any]:
        """Handle general guidance queries"""
        self.context.set_state("teaching")
        self._add_reasoning_step("General guidance handler activated")
        
        # Get resources
        resources = self.tools.get_learning_resources()
        self._add_reasoning_step("Retrieved learning resources")
        
        # Use Watsonx for personalized response
        profile = self.context.get_user_profile()
        prompt = f"""Answer this career-related question helpfully and motivatingly:
        
        Question: {user_input}
        User Profile: {json.dumps(profile, indent=2)}
        Available Resources: {json.dumps(resources, indent=2)}
        
        Provide specific, actionable advice."""
        
        message = await self.watsonx.generate_text(prompt)
        self._add_reasoning_step("Watsonx generated guidance")
        
        return {
            "message": message,
            "type": "general_guidance",
            "resources": resources
        }
    
    async def _handle_unknown_intent(self, user_input: str) -> Dict[str, Any]:
        """Handle unknown intents"""
        self._add_reasoning_step("Unknown intent detected")
        
        # Use Watsonx to understand and respond
        prompt = f"""A user asked a career-related question. Respond helpfully:
        
        Question: {user_input}
        
        If it's not career-related, politely redirect. If it is, provide helpful guidance."""
        
        message = await self.watsonx.generate_text(prompt)
        self._add_reasoning_step("Watsonx interpreted unknown intent")
        
        return {
            "message": message,
            "type": "general_guidance"
        }
    
    # ============ HELPER METHODS ============
    
    def _determine_user_level(self, profile: Dict[str, Any]) -> str:
        """Determine user's experience level"""
        skills_count = len(profile.get('skills', []))
        
        if skills_count >= 5:
            return "advanced"
        elif skills_count >= 2:
            return "intermediate"
        else:
            return "beginner"
    
    def _add_reasoning_step(self, step: str) -> None:
        """Add reasoning step for transparency"""
        self.reasoning_steps.append(step)
        logger.debug(f"Reasoning: {step}")
    
    def get_reasoning_steps(self) -> List[str]:
        """Get all reasoning steps from last interaction"""
        return self.reasoning_steps
    
    async def get_session_summary(self) -> Dict[str, Any]:
        """Get summary of agent session"""
        summary = self.context.generate_session_summary()
        logger.info(f"Session summary: {summary}")
        return summary
