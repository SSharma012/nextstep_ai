import logging
from typing import Dict, Any, Optional, List
import os

logger = logging.getLogger(__name__)

try:
    from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
    from ibm_watsonx_ai.foundation_models import ModelInference
    IBM_AVAILABLE = True
except ImportError:
    IBM_AVAILABLE = False
    logger.warning("⚠️ IBM SDK not available - using mock mode")

class WatsonxClient:
    """IBM Watsonx AI Client"""
    
    def __init__(self, api_key: str, project_id: str, space_id: str, 
                 url: str = "https://us-south.ml.cloud.ibm.com"):
        self.api_key = api_key
        self.project_id = project_id
        self.space_id = space_id
        self.url = url
        self.model_name = "ibm/granite-13b-chat-v2"
        self.mock_mode = False
        
        if IBM_AVAILABLE:
            try:
                self.authenticator = IAMAuthenticator(apikey=api_key)
                self.model = ModelInference(
                    model_id=self.model_name,
                    credentials=self.authenticator,
                    project_id=project_id,
                    space_id=space_id,
                    url=url
                )
                logger.info("✅ Connected to IBM Watsonx!")
            except Exception as e:
                logger.error(f"❌ IBM Connection Error: {str(e)}")
                self.mock_mode = True
        else:
            logger.warning("⚠️ IBM SDK not available - using mock mode")
            self.mock_mode = True
    
    def generate_response(self, prompt: str, max_tokens: int = 500, 
                         temperature: float = 0.7) -> Dict[str, Any]:
        """Generate response from Granite model"""
        
        if self.mock_mode:
            return self._generate_mock_response(prompt)
        
        try:
            response = self.model.generate(
                prompt=prompt,
                params={
                    "max_new_tokens": max_tokens,
                    "temperature": temperature,
                    "top_p": 0.9,
                }
            )
            
            if response and len(response["results"]) > 0:
                generated_text = response["results"][0]["generated_text"].strip()
                return {
                    "success": True,
                    "response": generated_text
                }
            else:
                return {"success": False, "response": "No response generated"}
                
        except Exception as e:
            logger.error(f"❌ Generation Error: {str(e)}")
            return {"success": False, "response": f"Error: {str(e)}"}
    
    def _generate_mock_response(self, prompt: str) -> Dict[str, Any]:
        """Generate mock response for testing"""
        
        prompt_lower = prompt.lower()
        
        if "data scientist" in prompt_lower:
            return {
                "success": True,
                "response": """A Data Scientist is a great choice! Here's your personalized guidance:

🎯 **Why Data Scientist?**
- Extract insights from data using ML and statistics
- Build predictive models that solve real problems
- High salary and job security
- Remote work opportunities

📊 **Your 6-Month Roadmap:**

**Month 1-2: Python Mastery**
- Python basics, data types, functions
- Libraries: NumPy, Pandas
- Time: 4-5 hours/week
- Project: Build a data cleaning tool

**Month 2-3: SQL & Databases**
- SQL queries, joins, aggregations
- PostgreSQL or MySQL
- Time: 3-4 hours/week
- Project: Create SQL queries for real datasets

**Month 3-4: Machine Learning**
- Supervised learning (regression, classification)
- Unsupervised learning (clustering)
- scikit-learn library
- Time: 5-6 hours/week
- Project: Build predictive model

**Month 4-5: Advanced Topics**
- Deep learning basics
- Neural networks with TensorFlow
- Model deployment
- Time: 5-6 hours/week
- Project: Deploy ML model to cloud

**Month 5-6: Portfolio & Certification**
- Build 2 strong portfolio projects
- Google Cloud or AWS certification
- Interview preparation
- Time: 4-5 hours/week

💼 **Skills to Learn:**
1. Python (Critical) ⭐⭐⭐
2. SQL (Critical) ⭐⭐⭐
3. Statistics (Important) ⭐⭐⭐
4. Machine Learning (Important) ⭐⭐⭐
5. Data Visualization (Important) ⭐⭐

💻 **Free Resources:**
- Kaggle Learn (free courses)
- YouTube: StatQuest with Josh Starmer
- Coursera (audit free): Google Data Analytics
- Real Python tutorials
- Fast.ai (practical deep learning)

🏆 **Certifications (Pick One):**
- Google Cloud Professional Data Engineer
- IBM Data Science Professional Certificate
- AWS Machine Learning Specialty

💰 **Expected Salary:**
- Entry Level: $70k - $90k
- Mid Level: $90k - $130k
- Senior: $130k - $180k+

✨ **Pro Tips:**
1. Start with Python today
2. Build projects on GitHub
3. Participate in Kaggle competitions
4. Network on LinkedIn
5. Read research papers (arXiv.org)

Ready to start? Begin with Python fundamentals this week!"""
            }
        
        elif "career" in prompt_lower or "recommend" in prompt_lower:
            return {
                "success": True,
                "response": """🎯 **Top Career Paths for You (2024-2025):**

**🥇 TIER 1 - Highest Demand & Salary:**

1. **AI/ML Engineer**
   - Salary: $100k - $200k+
   - Demand: ⭐⭐⭐⭐⭐ CRITICAL
   - Growth: 50%+ annually
   - Skills: Python, TensorFlow, LLMs, RAG
   - Companies: Google, Meta, OpenAI, IBM

2. **Cloud Architect**
   - Salary: $120k - $220k+
   - Demand: ⭐⭐⭐⭐⭐ CRITICAL
   - Growth: 30%+ annually
   - Skills: AWS/Azure/GCP, DevOps, Kubernetes
   - Companies: AWS, Microsoft, Google

3. **Data Scientist**
   - Salary: $90k - $160k+
   - Demand: ⭐⭐⭐⭐ Very High
   - Growth: 37% (2021-2031)
   - Skills: Python, SQL, ML, Statistics
   - Companies: Google, Amazon, Microsoft

**🥈 TIER 2 - Good Demand & Salary:**

4. **Full Stack Developer**
   - Salary: $80k - $140k+
   - Demand: ⭐⭐⭐⭐ High
   - Growth: 15%+
   - Skills: React, Node.js, SQL, Docker

5. **DevOps Engineer**
   - Salary: $100k - $170k+
   - Demand: ⭐⭐⭐⭐ High
   - Growth: 25%+
   - Skills: Docker, Kubernetes, CI/CD, Cloud

6. **Cybersecurity Specialist**
   - Salary: $100k - $180k+
   - Demand: ⭐⭐⭐⭐⭐ Critical
   - Growth: 35%+
   - Skills: Penetration Testing, Security, Compliance

**📊 Market Analysis:**
- AI/ML: Highest growth & salary
- Cloud: Stable high demand
- Data Science: Consistent growth
- Security: Critical need

**💡 My Recommendation:**
If you're starting: **Begin with Data Science or Python Development**
If you want highest salary: **Aim for AI/ML Engineer or Cloud Architect**
If you want job security: **Go for Cybersecurity**

What interests you most? I can create a personalized learning path!"""
            }
        
        elif "skill" in prompt_lower or "learn" in prompt_lower:
            return {
                "success": True,
                "response": """📚 **Your Personalized Learning Path:**

**🔴 CRITICAL SKILLS (Learn First):**

1. **Python Programming** ⭐⭐⭐
   - Why: Used in AI, Data Science, Web Dev
   - Time: 2-3 months
   - Resources: Real Python, Codecademy, YouTube
   - Project: Build a web scraper

2. **SQL & Databases** ⭐⭐⭐
   - Why: Every job needs database knowledge
   - Time: 1-2 months
   - Resources: Mode Analytics SQL Tutorial, LeetCode
   - Project: Write complex SQL queries

3. **Git & GitHub** ⭐⭐⭐
   - Why: Essential for team work
   - Time: 1 week
   - Resources: GitHub Learning Lab
   - Project: Create your first repo

**🟠 IMPORTANT SKILLS (Learn Next):**

4. **Data Structures & Algorithms**
   - Time: 2 months
   - Resources: LeetCode, HackerRank
   - Practice: 50+ problems

5. **Web Development Basics**
   - HTML, CSS, JavaScript
   - Time: 2-3 months
   - Resources: freeCodeCamp YouTube
   - Project: Build a portfolio website

6. **Machine Learning Basics**
   - Time: 3 months
   - Resources: Andrew Ng's ML course
   - Project: Build predictive model

**🟢 ADVANCED SKILLS (After Basics):**

7. **Cloud Platforms**
   - AWS / Azure / GCP
   - Time: 2-3 months
   - Get certified
   - Project: Deploy app to cloud

8. **System Design**
   - Time: 2 months
   - Resources: System Design Interview
   - Practice: Design Twitter, Uber, etc.

9. **LLMs & AI (Latest)**
   - ChatGPT, Prompt Engineering, RAG
   - Time: 1-2 months
   - Resources: OpenAI docs, YouTube
   - Project: Build AI app

**📅 Recommended Timeline (12 Months):**
- Month 1-3: Python + SQL + Git
- Month 4-6: Data Structures + Web Dev
- Month 7-9: Machine Learning + Cloud
- Month 10-12: Specialization + Internship search

**🎯 This Week's Action:**
1. Install Python today
2. Start one tutorial
3. Write your first Python program
4. Commit to GitHub

Which skill interests you most? I'll create a detailed learning plan!"""
            }
        
        elif "interview" in prompt_lower or "placement" in prompt_lower:
            return {
                "success": True,
                "response": """💼 **Your Complete Placement Preparation Plan (3 Months):**

**MONTH 1: Technical Foundation (Weeks 1-4)**

Week 1-2: Data Structures
- Arrays, Linked Lists, Stacks, Queues
- Study: 2 hours/day
- Practice: 10 problems/day on LeetCode Easy
- Resource: LeetCode Explore

Week 3-4: Algorithms & Sorting
- Binary Search, Sorting, Two Pointers
- Study: 2 hours/day
- Practice: 10 problems/day on LeetCode
- Resource: YouTube - TakeYouForward channel

**MONTH 2: Problem Solving (Weeks 5-8)**

Week 5-6: Medium Level Problems
- Dynamic Programming basics
- Graphs, Trees, Backtracking
- Practice: 15 problems/day
- Target: Solve 50 medium problems

Week 7-8: Hard Level + System Design
- Complex problem solving
- Introduction to system design
- Practice: 5 hard problems + 2 design problems/day

**MONTH 3: Final Prep (Weeks 9-12)**

Week 9-10: Company-Specific Questions
- Check company's question patterns
- Solve 20-30 company-specific problems
- Practice: 2 hours/day

Week 11-12: Mock Interviews
- Do 10+ mock interviews
- Practice with friends or InterviewBit
- Record and review yourself
- Work on communication

**📋 Daily Schedule (3 hours):**
- 8:00-8:30 AM: Watch concept videos (30 mins)
- 8:30-9:30 AM: Solve 3-4 problems (60 mins)
- 9:30-10:00 AM: Review & learn from solutions (30 mins)
- Evening: 1-2 more problems or mock interview

**🎯 Weekly Goals:**
- Week 1-4: Solve 70 problems
- Week 5-8: Solve 100 problems
- Week 9-12: 10 mock interviews + company prep

**📚 Best Resources:**
- LeetCode Premium ($159/year)
- InterviewBit (free)
- GeeksforGeeks (free)
- YouTube: Tech Interview channels
- Blind (read experiences)

**💻 Recommended Problems Count:**
- Easy: 50 problems
- Medium: 100 problems
- Hard: 20 problems
- Total: 170 problems minimum

**🎤 Soft Skills & Communication:**
- Speak while solving (think aloud)
- Explain your approach
- Ask clarifying questions
- Discuss trade-offs
- Write clean code

**📋 Resume Tips:**
- Highlight 3-5 best projects
- Show real impact (numbers matter)
- Link to GitHub projects
- Include certifications
- Keep it to 1 page

**🔗 LinkedIn Profile:**
- Professional photo
- Clear headline
- 500+ connections
- Endorsements for skills
- Post or comment regularly

**🎯 Application Strategy:**
- Apply to 20+ companies
- Target 50% fit, 30% reach, 20% dream
- Customize cover letter
- Follow up after 2 weeks
- Network on LinkedIn

**✨ Pro Tips:**
1. Start coding TODAY
2. Consistency > Intensity
3. Review mistakes
4. Practice out loud
5. Get feedback from mentors
6. Sleep 7-8 hours daily
7. Exercise 30 mins/day (boosts brain)

**Expected Timeline:**
- Month 1: Build foundation (50 problems)
- Month 2: Build confidence (100 problems)
- Month 3: Ready for interviews (70 problems + mocks)

Start with LeetCode Easy problems today. You've got this! 💪"""
            }
        
        else:
            return {
                "success": True,
                "response": f"""Hello! I'm NexrStep AI, your career counselor! 🎯

I can help you with:
- 💼 Career recommendations
- 📚 Skill development plans
- 🏆 Certification guidance
- 💬 Interview preparation
- 🗺️ Learning roadmaps
- 🔍 Job search strategies

Your question: "{prompt[:100]}"

Try asking me:
- "What career is best for me?"
- "What skills should I learn?"
- "How do I prepare for interviews?"
- "What's the best way to learn Python?"
- "Which certifications matter?"

Let's get started! 🚀"""
            }
    
    def chat(self, messages: List[Dict], max_tokens: int = 500, 
             temperature: float = 0.7) -> Dict[str, Any]:
        """Chat mode (not implemented yet)"""
        if messages:
            last_msg = messages[-1].get("content", "")
            return self.generate_response(last_msg, max_tokens, temperature)
        
        return {"success": False, "response": "No message"}

def get_watsonx_client() -> Optional[WatsonxClient]:
    """Initialize Watsonx client from environment"""
    try:
        api_key = os.getenv("IBM_CLOUD_API_KEY", "")
        project_id = os.getenv("IBM_PROJECT_ID", "")
        space_id = os.getenv("IBM_SPACE_ID", "")
        url = os.getenv("IBM_WATSONX_URL", "https://us-south.ml.cloud.ibm.com")
        
        if not api_key or not project_id or not space_id:
            logger.warning("⚠️ IBM credentials not found - using mock mode")
        
        client = WatsonxClient(
            api_key=api_key or "mock",
            project_id=project_id or "mock",
            space_id=space_id or "mock",
            url=url
        )
        return client
    except Exception as e:
        logger.error(f"❌ Failed to initialize: {str(e)}")
        return None