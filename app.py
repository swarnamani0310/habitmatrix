import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os
from PIL import Image
import base64
from database import save_to_sheet, load_from_sheet

# Config
st.set_page_config(page_title="HabitMatrix", layout="wide", page_icon="🧠", initial_sidebar_state="collapsed")
DATA_FILE = "survey_data.csv"
ADMIN_PASSWORD = "admin123"

# Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Animated gradient background */
    .stApp {
        background: linear-gradient(-45deg, #1a1a2e, #16213e, #0f3460, #1a1a2e);
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .main {
        background: transparent;
    }
    
    /* Form Container with glow effect */
    div[data-testid="stForm"] {
        background: rgba(255, 255, 255, 0.98);
        padding: 3rem;
        border-radius: 30px;
        box-shadow: 0 30px 90px rgba(102, 126, 234, 0.4), 0 0 50px rgba(102, 126, 234, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.2);
        animation: formGlow 3s ease-in-out infinite;
    }
    
    @keyframes formGlow {
        0%, 100% { box-shadow: 0 30px 90px rgba(102, 126, 234, 0.4), 0 0 50px rgba(102, 126, 234, 0.2); }
        50% { box-shadow: 0 30px 90px rgba(118, 75, 162, 0.5), 0 0 70px rgba(118, 75, 162, 0.3); }
    }
    
    /* Headers with gradient text */
    h1 {
        color: white !important;
        text-align: center;
        font-size: 4rem !important;
        font-weight: 800 !important;
        margin-bottom: 0.5rem !important;
        letter-spacing: -2px;
        text-shadow: 0 4px 20px rgba(255, 255, 255, 0.3), 0 0 40px rgba(255, 255, 255, 0.2);
        animation: titleFloat 3s ease-in-out infinite;
    }
    
    @keyframes titleFloat {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    h2 {
        color: #1a1a2e !important;
        font-weight: 700 !important;
        font-size: 1.8rem !important;
        margin-top: 2rem !important;
        margin-bottom: 1.5rem !important;
        padding-left: 1rem;
        border-left: 5px solid #667eea;
        animation: slideInLeft 0.6s ease;
    }
    
    @keyframes slideInLeft {
        from { opacity: 0; transform: translateX(-30px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    h3 {
        color: rgba(255, 255, 255, 0.95) !important;
        text-align: center;
        font-weight: 400 !important;
        font-size: 1.3rem !important;
        margin-bottom: 3rem !important;
        animation: fadeIn 1.5s ease;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    /* Input Fields with focus glow */
    .stTextInput > label, .stNumberInput > label, .stSelectbox > label {
        color: #000000 !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
        margin-bottom: 0.5rem;
        text-shadow: 0 0 1px rgba(255,255,255,0.5);
    }
    
    .stTextInput input, .stNumberInput input {
        border: 2px solid #e0e7ff !important;
        border-radius: 12px !important;
        padding: 0.8rem 1rem !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
        background: #f8fafc !important;
        color: #1a1a2e !important;
    }
    
    .stTextInput input:focus, .stNumberInput input:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.2), 0 0 20px rgba(102, 126, 234, 0.3) !important;
        background: white !important;
        color: #1a1a2e !important;
        transform: scale(1.01);
    }
    
    /* Radio Buttons with hover animation */
    .stRadio > label {
        color: #1a1a2e !important;
        font-weight: 600 !important;
        font-size: 1.05rem !important;
        margin-bottom: 1rem !important;
    }
    
    .stRadio > div {
        background: linear-gradient(135deg, #f8fafc 0%, #ffffff 100%);
        padding: 1.2rem;
        border-radius: 16px;
        border: 2px solid #e0e7ff;
        margin-bottom: 1.5rem;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }
    
    .stRadio > div > label {
        background: white;
        padding: 0.8rem 1.2rem;
        border-radius: 10px;
        margin: 0.3rem 0;
        border: 2px solid #e0e7ff;
        transition: all 0.3s ease;
        cursor: pointer;
        display: block;
        color: #1a1a2e !important;
    }
    
    .stRadio > div > label > div {
        color: #1a1a2e !important;
    }
    
    .stRadio > div > label:hover {
        border-color: #667eea;
        background: linear-gradient(135deg, #f0f4ff 0%, #e8edff 100%);
        transform: translateX(8px) scale(1.02);
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.2);
    }
    
    /* Selected radio button with gradient */
    .stRadio > div > label:has(input:checked) {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border-color: #667eea !important;
        transform: translateX(10px) scale(1.03);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
    
    .stRadio > div > label:has(input:checked) > div {
        color: white !important;
    }
    
    /* Submit Button with pulse animation */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        font-weight: 700 !important;
        font-size: 1.2rem !important;
        padding: 1rem 4rem !important;
        border-radius: 50px !important;
        border: none !important;
        box-shadow: 0 10px 40px rgba(102, 126, 234, 0.4) !important;
        transition: all 0.4s ease !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        width: 100% !important;
        margin-top: 2rem !important;
        animation: buttonPulse 2s ease-in-out infinite;
    }
    
    @keyframes buttonPulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.02); box-shadow: 0 15px 50px rgba(102, 126, 234, 0.6) !important; }
    }
    
    .stButton > button:hover {
        transform: translateY(-5px) scale(1.05) !important;
        box-shadow: 0 20px 60px rgba(102, 126, 234, 0.7) !important;
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%) !important;
    }
    
    .stButton > button:active {
        transform: translateY(-2px) scale(1.02) !important;
    }
    
    /* Sidebar with gradient */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%) !important;
        box-shadow: 5px 0 20px rgba(0,0,0,0.3);
    }
    
    section[data-testid="stSidebar"] h2 {
        color: white !important;
        border: none !important;
        padding: 0 !important;
    }
    
    section[data-testid="stSidebar"] label {
        color: rgba(255, 255, 255, 0.9) !important;
        font-weight: 600 !important;
    }
    
    section[data-testid="stSidebar"] .stSelectbox > div > div,
    section[data-testid="stSidebar"] .stRadio > div > label {
        background: rgba(255, 255, 255, 0.1) !important;
        border: 2px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 12px !important;
        color: white !important;
        transition: all 0.3s ease;
    }
    
    /* Selectbox text color fix for dark mode */
    .stSelectbox > div > div {
        color: #1a1a2e !important;
    }
    
    .stSelectbox [data-baseweb="select"] {
        color: #1a1a2e !important;
    }
    
    section[data-testid="stSidebar"] .stSelectbox > div > div:hover,
    section[data-testid="stSidebar"] .stRadio > div > label:hover {
        background: rgba(255, 255, 255, 0.2) !important;
        transform: scale(1.02);
    }
    
    /* Profile Card with shimmer effect */
    .profile-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 3rem;
        border-radius: 30px;
        color: white;
        box-shadow: 0 30px 90px rgba(102, 126, 234, 0.5);
        margin: 2rem 0;
        text-align: center;
        position: relative;
        overflow: hidden;
    }
    
    .profile-card::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent, rgba(255,255,255,0.1), transparent);
        animation: shimmer 3s infinite;
    }
    
    @keyframes shimmer {
        0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
        100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
    }
    
    .profile-card h1 {
        color: white !important;
        -webkit-text-fill-color: white !important;
        font-size: 5rem !important;
        margin: 0 !important;
        animation: bounce 2s ease-in-out infinite;
    }
    
    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-15px); }
    }
    
    .profile-card h2 {
        color: white !important;
        border: none !important;
        padding: 0 !important;
        margin: 1rem 0 !important;
        font-size: 2.5rem !important;
    }
    
    /* Metric Card with hover lift */
    .metric-card {
        background: linear-gradient(135deg, #ffffff 0%, #f6f8fb 100%);
        padding: 2.5rem;
        border-radius: 25px;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.1);
        text-align: center;
        border-top: 5px solid #667eea;
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 30px 80px rgba(102, 126, 234, 0.3);
    }
    
    /* Alerts with slide animation */
    .stAlert {
        border-radius: 15px;
        border-left: 5px solid;
        animation: slideInRight 0.5s ease;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    @keyframes slideInRight {
        from { opacity: 0; transform: translateX(30px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    /* Data Frame with fade in */
    .stDataFrame {
        border-radius: 20px;
        overflow: hidden;
        animation: fadeInUp 0.8s ease;
    }
    
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Scrollbar with gradient */
    ::-webkit-scrollbar {
        width: 12px;
        height: 12px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        transition: all 0.3s ease;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #764ba2 0%, #f093fb 100%);
    }
    
    /* Required Indicator */
    .stTextInput label::after, .stNumberInput label::after, .stRadio > label::after {
        content: " *";
        color: #ef4444;
        font-weight: 700;
    }
    
    /* Remove asterisk from optional fields */
    .stTextInput:has(input[placeholder*="Optional"]) label::after {
        content: "";
    }
    
    /* Spacing */
    .element-container {
        margin-bottom: 0.5rem;
    }
    
    /* Credit text with glow */
    .credit-text {
        position: fixed;
        top: 80px;
        right: 20px;
        color: rgba(255, 255, 255, 0.9);
        font-size: 0.9rem;
        font-weight: 600;
        z-index: 999;
        background: rgba(102, 126, 234, 0.3);
        padding: 0.5rem 1rem;
        border-radius: 10px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        animation: creditGlow 2s ease-in-out infinite;
    }
    
    @keyframes creditGlow {
        0%, 100% { box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3); }
        50% { box-shadow: 0 4px 25px rgba(102, 126, 234, 0.6); }
    }
</style>
""", unsafe_allow_html=True)

# Add credit text
st.markdown("""
<div class='credit-text'>
    Python Project by Swarna M
</div>
""", unsafe_allow_html=True)

# Questions
QUESTIONS = [
    {"q": "What's your go-to music when you're alone?", "options": ["Sad/emotional songs", "Upbeat party tracks", "Motivational anthems", "Chill lo-fi/instrumental"]},
    {"q": "How do you handle conflict?", "options": ["Confront directly", "Avoid and move on", "Analyze and strategize", "Mediate and find balance"]},
    {"q": "Your phone screen time is mostly spent on:", "options": ["Social media scrolling", "Learning/reading", "Gaming/entertainment", "Messaging friends"]},
    {"q": "When making big decisions, you rely on:", "options": ["Gut feeling", "Logic and data", "Others' advice", "Mix of heart and mind"]},
    {"q": "Your ideal weekend looks like:", "options": ["Adventure/exploring new places", "Relaxing at home", "Socializing with friends", "Working on personal projects"]},
    {"q": "How do you react to sudden change?", "options": ["Embrace it excitedly", "Feel anxious initially", "Adapt quickly", "Resist and prefer stability"]},
    {"q": "In a group project, you naturally become:", "options": ["The leader", "The creative mind", "The organizer", "The supporter"]},
    {"q": "Your sleep pattern is:", "options": ["Early bird (before 11 PM)", "Night owl (after 1 AM)", "Irregular/depends on mood", "Disciplined routine"]},
    {"q": "When someone wrongs you, you:", "options": ["Seek revenge/justice", "Forgive but don't forget", "Move on completely", "Confront and resolve"]},
    {"q": "Your risk-taking level is:", "options": ["High - YOLO mindset", "Calculated risks only", "Very cautious", "Depends on the situation"]},
    {"q": "People describe you as:", "options": ["Intense and passionate", "Calm and composed", "Fun and spontaneous", "Deep and mysterious"]},
    {"q": "Your biggest fear is:", "options": ["Being ordinary/forgotten", "Losing loved ones", "Failure", "Being controlled/trapped"]}
]

def save_response(responses):
    # Try Google Sheets first
    if save_to_sheet(responses):
        return
    # Fallback to CSV for local testing
    df = pd.DataFrame([responses])
    if os.path.exists(DATA_FILE):
        df.to_csv(DATA_FILE, mode='a', header=False, index=False, escapechar='\\')
    else:
        df.to_csv(DATA_FILE, index=False, escapechar='\\')

def load_data():
    # Try Google Sheets first
    df = load_from_sheet()
    if not df.empty:
        return df
    # Fallback to CSV for local testing
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE, escapechar='\\')
    return pd.DataFrame()

def preprocess_data(df):
    df_encoded = df.copy()
    # Skip Name, Age, Email, College, Year, Comments columns
    for col in df_encoded.columns:
        if col not in ['Name', 'Age', 'Email', 'College', 'Year', 'Comments', 'timestamp']:
            df_encoded[col] = pd.Categorical(df_encoded[col]).codes
    return df_encoded

def cluster_analysis(df):
    df_encoded = preprocess_data(df)
    # Use only question columns for clustering
    X = df_encoded[[f'Q{i+1}' for i in range(12)]].values
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    n_clusters = min(10, len(df))
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    clusters = kmeans.fit_predict(X_scaled)
    return clusters

def get_character_image(character_name, gender):
    """Load character image if exists"""
    name = character_name.split()[0]
    
    # Try exact match first
    image_path = f"{name}.jpg"
    if os.path.exists(image_path):
        return Image.open(image_path)
    
    # Try case-insensitive match in current directory
    for file in os.listdir("."):
        if file.lower().startswith(name.lower()) and file.endswith(".jpg"):
            return Image.open(file)
    
    return None

def get_profile(cluster, gender):
    profiles = {
        0: {"name": "JD", "movie": "(From Master)", "desc": "Emotionally intense rebel with sad music preference. You're a night owl with high risk appetite and embrace change. Gut feeling drives your decisions.", "strength": "Your raw authenticity and courage inspire others to break free.", "weakness": "Your intensity and impulsiveness can push people away. Channel emotions wisely.", "vibe": "Bold, rebellious, and deeply emotional. You live life on your own terms.", "color": "#667eea", "emoji": "🔥"},
        1: {"name": "Vinayak Mahadev", "movie": "(From Mankatha)", "desc": "High-risk strategist with revenge mindset. You use logic for selfish calculation, love control, and stay strategic under pressure.", "strength": "Your manipulative genius and calculated risks always keep you ahead.", "weakness": "Your selfishness isolates you. Trust and loyalty can be strengths too.", "vibe": "Cunning, strategic, and ruthlessly ambitious. You play to win at any cost.", "color": "#764ba2", "emoji": "♟️"},
        2: {"name": "Vijay Kumar IPS", "movie": "(From Theri)", "desc": "Justice-driven leader with disciplined routine. You listen to motivational music, lead groups naturally, and fear losing loved ones.", "strength": "Your leadership and sense of justice make you a natural protector.", "weakness": "You carry too much responsibility. Learn to share the burden.", "vibe": "Disciplined, protective, and justice-oriented. You serve and protect.", "color": "#f093fb", "emoji": "👮"},
        3: {"name": "Ganesh", "movie": "(From Vedalom)", "desc": "Calm outside, intense inside. You forgive but don't forget, protect family fiercely, and confront directly when needed.", "strength": "Your emotional control and protective nature make you a guardian.", "weakness": "Your hidden aggression can explode unexpectedly. Express emotions regularly.", "vibe": "Calm protector with hidden fire. You're gentle until provoked.", "color": "#f5576c", "emoji": "🛡️"},
        4: {"name": "Kabali", "movie": "(From Kabali)", "desc": "Calm and composed with strategic thinking. You're justice-oriented, a natural leader with disciplined sleep patterns and mature authority.", "strength": "Your calm dominance and wisdom command respect effortlessly.", "weakness": "Your emotional detachment can seem cold. Show vulnerability sometimes.", "vibe": "Mature, authoritative, and strategically brilliant. You lead with quiet power.", "color": "#667eea", "emoji": "👑"},
        5: {"name": "Suriya", "movie": "(From Vaaranam Aayiram)", "desc": "Deep and mysterious with sad music preference. You fear losing loved ones, make emotional decisions, and overthink at night.", "strength": "Your emotional depth and empathy create profound connections.", "weakness": "Your overthinking and nostalgia trap you in the past. Live in the now.", "vibe": "Emotional, nostalgic, and deeply introspective. You feel everything intensely.", "color": "#764ba2", "emoji": "💙"},
        6: {"name": "Anbu", "movie": "(From Vikram)", "desc": "Silent strategist who analyzes everything. You're calm, make logical decisions, adapt quickly, and stay silent in groups.", "strength": "Your analytical mind and adaptability make you invaluable in crisis.", "weakness": "Your silence can be misunderstood. Communicate your thoughts more.", "vibe": "Silent, strategic, and highly observant. You see what others miss.", "color": "#f093fb", "emoji": "🎯"},
        7: {"name": "Rolex", "movie": "(From Vikram)", "desc": "Extreme dominance with high risk appetite. You're intense, fear being controlled, seek revenge, and thrive as a night owl.", "strength": "Your power psychology and fearlessness make you unstoppable.", "weakness": "Your need for control creates enemies. Power without wisdom is dangerous.", "vibe": "Dominant, fearless, and ruthlessly powerful. You bow to no one.", "color": "#f5576c", "emoji": "💀"},
        8: {"name": "Siva", "movie": "(From Siva Manasula Sakthi)", "desc": "Fun and spontaneous with high social energy. You confront directly but emotionally, love socializing, and make decisions with gut feeling mixed with heart and mind.", "strength": "Your social charm and spontaneity make you the life of every gathering.", "weakness": "Your emotional reactivity can create unnecessary drama. Think before reacting.", "vibe": "Socially vibrant, emotionally expressive, and dramatically fun. You live for connections.", "color": "#667eea", "emoji": "🎉"},
        9: {"name": "Karna", "movie": "(From Asuran)", "desc": "Calm but explosive with suppressed anger. You protect loved ones, move on but remember, and fear losing family above all.", "strength": "Your emotional loyalty and protective instinct make you a fierce guardian.", "weakness": "Your suppressed rage can erupt destructively. Process emotions healthily.", "vibe": "Quietly intense, fiercely loyal, and emotionally charged. You protect your own.", "color": "#764ba2", "emoji": "🌾"}
    }
    return profiles.get(cluster, profiles[0])

# Main App
def main_app():
    st.markdown("<h1>HabitMatrix</h1>", unsafe_allow_html=True)
    st.markdown("<h3>Where Habits Become Insights</h3>", unsafe_allow_html=True)
    
    st.warning("⚠️ **Ethical Disclaimer**: This assessment is for self-awareness purposes only and is not a clinical psychological diagnosis.")
    
    with st.form("assessment_form"):
        st.markdown("<h2>👤 Personal Information</h2>", unsafe_allow_html=True)
        responses = {}
        col1, col2 = st.columns(2)
        with col1:
            responses['Name'] = st.text_input("Name", key="name", placeholder="Enter your full name")
            responses['Age'] = st.number_input("Age", min_value=1, max_value=120, step=1, key="age")
            responses['College'] = st.text_input("College (Optional)", key="college", placeholder="Enter your college name")
        with col2:
            responses['Email'] = st.text_input("Email", key="email", placeholder="your@email.com")
            responses['Year'] = st.selectbox("Year", ["1st Year", "2nd Year", "3rd Year", "4th Year", "Graduate", "Other"], key="year")
        
        st.markdown("<h2>🎭 Personality Assessment</h2>", unsafe_allow_html=True)
        
        for i, item in enumerate(QUESTIONS):
            col1, col2 = st.columns([3, 2])
            with col1:
                responses[f"Q{i+1}"] = st.radio(f"{i+1}. {item['q']}", item['options'], key=f"q{i}", index=None)
            with col2:
                video_path = f"{i+1}.mp4"
                if os.path.exists(video_path):
                    video_file = open(video_path, 'rb')
                    video_bytes = video_file.read()
                    video_base64 = base64.b64encode(video_bytes).decode()
                    st.markdown(f"""
                    <div style="margin-top: 3rem;">
                        <video width="100%" height="auto" autoplay loop muted playsinline style="border-radius: 15px; max-height: 300px; object-fit: contain;">
                            <source src="data:video/mp4;base64,{video_base64}" type="video/mp4">
                        </video>
                    </div>
                    """, unsafe_allow_html=True)
        
        st.markdown("<h2 style='margin-top: 2rem;'>💬 Additional Comments (Optional)</h2>", unsafe_allow_html=True)
        col1, col2 = st.columns([3, 2])
        with col1:
            responses['Comments'] = st.text_area("Anything you wanna say?", placeholder="Share your thoughts, feedback, or anything else...", key="comments")
        with col2:
            if os.path.exists("others.jpg"):
                st.image("others.jpg", use_column_width=True)
            elif os.path.exists("others.png"):
                st.image("others.png", use_column_width=True)
        
        responses['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        submitted = st.form_submit_button("🚀 Submit")
        
        if submitted:
            # Validate all fields
            if not responses['Name'] or not responses['Email'] or not responses['Age']:
                if os.path.exists("Fails.jpg"):
                    col1, col2, col3 = st.columns([1, 2, 1])
                    with col2:
                        st.image("Fails.jpg", use_column_width=True)
                st.error("❌ Please fill in all required personal information fields (Name, Age, Email, Year).")
                return
            
            # Validate all questions are answered
            for i in range(12):
                if not responses.get(f"Q{i+1}"):
                    if os.path.exists("Fails.jpg"):
                        col1, col2, col3 = st.columns([1, 2, 1])
                        with col2:
                            st.image("Fails.jpg", use_column_width=True)
                    st.error(f"❌ Please answer Question {i+1}.")
                    return
            
            # Show thank you image after successful submission
            if os.path.exists("thank.jpg"):
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    st.image("thank.jpg", use_column_width=True)
            
            save_response(responses)
            
            df = load_data()
            if len(df) >= 1:
                clusters = cluster_analysis(df)
                user_cluster = clusters[-1]
                profile = get_profile(user_cluster, 'male')
                
                st.balloons()
                
                # Show cutout images animation
                cutout_cols = st.columns(5)
                for idx, col in enumerate(cutout_cols):
                    cutout_num = 20 + idx
                    cutout_path = f"{cutout_num}.png"
                    if not os.path.exists(cutout_path):
                        cutout_path = f"{cutout_num}.jpg"
                    if os.path.exists(cutout_path):
                        with col:
                            st.markdown(f"""
                            <div style='animation: floatUp 2s ease-out;'>
                                <img src='data:image/png;base64,{base64.b64encode(open(cutout_path, 'rb').read()).decode()}' 
                                     style='width: 100%; animation: bounce 1s ease-in-out infinite;' />
                            </div>
                            <style>
                                @keyframes floatUp {{
                                    from {{ opacity: 0; transform: translateY(100px); }}
                                    to {{ opacity: 1; transform: translateY(0); }}
                                }}
                            </style>
                            """, unsafe_allow_html=True)
                
                # Add scroll message
                st.markdown("""
                <div style='text-align: center; padding: 2rem; margin: 2rem auto; max-width: 600px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 20px; box-shadow: 0 8px 30px rgba(0,0,0,0.3); border: 3px solid #ffffff;'>
                    <h3 style='color: #ffffff; font-size: 2.5rem; margin: 0; font-weight: 800; text-shadow: 2px 2px 4px rgba(0,0,0,0.3); animation: pulse 2s ease-in-out infinite;'>
                        Scroll pannu namba 😊🎀
                    </h3>
                </div>
                <style>
                    @keyframes pulse {
                        0%, 100% { opacity: 1; transform: scale(1); }
                        50% { opacity: 0.8; transform: scale(1.05); }
                    }
                </style>
                """, unsafe_allow_html=True)
                
                # Creative success message with emoji animation
                st.markdown("""
                <div style='text-align: center; padding: 2rem; animation: fadeIn 1s;'>
                    <h1 style='font-size: 4rem; margin: 0; animation: bounce 1s;'>🎉</h1>
                    <h2 style='color: white; margin: 1rem 0;'>Character Match Found!</h2>
                </div>
                <style>
                    @keyframes bounce {
                        0%, 100% { transform: translateY(0); }
                        50% { transform: translateY(-20px); }
                    }
                    @keyframes fadeIn {
                        from { opacity: 0; }
                        to { opacity: 1; }
                    }
                </style>
                """, unsafe_allow_html=True)
                
                # Try to load character image
                char_image = get_character_image(profile['name'], 'male')
                
                # Center the image
                if char_image:
                    col1, col2, col3 = st.columns([1, 2, 1])
                    with col2:
                        st.image(char_image, use_column_width=True)
                
                # Display profile card
                st.markdown(f"""
                <div class='profile-card'>
                    <h1 style='text-align: center; margin: 0; font-size: 4rem;'>{profile['emoji']}</h1>
                    <h2 style='text-align: center; color: white; border: none; text-shadow: 2px 2px 4px rgba(0,0,0,0.3); font-size: 2rem;'>🎬 Your Tamil Movie Character Match:</h2>
                    <h2 style='text-align: center; color: white; border: none; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);'>{profile['name']}</h2>
                    <p style='text-align: center; color: rgba(255,255,255,0.9); font-size: 1.1rem; margin-top: 0.5rem;'>{profile['movie']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Use Streamlit containers for content sections
                with st.container():
                    st.markdown(f"""
                    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                                padding: 2rem; border-radius: 20px; margin: 1rem 0; color: white;'>
                        <h3 style='color: white; margin-top: 0;'>🧠 Why You Got This Result:</h3>
                        <p style='color: white; font-size: 1.1rem; line-height: 1.6;'>{profile['desc']}</p>
                        
                        <h3 style='color: white; margin-top: 1.5rem;'>🔥 Your Core Strength:</h3>
                        <p style='color: white; font-size: 1.1rem; line-height: 1.6;'>{profile['strength']}</p>
                        
                        <h3 style='color: white; margin-top: 1.5rem;'>⚠️ Your Hidden Weakness:</h3>
                        <p style='color: white; font-size: 1.1rem; line-height: 1.6;'>{profile['weakness']}</p>
                        
                        <h3 style='color: white; margin-top: 1.5rem;'>🎵 Your Vibe:</h3>
                        <p style='color: white; font-size: 1.1rem; line-height: 1.6;'>{profile['vibe']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Show happy image at the end
                if os.path.exists("happy.jpg"):
                    col1, col2, col3 = st.columns([1, 2, 1])
                    with col2:
                        st.image("happy.jpg", use_column_width=True)
                
                # Add reaction text and video
                st.markdown("<h2 style='text-align: center; color: white; margin-top: 2rem;'>Me After Reading All Your Data:</h2>", unsafe_allow_html=True)
                
                if os.path.exists("reaction.mp4"):
                    col1, col2, col3 = st.columns([1, 2, 1])
                    with col2:
                        video_file = open("reaction.mp4", 'rb')
                        video_bytes = video_file.read()
                        video_base64 = base64.b64encode(video_bytes).decode()
                        st.markdown(f"""
                        <video width="100%" height="auto" autoplay loop muted playsinline style="border-radius: 20px; max-height: 400px; object-fit: contain;">
                            <source src="data:video/mp4;base64,{video_base64}" type="video/mp4">
                        </video>
                        """, unsafe_allow_html=True)
            else:
                st.success("✅ Response recorded! Complete more assessments to generate your character profile.")
                st.info("📊 We need at least 1 response to perform clustering analysis. Keep going!")

def admin_dashboard():
    st.markdown("<h1>📈 Admin Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("<h3>Analytics & Insights</h3>", unsafe_allow_html=True)
    
    password = st.text_input("🔑 Admin Password", type="password", placeholder="Enter password")
    
    if password == ADMIN_PASSWORD:
        df = load_data()
        
        if df.empty:
            st.warning("📄 No responses yet.")
            return
        
        st.markdown(f"""
        <div class='metric-card'>
            <h2 style='color: #667eea; margin: 0; font-size: 3rem;'>{len(df)}</h2>
            <p style='color: #718096; margin: 0.5rem 0 0 0; font-weight: 600; font-size: 1.1rem;'>📊 Total Responses</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<div style='margin: 2rem 0;'></div>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("<h2>📋 Response Data</h2>", unsafe_allow_html=True)
            st.dataframe(df.head(10), use_container_width=True)
        
        with col2:
            st.markdown("<h2>📈 Question Analysis</h2>", unsafe_allow_html=True)
            q_col = st.selectbox("Select Question", [f"Q{i+1}" for i in range(12)])
            fig = px.pie(df, names=q_col, title=f"{q_col} Distribution", 
                        color_discrete_sequence=['#667eea', '#764ba2', '#f093fb', '#f5576c', '#4facfe', '#00f2fe'])
            fig.update_layout(
                paper_bgcolor='rgba(255,255,255,0.9)', 
                plot_bgcolor='rgba(255,255,255,0.9)',
                font=dict(size=13, color='#2d3748'),
                title_font_size=16
            )
            st.plotly_chart(fig, use_container_width=True)
        
        if len(df) >= 1:
            clusters = cluster_analysis(df)
            df['Cluster'] = clusters
            
            st.markdown("<h2 style='margin-top: 2rem;'>🎯 Cluster Distribution</h2>", unsafe_allow_html=True)
            cluster_counts = pd.Series(clusters).value_counts().sort_index()
            
            fig = go.Figure(data=[
                go.Bar(x=[f"Cluster {i}" for i in cluster_counts.index], 
                       y=cluster_counts.values,
                       marker=dict(
                           color=['#667eea', '#764ba2', '#f093fb', '#f5576c'],
                           line=dict(color='white', width=3),
                           pattern_shape=""),
                       text=cluster_counts.values,
                       textposition='auto',
                       textfont=dict(size=16, color='white', family='Poppins'))
            ])
            fig.update_layout(
                title="Users per Cluster", 
                xaxis_title="Cluster", 
                yaxis_title="Count",
                paper_bgcolor='rgba(255,255,255,0.9)',
                plot_bgcolor='rgba(255,255,255,0.9)',
                font=dict(size=14, color='#2d3748', family='Poppins'),
                title_font_size=18,
                showlegend=False,
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.1)')
            )
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("<h2 style='margin-top: 2rem;'>🔥 Behavioral Correlation Heatmap</h2>", unsafe_allow_html=True)
            df_encoded = preprocess_data(df.drop('Cluster', axis=1))
            # Only correlate question columns
            q_cols = [f'Q{i+1}' for i in range(12)]
            corr = df_encoded[q_cols].corr()
            fig = px.imshow(corr, text_auto='.2f', aspect="auto", 
                          color_continuous_scale=[
                              [0, '#667eea'],
                              [0.5, '#ffffff'],
                              [1, '#f093fb']
                          ],
                          labels=dict(color="Correlation"))
            fig.update_layout(
                title="Question Correlations",
                paper_bgcolor='rgba(255,255,255,0.9)',
                font=dict(size=12, color='#2d3748', family='Poppins'),
                title_font_size=16
            )
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("<h2 style='margin-top: 2rem;'>🌟 Cluster Profiles Overview</h2>", unsafe_allow_html=True)
            
            unique_clusters = sorted(df['Cluster'].unique())
            num_clusters = len(unique_clusters)
            
            if num_clusters > 0:
                cols = st.columns(min(4, num_clusters))
                for idx, cluster_id in enumerate(unique_clusters):
                    profile = get_profile(cluster_id, 'male')
                    count = (df['Cluster'] == cluster_id).sum()
                    percentage = count/len(df)*100
                    
                    col_idx = idx % len(cols)
                    with cols[col_idx]:
                        st.markdown(f"""
                        <div style='background: linear-gradient(135deg, {profile['color']}22, {profile['color']}44); 
                                    padding: 1.5rem; border-radius: 15px; border-left: 5px solid {profile['color']};'>
                            <h3 style='color: {profile['color']}; margin: 0; font-size: 2rem; text-align: center;'>{profile['emoji']}</h3>
                            <h4 style='color: #2d3748; margin: 0.5rem 0; text-align: center; font-size: 0.9rem;'>{profile['name']}</h4>
                            <p style='color: #4a5568; text-align: center; margin: 0; font-size: 1.5rem; font-weight: bold;'>{count}</p>
                            <p style='color: #718096; text-align: center; margin: 0; font-size: 0.9rem;'>{percentage:.1f}%</p>
                        </div>
                        """, unsafe_allow_html=True)
    
    elif password:
        st.error("❌ Incorrect password")

# Navigation
st.sidebar.markdown("<h2 style='color: white; text-align: center; margin-bottom: 2rem;'>🧭 Menu</h2>", unsafe_allow_html=True)
page = st.sidebar.radio("Navigation", ["📝 Take Assessment", "📈 Admin Dashboard"])

if "Assessment" in page:
    main_app()
else:
    admin_dashboard()
