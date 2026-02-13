import streamlit as st
import pandas as pd
import numpy as np
import time
from datetime import datetime, timedelta
import plotly.graph_objects as go

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Neural Master Control v9", layout="wide")

# --- 2. DATABASE & CREDENTIALS ---
if 'admin_creds' not in st.session_state:
    st.session_state['admin_creds'] = {"user": "admin", "pwd": "2026"}
if 'user_db' not in st.session_state:
    # Tubanza gushyiramo admin muri DB kugira ngo agire access ihoraho
    st.session_state['user_db'] = {"admin": datetime.now() + timedelta(days=365)}
if 'auth_user' not in st.session_state:
    st.session_state['auth_user'] = None
if 'next_day_key' not in st.session_state:
    st.session_state['next_day_key'] = "1234" 
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
    .contact-btn {
        display: block; width: 100%; padding: 12px; margin: 10px 0;
        border-radius: 8px; text-decoration: none; font-weight: bold; text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. AUTHENTICATION (KOSORA KWINJIRA KWA USER) ---
def is_authorized(user, password):
    # 1. Check niba ari Admin
    if user == st.session_state['admin_creds']['user'] and password == st.session_state['admin_creds']['pwd']:
        return "admin"
    
    # 2. Check niba ari User washyizwemo na Admin kandi akaba akoresheje Key nyayo
    if user in st.session_state['user_db'] and password == st.session_state['next_day_key']:
        expiry_date = st.session_state['user_db'][user]
        if datetime.now() < expiry_date:
            return "user"
        else:
            return "expired"
            
    return "invalid"

if st.session_state['auth_user'] is None:
    st.markdown("<br><br>", unsafe_allow_html=True)
    with st.container():
        st.markdown("<div style='max-width:400px; margin:auto; background:#111; padding:25px; border-radius:15px; border:1px solid #333;'>", unsafe_allow_html=True)
        st.header("SYSTEM LOGIN")
        uid = st.text_input("Username / ID")
        pwd = st.text_input("Access Key", type="password")
        
        if st.button("LOGIN", use_container_width=True):
            result = is_authorized(uid, pwd)
            
            if result == "admin" or result == "user":
                st.session_state['auth_user'] = uid
                st.rerun()
            elif result == "expired":
                st.error("Access Expired. Contact Admin to re-pay.")
            else:
                st.error("Invalid Username or Access Key.")
        
        st.markdown(f"""
            <a href="https://wa.me/250780000000" class="contact-btn" style="background: #25d366; color: white;">WhatsApp Admin</a>
            <a href="mailto:linezee3@gmail.com" class="contact-btn" style="background: #ea4335; color: white;">Email: linezee3@gmail.com</a>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

else:
    # --- SIDEBAR (ADMIN CONTROL PANEL) ---
    with st.sidebar:
        st.title("🎛️ CONTROL PANEL")
        
        # Admin is the only one who can see these settings
        if st.session_state['auth_user'] == st.session_state['admin_creds']['user']:
            with st.expander("👤 ADMIN PROFILE"):
                new_admin_u = st.text_input("New Username", value=st.session_state['admin_creds']['user'])
                new_admin_p = st.text_input("New Password", type="password")
                if st.button("Update Profile"):
                    st.session_state['admin_creds']['user'] = new_admin_u
                    if new_admin_p: st.session_state['admin_creds']['pwd'] = new_admin_p
                    st.success("Admin Profile Updated!")

            st.write("---")
            st.session_state['next_day_key'] = st.text_input("Users' Key (Next Day)", value=st.session_state['next_day_key'])
            
            st.subheader("Add User Access")
            new_u = st.text_input("User ID")
            days = st.number_input("Days", 1, 30, 1)
            if st.button("Authorize User"):
                if new_u:
                    st.session_state['user_db'][new_u] = datetime.now() + timedelta(days=days)
                    st.success(f"User '{new_u}' added!")
                else: st.error("Enter a Username!")
        
        st.write("---")
        game_choice = st.selectbox("GAME", ["AVIATOR", "JETX", "LUCKY JET"])
        if st.button("LOGOUT"):
            st.session_state['auth_user'] = None
            st.rerun()

    # --- 5. DASHBOARD (BETPAWA STYLE) ---
    @st.fragment(run_every=5)
    def live_dashboard():
        if 'history' not in st.session_state: st.session_state['history'] = [1.3, 2.1, 1.0, 4.2]
        actual = round(np.random.uniform(1.0, 4.0), 2)
        st.session_state['history'].append(actual)
        if len(st.session_state['history']) > 15: st.session_state['history'].pop(0)

        st.markdown(f"<h2 style='text-align:center; color:#ff4b4b;'>🚀 {game_choice} PRO</h2>", unsafe_allow_html=True)
        
        # Last Results
        odds_html = "".join([f"<div class='odd-circle {'color:#34b7f1' if o < 2 else 'color:#ff4b4b'}'>{o}x</div>" for o in st.session_state['history'][-8:]])
        st.markdown(f"<div style='text-align:center;'>{odds_html}</div>", unsafe_allow_html=True)

        # Line Graph
        fig = go.Figure(go.Scatter(y=st.session_state['history'], mode='lines+markers', line=dict(color='#ff4b4b', width=3), fill='tozeroy'))
        fig.update_layout(paper_bgcolor='black', plot_bgcolor='black', height=220, margin=dict(l=0,r=0,t=10,b=0), xaxis=dict(visible=False), yaxis=dict(gridcolor='#222'))
        st.plotly_chart(fig, use_container_width=True)

        # Prediction Cards
        c1, c2 = st.columns(2)
        pred = round(np.random.uniform(1.6, 3.2), 2)
        status = "WIN" if actual >= pred else "LOSS"
        if status == "WIN": st.session_state['streak'] += 1
        else: st.session_state['streak'] = 0
        st.session_state['logs'].insert(0, {"AI": f"{pred}x", "Res": f"{actual}x", "Stat": status})

        with c1:
            st.markdown(f"<div style='background:#111; padding:20px; border-radius:15px; border:2px solid #ff4b4b; text-align:center;'><div style='color:#888;'>SIGNAL</div><h1 style='color:#ff4b4b; margin:0;'>{pred}x</h1><p style='color:#45ad15; margin:0;'>STREAK: {st.session_state['streak']}</p></div>", unsafe_allow_html=True)
        with c2:
            st.markdown(f"<div style='background:#111; padding:20px; border-radius:15px; border:2px solid #333; text-align:center;'><div style='color:#888;'>ACTUAL</div><h1 style='color:white; margin:0;'>{actual}x</h1><p style='color:#888; margin:0;'>LIVE FEED</p></div>", unsafe_allow_html=True)

        # Performance History
        st.write("---")
        st.markdown("### 📊 PERFORMANCE HISTORY")
        for log in st.session_state['logs'][:5]:
            color = "#45ad15" if log['Stat'] == "WIN" else "#ff4b4b"
            st.markdown(f"<div style='background:#111; padding:8px; border-radius:8px; margin-bottom:5px; border-left: 5px solid {color};'>AI: {log['AI']} | Result: {log['Res']} | <span style='color:{color}; font-weight:bold;'>{log['Stat']}</span></div>", unsafe_allow_html=True)

    live_dashboard()
