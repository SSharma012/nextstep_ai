# NextStep AI - Intelligent Career Counselor

🎯 **An AI-powered career counselor that provides personalized guidance, career recommendations, and learning paths using IBM Watsonx and advanced RAG (Retrieval-Augmented Generation).**

---

## 📋 Features

### 🤖 Intelligent Agent System
- **Multi-step Reasoning**: Agent analyzes user input through multiple decision steps
- **Context-Aware**: Maintains conversation context and user profile
- **Smart Intent Detection**: Understands user intent and routes appropriately
- **Transparent Reasoning**: Shows all reasoning steps for transparency

### 💼 Career Services
- **Career Exploration**: Explore 8+ different career paths
- **Career Recommendations**: Get personalized career suggestions based on skills and interests
- **Skill Gap Analysis**: Identify missing skills for target careers
- **Learning Roadmaps**: Get 3-6 month personalized learning paths
- **Interview Preparation**: Get interview materials and preparation strategy
- **Project Recommendations**: Get beginner to advanced projects
- **Certification Guidance**: Learn about relevant certifications

### 📚 Knowledge Base
- **8 Career Profiles**: Data Scientist, ML Engineer, AI Engineer, Cloud Architect, DevOps Engineer, Full Stack Developer, Frontend Developer, Backend Developer
- **50+ Skills**: Detailed information on required skills with learning resources
- **4 Certifications**: Relevant industry certifications
- **100+ Learning Resources**: Platforms, coding practice sites, communities
- **40+ Projects**: Beginner, intermediate, and advanced projects
- **Interview Prep**: Technical and behavioral interview materials

### 🗄️ Persistent Storage
- **User Profiles**: Store education, skills, interests, goals
- **Chat History**: Maintain conversation history
- **Recommendations**: Track all recommendations given
- **MySQL Database**: Secure data storage

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    User Interface (Flask)                    │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                    Career Agent (Agentic AI)                 │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ Step 1: Intent Detection                             │   │
│  │ Step 2: Context Loading                              │   │
│  │ Step 3: Route to Handler                             │   │
│  │ Step 4: Execute Handler                              │   │
│  │ Step 5: Generate Response (Watsonx)                  │   │
│  │ Step 6: Save to Database                             │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
        ↓                       ↓                      ↓
    ┌───────┐           ┌──────────────┐        ┌──────────┐
    │ Tools │           │ Context Mgr  │        │ Watsonx  │
    └───────┘           └──────────────┘        └──────────┘
        ↓
    ┌─────────────────────────────────────┐
    │  Knowledge Base (Careers, Skills)   │
    └─────────────────────────────────────┘
        ↓
    ┌─────────────────────────────────────┐
    │     MySQL Database                  │
    │  (Users, Profiles, Chat History)    │
    └─────────────────────────────────────┘
```

---

## 📦 Installation

### Prerequisites
- Python 3.8+
- MySQL Server
- IBM Watsonx API Key
- Git

### Step 1: Clone Repository
```bash
git clone https://github.com/SSharma012/nextstep_ai.git
cd nextstep_ai
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment
```bash
cp .env.example .env
# Edit .env with your configuration
```

### Step 5: Setup Database
```bash
mysql -u root -p

CREATE DATABASE nextstep_ai;
USE nextstep_ai;

# The app will create tables automatically on first run
```

### Step 6: Run Application
```bash
python app.py
```

Application will be available at `http://localhost:5000`

---

## 🚀 Usage

### 1. User Registration
```bash
POST /api/auth/register
Content-Type: application/json

{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "secure_password",
  "full_name": "John Doe"
}
```

### 2. User Login
```bash
POST /api/auth/login
Content-Type: application/json

{
  "username": "john_doe",
  "password": "secure_password"
}
```

### 3. Start Chat with Agent
```bash
POST /api/chat
Content-Type: application/json
Authorization: Bearer <token>

{
  "user_id": 1,
  "message": "I'm interested in becoming a data scientist. Can you help?"
}
```

### 4. Get Career Recommendations
```bash
GET /api/careers/recommendations
Authorization: Bearer <token>

Query Parameters:
- user_id: User ID
```

### 5. Get Learning Path
```bash
GET /api/learning/roadmap
Authorization: Bearer <token>

Query Parameters:
- user_id: User ID
- career: Target career name
```

---

## 🧠 Agent Reasoning Example

**User Input:** "I know Python, SQL, and statistics. I'm interested in data analysis and AI. What should I do?"

**Agent Reasoning Steps:**
1. ✅ Intent parsed: career_recommendation
2. ✅ Context loaded: user has 0 profile fields
3. ✅ Profile setup handler activated
4. ✅ Watsonx extracted: education level, skills (Python, SQL, Statistics), interests (data analysis, AI), goal (not specified)
5. ✅ Profile updated in database
6. ✅ Career focus set to: Data Scientist
7. ✅ Generated 3 career recommendations
8. ✅ Watsonx generated recommendations message
9. ✅ Recommendation tracked: career_recommendations

**Agent Response:**
"Based on your skills and interests, I recommend three careers:

1. **Data Scientist** (95% match) - Your Python, SQL, and statistics skills are perfect for this role. Average salary: $100,000-$150,000

2. **Machine Learning Engineer** (85% match) - You have foundational skills. You'll need to learn more about ML frameworks.

3. **AI Engineer** (80% match) - With your current skills, you can start learning LLMs and RAG concepts.

Would you like me to create a learning roadmap for any of these?"

---

## 📁 Project Structure

```
nextstep_ai/
├── src/
│   ├── __init__.py
│   ├── database/
│   │   ├── __init__.py
│   │   └── db.py                 # Database management
│   ├── api/
│   │   ├── __init__.py
│   │   └── watsonx_client.py     # Watsonx API client
│   ├── rag/
│   │   ├── __init__.py
│   │   └── knowledge_base.py     # Knowledge base with 8 careers
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── tools.py              # Agent tools (20+ functions)
│   │   ├── career_agent.py       # Main agentic AI
│   │   └── context_manager.py    # Conversation context
│   └── memory/
│       ├── __init__.py
│       └── context_manager.py    # Memory management
├── data/
│   └── knowledge_base/           # KB JSON files
├── app.py                         # Flask application
├── constants.py                   # Constants
├── settings.py                    # Configuration
├── requirements.txt               # Dependencies
├── .env.example                   # Environment template
├── .gitignore                     # Git ignore
└── README.md                      # This file
```

---

## 🔑 Key Components

### Agent Tools (`src/agents/tools.py`)
- 20+ tools for career analysis, recommendations, learning paths
- Tools for skill gap analysis, interview prep, resources
- Database integration for saving recommendations

### Career Agent (`src/agents/career_agent.py`)
- Multi-step reasoning agent
- Intent detection: profile_setup, career_exploration, career_recommendation, learning_path, skill_assessment, interview_prep, general_guidance
- 7 specialized handlers for different intent types
- Transparent reasoning steps

### Context Manager (`src/agents/context_manager.py`)
- Manages conversation context
- Tracks user profile, recommendations, session state
- Decision logic for agent (e.g., should_ask_for_profile, should_recommend_careers)

### Knowledge Base (`src/rag/knowledge_base.py`)
- 8 detailed career profiles
- 50+ skills with learning resources
- 4 industry certifications
- 100+ learning resources
- 40+ recommended projects
- Interview preparation materials

---

## 🎓 Supported Careers

1. **Data Scientist** - Extract insights from data using ML and statistics
2. **ML Engineer** - Build and deploy ML models
3. **AI Engineer** - Develop AI solutions using LLMs
4. **Cloud Architect** - Design and manage cloud infrastructure
5. **DevOps Engineer** - Automate deployment and infrastructure
6. **Full Stack Developer** - Build complete web applications
7. **Frontend Developer** - Build user interfaces
8. **Backend Developer** - Build server-side logic and APIs

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

MIT License - see LICENSE file for details

---

## 👥 Authors

- **Saksham Sharma** - Initial work - [@SSharma012](https://github.com/SSharma012)

---

## 📞 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Email: support@nextstep-ai.com
- Documentation: [Full Docs](https://docs.nextstep-ai.com)

---

## 🗺️ Roadmap

- [ ] Add more careers (50+)
- [ ] Implement video tutorials integration
- [ ] Add AI mock interview feature
- [ ] Implement portfolio building guide
- [ ] Add job market insights
- [ ] Implement progress tracking
- [ ] Add mobile app
- [ ] Implement peer mentoring feature

---

## 📊 Statistics

- **8** Career Paths
- **50+** Skills
- **4** Certifications
- **100+** Learning Resources
- **40+** Projects
- **7** Agent Intent Types
- **20+** Agent Tools

---

**Made with ❤️ for career seekers and learners**
