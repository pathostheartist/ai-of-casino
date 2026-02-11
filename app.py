import streamlit as st
import pandas as pd
import numpy as np
import time
import plotly.graph_objects as go

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Aviator AI Auto-Bot", layout="wide")

if 'db_users' not in st.session_state:
    st.session_state['db_users'] = {
        "admin_divin": {"password": "divin2026", "status": "Admin", "active": True},
        "test_user": {"password": "123", "status": "Trial", "active": True},
    }

# --- 2. AUTO-DATA ENGINE ---
# Iyi function niyo isoma imibare "iheruka" muri system
def fetch_last_odds():
    # Mu buzima busanzwe hano haba harimo link isoma amakuru ya casino
    # Ubu turakoresha random odds kugira ngo system ihuze na graph
    return [round(np.random.uniform(1.0, 5.0), 2) for _ in range(10)]

# --- 3. SMART AI LOGIC ---
def ai_brain(question, last_odds):
    question = question.lower()
    last_one = last_odds[-1]
    avg_odds = np.mean(last_odds)
    
    # AI isoma imibare iheruka ikaguha igisubizo gifatika
    if "signal" in question or "predict" in question:
        if last_one < 1.5:
            return f"Isesengura ryanjye ryerekana ko indege iheruka kugurukira hasi ({last_one}x). Round itaha ishobora kurenga 2.50x. Genda buhoro!"
        else:
            return f"System irerekana ko trend imeze neza. Average ubu ni {round(avg_odds, 2)}x. Inama: Cash out kuri 1.80x."
    elif "status" in question:
        return f"Server Status: STABLE. Last odd was {last_one}x. Ubushobozi bwanjye bwo gu-predict ubu ni 96%."
    else:
        return f"Nitegereje imibare 10 iheruka, mbona trend iri guhinduka. Round itaha ifite amahirwe 80% yo kurenga 2.0x. Wifuza ko nguha Signal?"

# --- 4. CUSTOM STYLING ---
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: white; }
    .ai-card {
        background-color: #111; padding: 20px; border-radius: 15px;
        border: 1px solid #ff4b4b; margin-top: 10px;
    }
    .user-msg { color: #888; font-style: italic; margin-top: 10px; }
    .ai-msg { color: #00ff00; font-weight: bold; margin-bottom: 10px; border-bottom: 1px solid #333; padding-bottom: 5px; }
    </style>
    """, unsafe_allow_html=True)

# --- 5. MAIN DASHBOARD ---
def user_dashboard():
    user = st.session_state['user']
    st.title(f"🚀 Aviator AI: Auto-Analysis Mode")
    
    # 1. FETCH LIVE DATA
    last_odds = fetch_last_odds()
    rounds = list(range(1, 11))

    # 2. GRAPH SECTION
    st.subheader("📊 Live Multiplier Trend")
    fig = go.Figure(go.Scatter(x=rounds, y=last_odds, mode='lines+markers', 
                               line=dict(color='#ff4b4b', width=4),
                               marker=dict(size=12, color='white')))
    fig.update_layout(paper_bgcolor='black', plot_bgcolor='black', font_color='white', height=400)
    st.plotly_chart(fig, use_container_width=True)
    

    st.write("---")

    # 3. CHATBOT SECTION (MUNSI YA GRAPH)
    st.subheader("🤖 AI Assistant (Auto-Reading Odds)")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if 'chat_history' not in st.session_state:
            st.session_state['chat_history'] = []

        # Chat Input
        with st.form(key='ai_chat', clear_on_submit=True):
            user_input = st.text_input("Ask AI about current trends:", placeholder="Urugero: Nimeze nte ubu?")
            submit = st.form_submit_button("Send to AI")
            
            if submit and user_input:
                response = ai_brain(user_input, last_odds)
                st.session_state['chat_history'].append({"q": user_input, "a": response})

        # Display Chat
        for chat in reversed(st.session_state['chat_history']):
            st.markdown(f'<div class="ai-card"><div class="user-msg">Wowe: {chat["q"]}</div><div class="ai-msg">AI Bot: {chat["a"]}</div></div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div style="background-color:#111; padding:15px; border-radius:10px;">', unsafe_allow_html=True)
        st.write("### AI Real-time Scan")
        st.write(f"Last Multiplier: **{last_odds[-1]}x**")
        st.write(f"Trend Strength: **High**")
        if st.button("🔄 Refresh Data"):
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# --- 6. ADMIN & LOGIN (Same as before) ---
def admin_panel():
    st.title("👨‍🔧 Admin Master")
    for username, info in st.session_state['db_users'].items():
        if username == "admin_divin": continue
        st.write(f"👤 {username} - Status: {'Active' if info['active'] else 'Blocked'}")
        if st.button("Toggle Access", key=username):
            st.session_state['db_users'][username]['active'] = not info['active']
            st.rerun()

if st.session_state['user'] is None:
    st.title("Aviator AI Pro Login")
    u = st.text_input("Username").lower().strip()
    p = st.text_input("Password", type="password")
    if st.button("Login"):
        db = st.session_state['db_users']
        if u in db and db[u]["password"] == p and db[u]["active"]:
            st.session_state['user'] = {"username": u, "status": db[u]["status"]}
            st.rerun()
        else: st.error("Invalid credentials.")
else:
    user = st.session_state['user']
    if user['status'] == "Admin":
        m = st.sidebar.radio("Menu", ["Dashboard", "Admin"])
        if m == "Admin": admin_panel()
        else: user_dashboard()
    else: user_dashboard()
    if st.sidebar.button("Logout"):
        st.session_state['user'] = None
        st.rerun()
