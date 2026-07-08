import streamlit as st
import sys
from pathlib import Path
import os
from dotenv import load_dotenv

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.database.db import Database
from src.api.watsonx_client import get_watsonx_client
from src.rag.knowledge_base import KnowledgeBase
from src.agents.career_agent import CareerAgent

load_dotenv()

# Page config
st.set_page_config(
    page_title="NextStep AI - Career Counselor",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS Styling
st.markdown("""
<style>
    * { margin: 0; padding: 0; }
    body { 
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .main { 
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        color: white;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea, #764ba2) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 12px 24px !important;
        font-weight: 600 !important;
        transition: all 0.3s !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3) !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.5) !important;
    }
    
    /* Input fields */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select {
        background: rgba(255, 255, 255, 0.1) !important;
        color: white !important;
        border: 1px solid rgba(102, 126, 234, 0.3) !important;
        border-radius: 8px !important;
    }
    
    /* Headings */
    h1 {
        background: linear-gradient(135deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.5rem !important;
    }
    
    h2 {
        color: #667eea !important;
        font-size: 2rem !important;
    }
    
    h3 {
        color: #764ba2 !important;
    }
    
    /* Cards */
    .metric-card {
        background: rgba(102, 126, 234, 0.1);
        border: 1px solid rgba(102, 126, 234, 0.3);
        border-radius: 15px;
        padding: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Database connection
@st.cache_resource
def init_db():
    db = Database(
        host=os.getenv('MYSQL_HOST', 'localhost'),
        user=os.getenv('MYSQL_USER', 'root'),
        password=os.getenv('MYSQL_PASSWORD', ''),
        database=os.getenv('MYSQL_DATABASE', 'nextstep_ai')
    )
    if db.connect():
        db.create_tables()
        return db
    return None

# Initialize AI
@st.cache_resource
def init_ai():
    try:
        client = get_watsonx_client()
        kb = KnowledgeBase()
        agent = CareerAgent(client, kb)
        return agent
    except:
        return None

# Session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user' not in st.session_state:
    st.session_state.user = None
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'db' not in st.session_state:
    st.session_state.db = init_db()
if 'agent' not in st.session_state:
    st.session_state.agent = init_ai()
if 'messages' not in st.session_state:
    st.session_state.messages = []

# ============ LOGIN/REGISTER PAGES ============

def login_page():
    st.markdown("<h1 style='text-align: center;'>🚀 NextStep AI</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 1.2rem; color: rgba(255,255,255,0.7);'>Your Intelligent Career Counselor</p>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<h2 style='text-align: center;'>Login</h2>", unsafe_allow_html=True)
        
        username = st.text_input("Username", placeholder="Enter username")
        password = st.text_input("Password", type="password", placeholder="Enter password")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🔓 Login", use_container_width=True):
                if username and password:
                    user = st.session_state.db.login_user(username, password)
                    if user:
                        st.session_state.logged_in = True
                        st.session_state.user = user
                        st.success(f"Welcome back, {user['full_name']}! 🎉")
                        st.rerun()
                    else:
                        st.error("❌ Invalid username or password!")
                else:
                    st.warning("⚠️ Please fill all fields")
        
        with col2:
            if st.button("📝 Register", use_container_width=True):
                st.session_state.page = 'register'
                st.rerun()
        
        st.markdown("""
        <div style='text-align: center; margin-top: 2rem; color: rgba(255,255,255,0.6);'>
            <p>Demo Credentials:</p>
            <p>Username: <strong>demo</strong></p>
            <p>Password: <strong>demo123</strong></p>
        </div>
        """, unsafe_allow_html=True)

def register_page():
    st.markdown("<h1 style='text-align: center;'>🚀 NextStep AI</h1>", unsafe_allow_html=True)
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<h2 style='text-align: center;'>Create Account</h2>", unsafe_allow_html=True)
        
        full_name = st.text_input("Full Name", placeholder="Enter your full name")
        email = st.text_input("Email", placeholder="Enter email")
        username = st.text_input("Username", placeholder="Choose username")
        password = st.text_input("Password", type="password", placeholder="Create password")
        confirm_pass = st.text_input("Confirm Password", type="password", placeholder="Confirm password")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("✅ Register", use_container_width=True):
                if full_name and email and username and password and confirm_pass:
                    if password != confirm_pass:
                        st.error("❌ Passwords don't match!")
                    elif st.session_state.db.user_exists(username, email):
                        st.error("❌ Username or email already exists!")
                    else:
                        if st.session_state.db.register_user(username, email, password, full_name):
                            st.success("✅ Account created! Please login.")
                            st.session_state.page = 'login'
                            st.rerun()
                        else:
                            st.error("❌ Registration failed!")
                else:
                    st.warning("⚠️ Please fill all fields")
        
        with col2:
            if st.button("🔙 Back to Login", use_container_width=True):
                st.session_state.page = 'login'
                st.rerun()

# ============ MAIN APP PAGES ============

def navbar():
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    with col1:
        if st.button("🏠 Home", use_container_width=True):
            st.session_state.page = 'home'
            st.rerun()
    with col2:
        if st.button("👤 Profile", use_container_width=True):
            st.session_state.page = 'profile'
            st.rerun()
    with col3:
        if st.button("💬 Chat", use_container_width=True):
            st.session_state.page = 'chat'
            st.rerun()
    with col4:
        if st.button("📊 Dashboard", use_container_width=True):
            st.session_state.page = 'dashboard'
            st.rerun()
    with col5:
        if st.button("📚 History", use_container_width=True):
            st.session_state.page = 'history'
            st.rerun()
    with col6:
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.user = None
            st.session_state.page = 'home'
            st.rerun()

def home_page():
    st.markdown(f"""
    <div style='text-align: center; padding: 3rem 0;'>
        <h1>Welcome, {st.session_state.user['full_name']}! 👋</h1>
        <p style='font-size: 1.2rem; color: rgba(255,255,255,0.8);'>Your Intelligent Career Counselor</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.info("🤖 Get personalized career recommendations from AI")
    with col2:
        st.info("📚 Create custom learning paths for your goals")
    
    col1, col2 = st.columns(2)
    with col1:
        st.info("💼 Prepare for job interviews with AI coaching")
    with col2:
        st.info("📈 Track your progress and growth")

def profile_page():
    st.markdown("<h2>👤 Your Profile</h2>", unsafe_allow_html=True)
    
    profile = st.session_state.db.get_profile(st.session_state.user['id'])
    
    col1, col2 = st.columns(2)
    
    with col1:
        education = st.selectbox("Education Level", ["", "12th Pass", "Bachelor's", "Master's", "Diploma"], 
                                 index=0 if not profile or not profile['education'] else ["", "12th Pass", "Bachelor's", "Master's", "Diploma"].index(profile['education']))
    
    with col2:
        goal = st.text_input("Career Goal", value=profile['goal'] if profile and profile['goal'] else "")
    
    st.markdown("<h3>Your Skills</h3>", unsafe_allow_html=True)
    
    skill_list = ["Python", "ML", "Data Analysis", "AWS", "Docker", "React", "JavaScript", "SQL", "Git", "TensorFlow"]
    current_skills = profile['skills'] if profile and profile['skills'] else []
    
    skills = []
    col1, col2, col3 = st.columns(3)
    
    for i, skill in enumerate(skill_list):
        col = [col1, col2, col3][i % 3]
        with col:
            if st.checkbox(skill, value=skill in current_skills):
                skills.append(skill)
    
    st.markdown("<h3>Your Interests</h3>", unsafe_allow_html=True)
    
    current_interests = profile['interests'] if profile and profile['interests'] else []
    interests = st.multiselect("Select interests:", ["AI/ML", "Data Science", "Web Dev", "Cloud", "Cybersecurity", "DevOps"], default=current_interests)
    
    if st.button("💾 Save Profile", use_container_width=True):
        if st.session_state.db.save_profile(st.session_state.user['id'], education, skills, interests, goal):
            st.success("✅ Profile saved!")
            st.balloons()
        else:
            st.error("❌ Failed to save profile")

def chat_page():
    st.markdown("<h2>💬 Chat with AI Counselor</h2>", unsafe_allow_html=True)
    
    if not st.session_state.agent:
        st.error("❌ AI not initialized")
        return
    
    # Display chat
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.info(f"**You:** {msg['content']}")
        else:
            st.success(f"**AI:** {msg['content'][:300]}...")
    
    col1, col2 = st.columns([5, 1])
    
    with col1:
        user_input = st.text_input("Ask a question:", placeholder="What career is best for me?")
    
    with col2:
        send = st.button("Send ➤")
    
    if send and user_input:
        with st.spinner("🤔 Thinking..."):
            response = st.session_state.agent.chat(user_input)
        
        if response["success"]:
            st.session_state.messages.append({"role": "user", "content": user_input})
            st.session_state.messages.append({"role": "assistant", "content": response["response"]})
            
            # Save to database
            st.session_state.db.save_chat(st.session_state.user['id'], user_input, response["response"])
            st.rerun()
        else:
            st.error(f"Error: {response['response']}")

def dashboard_page():
    st.markdown("<h2>📊 Your Dashboard</h2>", unsafe_allow_html=True)
    
    profile = st.session_state.db.get_profile(st.session_state.user['id'])
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Profile", "75%")
    with col2:
        st.metric("Skills", len(profile['skills']) if profile and profile['skills'] else 0)
    with col3:
        st.metric("Messages", len(st.session_state.messages))
    with col4:
        st.metric("Progress", "0%")
    
    st.divider()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<h3>📈 Your Skills</h3>", unsafe_allow_html=True)
        if profile and profile['skills']:
            for skill in profile['skills']:
                st.write(f"✅ {skill}")
        else:
            st.info("No skills added yet")
    
    with col2:
        st.markdown("<h3>⭐ Your Interests</h3>", unsafe_allow_html=True)
        if profile and profile['interests']:
            for interest in profile['interests']:
                st.write(f"⭐ {interest}")
        else:
            st.info("No interests added yet")

def history_page():
    st.markdown("<h2>📚 Chat History</h2>", unsafe_allow_html=True)
    
    history = st.session_state.db.get_chat_history(st.session_state.user['id'])
    
    if history:
        for msg, response, created_at in history:
            st.markdown(f"""
            <div style='background: rgba(102, 126, 234, 0.1); padding: 1rem; border-radius: 10px; margin-bottom: 1rem;'>
                <p><strong>You:</strong> {msg}</p>
                <p><strong>AI:</strong> {response[:200]}...</p>
                <p style='color: rgba(255,255,255,0.5); font-size: 0.8rem;'>{created_at}</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No chat history yet")

# ============ MAIN APP LOGIC ============

if not st.session_state.logged_in:
    if st.session_state.page == 'register':
        register_page()
    else:
        login_page()
else:
    st.markdown("<h1 style='text-align: center;'>🚀 NextStep AI</h1>", unsafe_allow_html=True)
    navbar()
    st.divider()
    
    if st.session_state.page == 'home':
        home_page()
    elif st.session_state.page == 'profile':
        profile_page()
    elif st.session_state.page == 'chat':
        chat_page()
    elif st.session_state.page == 'dashboard':
        dashboard_page()
    elif st.session_state.page == 'history':
        history_page()

st.markdown("<p style='text-align: center; color: rgba(255,255,255,0.5); margin-top: 3rem;'>© 2024 NextStep AI | Your Career Counselor</p>", unsafe_allow_html=True)