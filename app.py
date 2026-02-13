import streamlit as st
import pandas as pd
import numpy as np
import time
from datetime import datetime, timedelta
import plotly.graph_objects as go

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Neural Master Control v6", layout="wide")

# --- 2. DATABASE ---
if 'user_db' not in st.session_state:
    st.session_state['user_db'] = {"admin": datetime.now() + timedelta(days=365)}
if 'auth_user' not in st.session_state:
    st.session_state['auth_user'] = None
if 'logs' not in st.session_state:
    st.session_state['logs'] = []
if 'streak' not in st.session_state:
    st.session_state['streak'] = 0

# --- 3. CUSTOM CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: white; }
    .odd-circle {
        display: inline-block; width: 45px; height: 45px; line-height: 45px;
        border-radius: 50%; border: 1px solid #333; text-align: center;
        margin: 4px; font-weight: bold; font-size: 13px; background: #111;
    }
    .repay-box {
        background: #111; padding: 30px; border-radius: 15px;
        border: 2px solid #ff4b4b; text-align: center; max-width: 450px; margin: auto;
    }
    .contact-btn {
        display: block; width: 100%; padding: 12px; margin: 10px 0;
        border-radius: 8px; text-decoration: none; font-weight: bold; text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. AUTHENTICATION (KOSORA BUG) ---
def check_expiry(user):
    if user in st.session_state['user_db']:
        expiry_date = st.session_state['user_db'][user]
        if datetime.now() < expiry_date:
            return True, expiry_date
    return False, None

if st.session_state['auth_user'] is None:
    st.markdown("<br><br>", unsafe_allow_html=True)
    with st.container():
        st.markdown("<div style='max-width:400px; margin:auto; background:#111; padding:25px; border-radius:15px; border:1px solid #333;'>", unsafe_allow_html=True)
        st.header("SYSTEM ACCESS")
        uid = st.text_input("Username")
        pwd = st.text_input("Access Key", type="password")
        
        if st.button("LOGIN", use_container_width=True):
            # Admin Security Fix: Lazima byose bihure
            if uid == "admin" and pwd == "2026":
                st.session_state['auth_user'] = "admin"
                st.rerun()
            elif uid != "admin" and uid != "": # Check regular users
                is_valid, exp = check_expiry(uid)
                if is_valid and pwd == "2026": # Assuming same key for now
                    st.session_state['auth_user'] = uid
                    st.rerun()
                else:
                    st.error("Invalid Credentials or Access Expired.")
            else:
                st.error("Invalid Username or Key.")
        st.markdown("</div>", unsafe_allow_html=True)

else:
    # Check if access is still valid while logged in
    current_user = st.session_state['auth_user']
    is_still_valid, expiry = check_expiry(current_user)

    if not is_still_valid:
        st.markdown(f"<div class='repay-box'><h2>⚠️ EXPIRED</h2><p>Please contact admin to re-pay.</p><a href='mailto:linezee3@gmail.com' class='contact-btn' style='background:#ea4335; color:white;'>Email Admin</a></div>", unsafe_allow_html=True)
        st.session_state['auth_user'] = None
        st.stop()

    # --- SIDEBAR ---
    with st.sidebar:
        st.title("🎛️ CONTROL")
        if current_user == "admin":
            st.subheader("Manage Users")
            new_u = st.text_input("User ID to Add")
            days = st.number_input("Days", 1, 30, 1)
            if st.button("Add User"):
                st.session_state['user_db'][new_u] = datetime.now() + timedelta(days=days)
                st.success(f"User {new_u} Authorized!")
        
        game_choice = st.selectbox("GAME", ["AVIATOR", "JETX", "LUCKY JET"])
        if st.button("LOGOUT"):
            st.session_state['auth_user'] = None
            st.rerun()

    # --- DASHBOARD FRAGMENT ---
    @st.fragment(run_every=5)
    def live_dashboard():
        if 'history' not in st.session_state: st.session_state['history'] = [1.5, 2.0, 1.1]
        
        actual = round(np.random.uniform(1.0, 4.0), 2)
        st.session_state['history'].append(actual)
        if len(st.session_state['history']) > 15: st.session_state['history'].pop(0)

        # 1. UI HEADER & CIRCLES
        st.markdown(f"<h2 style='text-align:center; color:#ff4b4b;'>🚀 {game_choice} PRO</h2>", unsafe_allow_html=True)
        odds_html = "".join([f"<div class='odd-circle {'color:#34b7f1' if o < 2 else 'color:#ff4b4b'}'>{o}x</div>" for o in st.session_state['history'][-8:]])
        st.markdown(f"<div style='text-align:center;'>{odds_html}</div>", unsafe_allow_html=True)

        # 2. LINE GRAPH
        fig = go.Figure(go.Scatter(y=st.session_state['history'], mode='lines+markers', line=dict(color='#ff4b4b', width=3), fill='tozeroy'))
        fig.update_layout(paper_bgcolor='black', plot_bgcolor='black', height=220, margin=dict(l=0,r=0,t=10,b=0), xaxis=dict(visible=False), yaxis=dict(gridcolor='#222'))
        st.plotly_chart(fig, use_container_width=True)

        # 3. PREDICTION & STREAK
        c1, c2 = st.columns(2)
        pred = round(np.random.uniform(1.6, 3.2), 2)
        
        # Win/Loss Logic for Logs
        status = "WIN" if actual >= pred else "LOSS"
        if status == "WIN": st.session_state['streak'] += 1
        else: st.session_state['streak'] = 0
        st.session_state['logs'].insert(0, {"AI": f"{pred}x", "Res": f"{actual}x", "Stat": status})

        with c1:
            st.markdown(f"<div style='background:#111; padding:20px; border-radius:15px; border:2px solid #ff4b4b; text-align:center;'><div style='color:#888;'>SIGNAL</div><h1 style='color:#ff4b4b; margin:0;'>{pred}x</h1><p style='color:#45ad15; margin:0;'>STREAK: {st.session_state['streak']}</p></div>", unsafe_allow_html=True)
        with c2:
            st.markdown(f"<div style='background:#111; padding:20px; border-radius:15px; border:2px solid #333; text-align:center;'><div style='color:#888;'>ACTUAL</div><h1 style='color:white; margin:0;'>{actual}x</h1><p style='color:#888; margin:0;'>LIVE FEED</p></div>", unsafe_allow_html=True)

        # 4. WIN/LOSS LOGS (HASI)
        st.write("---")
        st.markdown("### 📊 PERFORMANCE HISTORY")
        for log in st.session_state['logs'][:5]:
            color = "#45ad15" if log['Stat'] == "WIN" else "#ff4b4b"
            st.markdown(f"<div style='background:#111; padding:8px; border-radius:8px; margin-bottom:5px; border-left: 5px solid {color};'>AI: {log['AI']} | Result: {log['Res']} | <span style='color:{color}; font-weight:bold;'>{log['Stat']}</span></div>", unsafe_allow_html=True)

    live_dashboard()
