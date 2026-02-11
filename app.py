import streamlit as st
import pandas as pd
import numpy as np
import time
import plotly.graph_objects as go

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Aviator AI Pro Master", layout="wide")

if 'db_users' not in st.session_state:
    st.session_state['db_users'] = {
        "admin_divin": {"password": "divin2026", "status": "Admin", "active": True},
        "test_user": {"password": "123", "status": "Trial", "active": True},
    }

# --- 2. AI BRAIN (Simple Logic for Chat) ---
def get_ai_response(question):
    question = question.lower()
    if "win" in question or "gutsinda" in question:
        return "Inama ya AI: Tegerereza signal irenze 2.00x, ariko ube maso ku masegonda 5 ya mbere."
    elif "risk" in question or "akaga" in question:
        return "Ubu system irerekana ko risk iri kuri 15%. Ni umwanya mwiza wo gukina."
    elif "status" in question:
        return "Server iri gukora neza (STABLE). Amahirwe yo gutsinda ubu ni 94%."
    else:
        return "Icyo ni ikibazo cyiza. AI yanjye irimo gusoma pattern nshya, andika 'Signal' urebe niba isaha igeze."

# --- 3. CUSTOM CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: white; }
    .chat-bubble {
        background-color: #1a1a1a; padding: 15px; border-radius: 15px;
        border-left: 5px solid #ff4b4b; margin: 10px 0;
    }
    .user-bubble {
        background-color: #333; padding: 10px; border-radius: 10px;
        text-align: right; margin: 10px 0; font-style: italic;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. LOGIN LOGIC ---
if 'user' not in st.session_state:
    st.session_state['user'] = None

# --- 5. USER DASHBOARD ---
def user_dashboard():
    user = st.session_state['user']
    st.title(f"🚀 Aviator AI: Master Console")

    # Tab System for Organization
    tab_ana, tab_ai = st.tabs(["📊 Game Analytics", "🤖 Ask AI Assistant"])

    with tab_ana:
        c1, c2 = st.columns([2, 1])
        with c1:
            st.subheader("Live Multiplier Trend")
            # Simulation of live graph
            rounds = list(range(1, 11))
            odds = [round(np.random.uniform(1.0, 4.5), 2) for _ in range(10)]
            fig = go.Figure(go.Scatter(x=rounds, y=odds, mode='lines+markers', line=dict(color='#ff4b4b')))
            fig.update_layout(paper_bgcolor='black', plot_bgcolor='black', font_color='white')
            st.plotly_chart(fig, use_container_width=True)
            

        with c2:
            st.subheader("Signal Engine")
            if st.button("GET NEW SIGNAL"):
                with st.spinner("AI Analysis..."):
                    time.sleep(1.5)
                    st.success(f"🔥 Next Signal: {round(np.random.uniform(1.5, 5.0), 2)}x")

    with tab_ai:
        st.subheader("💬 Ask anything to Aviator AI")
        if 'chat_history' not in st.session_state:
            st.session_state['chat_history'] = []

        # Input field
        user_q = st.text_input("Andika ikibazo hano...", placeholder="Urugero: Ese ubu umukino umeze ute?")
        
        if st.button("SEND QUESTION"):
            if user_q:
                response = get_ai_response(user_q)
                st.session_state['chat_history'].append({"q": user_q, "a": response})
        
        # Display Chat History
        for chat in reversed(st.session_state['chat_history']):
            st.markdown(f'<div class="user-bubble">Wowe: {chat["q"]}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="chat-bubble"><b>AI:</b> {chat["a"]}</div>', unsafe_allow_html=True)
            

# --- 6. ADMIN PANEL ---
def admin_panel():
    st.title("👨‍🔧 Master Admin")
    db = st.session_state['db_users']
    for username, info in db.items():
        if username == "admin_divin": continue
        col1, col2, col3 = st.columns([2, 2, 1])
        col1.write(f"User: **{username}**")
        status = "✅ Active" if info['active'] else "🚫 Blocked"
        col2.write(f"Status: {status}")
        if col3.button("Toggle", key=username):
            st.session_state['db_users'][username]['active'] = not info['active']
            st.rerun()

# --- 7. MAIN ---
if st.session_state['user'] is None:
    # Login page
    st.title("Aviator AI Pro")
    u = st.text_input("Username").lower().strip()
    p = st.text_input("Password", type="password")
    if st.button("LOGIN"):
        db = st.session_state['db_users']
        if u in db and db[u]["password"] == p and db[u]["active"]:
            st.session_state['user'] = {"username": u, "status": db[u]["status"]}
            st.rerun()
        else:
            st.error("Account not found or Deactivated.")
else:
    user = st.session_state['user']
    st.sidebar.title(f"Hi, {user['username']}")
    if user['status'] == "Admin":
        menu = st.sidebar.radio("Menu", ["Admin Panel", "User Dashboard"])
        if menu == "Admin Panel": admin_panel()
        else: user_dashboard()
    else:
        user_dashboard()
    
    if st.sidebar.button("Logout"):
        st.session_state['user'] = None
        st.rerun()
