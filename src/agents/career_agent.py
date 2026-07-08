import logging

logger = logging.getLogger(__name__)

class CareerAgent:
    def __init__(self, watsonx_client, knowledge_base):
        self.client = watsonx_client
        self.kb = knowledge_base
        self.conversation_history = []
        
        self.system_prompt = """You are NexrStep AI, an expert career counselor powered by IBM Watsonx.

Your responsibilities:
1. Understand the user's career goals and interests
2. Recommend suitable career paths
3. Suggest skills to learn
4. Help with placement preparation
5. Motivate and guide students

Always be supportive, encouraging, and provide actionable advice."""
    
    def chat(self, user_message):
        try:
            # Search knowledge base for relevant information
            kb_results = self.kb.search(user_message, limit=2)
            kb_text = self._format_kb_context(kb_results)
            
            # Create the full prompt
            if kb_text:
                full_prompt = f"""{self.system_prompt}

Knowledge Base:
{kb_text}

User Question: {user_message}

Response:"""
            else:
                full_prompt = f"""{self.system_prompt}

User Question: {user_message}

Response:"""
            
            # Get response from Watsonx
            response = self.client.generate_response(full_prompt, max_tokens=500)
            
            if response["success"]:
                # Store in history
                self.conversation_history.append({
                    "role": "user",
                    "message": user_message
                })
                self.conversation_history.append({
                    "role": "assistant",
                    "message": response["response"]
                })
                
                return {
                    "success": True,
                    "response": response["response"]
                }
            else:
                return {
                    "success": False,
                    "response": "Sorry, I couldn't generate a response. Please try again."
                }
        except Exception as e:
            return {
                "success": False,
                "response": f"Error: {str(e)}"
            }
    
    def _format_kb_context(self, kb_results):
        if not kb_results:
            return ""
        
        text = ""
        for i, result in enumerate(kb_results, 1):
            text += f"{i}. {result.get('key', 'Unknown')}: {str(result.get('content', ''))[:150]}\n"
        
        return text
    
    def get_conversation_history(self):
        return self.conversation_history
    
    def clear_history(self):
        self.conversation_history = []