import streamlit as st
import pandas as pd
import numpy as np
import time
from datetime import datetime, timedelta
import plotly.graph_objects as go

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Neural Master Control v5", layout="wide")

# --- 2. DATABASE SIMULATION (Muri Session State) ---
if 'user_db' not in st.session_state:
    # Izina: Igihe access izarangirira
    st.session_state['user_db'] = {
        "admin": datetime.now() + timedelta(days=365) # Admin has 1 year
    }
if 'auth_user' not in st.session_state:
    st.session_state['auth_user'] = None
if 'admin_msg' not in st.session_state:
    st.session_state['admin_msg'] = "System is active. New patterns detected."

# --- 3. CUSTOM BETPAWA CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: white; }
    .odd-circle {
        display: inline-block; width: 45px; height: 45px; line-height: 45px;
        border-radius: 50%; border: 1px solid #333; text-align: center;
        margin: 4px; font-weight: bold; font-size: 13px; background: #111;
    }
    .odd-low { color: #34b7f1; } 
    .odd-mid { color: #9b59b6; }
    .odd-high { color: #ff4b4b; }
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

# --- 4. AUTHENTICATION LOGIC ---
def check_expiry(user):
    if user in st.session_state['user_db']:
        expiry_date = st.session_state['user_db'][user]
        if datetime.now() < expiry_date:
            return True, expiry_date
    return False, None

# Login Page
if st.session_state['auth_user'] is None:
    st.markdown("<br><br>", unsafe_allow_html=True)
    with st.container():
        st.markdown("<div style='max-width:400px; margin:auto; background:#111; padding:25px; border-radius:15px; border:1px solid #333;'>", unsafe_allow_html=True)
        st.header("NEURAL ACCESS")
        uid = st.text_input("Username / ID")
        pwd = st.text_input("Password / PIN", type="password")
        
        if st.button("LOGIN", use_container_width=True):
            is_valid, exp = check_expiry(uid)
            # Admin login (Static for security)
            if uid == "admin" and pwd == "2026":
                st.session_state['auth_user'] = "admin"
                st.rerun()
            elif is_valid:
                st.session_state['auth_user'] = uid
                st.rerun()
            else:
                st.error("Access Expired or Invalid. Contact Admin.")
        st.markdown("</div>", unsafe_allow_html=True)

# --- 5. THE SYSTEM ---
else:
    current_user = st.session_state['auth_user']
    is_still_valid, expiry = check_expiry(current_user)

    # Iyo igihe cyarangiye
    if not is_still_valid:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown(f"""
            <div class='repay-box'>
                <h2 style='color:#ff4b4b;'>⚠️ ACCESS EXPIRED</h2>
                <p>Hello {current_user}, your subscription has ended.</p>
                <p style='font-size:18px; font-weight:bold;'>PLEASE CONTACT ADMIN TO RE-PAY</p>
                <a href="https://wa.me/250780000000" class="contact-btn" style="background: #25d366; color: white;">WhatsApp Admin</a>
                <a href="mailto:linezee3@gmail.com" class="contact-btn" style="background: #ea4335; color: white;">Email: linezee3@gmail.com</a>
                <br>
                <form action="/"><button type="submit" style="background:none; border:none; color:#888; text-decoration:underline; cursor:pointer;">Back to Login</button></form>
            </div>
        """, unsafe_allow_html=True)
        st.session_state['auth_user'] = None
        st.stop()

    # --- ADMIN SIDEBAR OPERATIONS ---
    with st.sidebar:
        st.title("🎛️ CONTROL CENTER")
        if current_user == "admin":
            st.markdown("### ➕ Add New User")
            new_uid = st.text_input("New User ID")
            days = st.number_input("Access Days", min_value=1, value=1)
            if st.button("Authorize User"):
                st.session_state['user_db'][new_uid] = datetime.now() + timedelta(days=days)
                st.success(f"User {new_uid} added for {days} day(s)!")
            
            st.write("---")
            st.subheader("📢 Broadcast message")
            st.session_state['admin_msg'] = st.text_area("Live Notification", st.session_state['admin_msg'])
        else:
            st.info(f"User: {current_user}\nExpires: {expiry.strftime('%Y-%m-%d %H:%M')}")
        
        game_choice = st.selectbox("GAME", ["AVIATOR", "JETX", "SPACEMAN", "LUCKY JET"])
        if st.button("LOGOUT"):
            st.session_state['auth_user'] = None
            st.rerun()

    # --- 6. DASHBOARD WITH LINE GRAPH ---
    @st.fragment(run_every=5)
    def dashboard():
        # Data Update
        if 'history' not in st.session_state:
            st.session_state['history'] = [1.2, 2.5, 1.0, 3.2, 1.1]
        
        new_val = round(np.random.uniform(1.0, 4.0), 2)
        st.session_state['history'].append(new_val)
        if len(st.session_state['history']) > 15: st.session_state['history'].pop(0)
        
        st.markdown(f"<h2 style='text-align:center; color:#ff4b4b;'>🚀 {game_choice} NEURAL PRO</h2>", unsafe_allow_html=True)
        st.info(f"🔔 **Admin:** {st.session_state['admin_msg']}")

        # Top Circles
        odds_html = "".join([f"<div class='odd-circle {'odd-low' if o < 2 else 'odd-mid' if o < 10 else 'odd-high'}'>{o}x</div>" for o in st.session_state['history'][-8:]])
        st.markdown(f"<div style='text-align:center;'>{odds_html}</div>", unsafe_allow_html=True)

        # LINE GRAPH (BetPawa Style)
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            y=st.session_state['history'], 
            mode='lines+markers',
            line=dict(color='#ff4b4b', width=3),
            marker=dict(size=8, color='white'),
            fill='tozeroy',
            fillcolor='rgba(255, 75, 75, 0.1)'
        ))
        fig.update_layout(
            paper_bgcolor='black', plot_bgcolor='black', 
            margin=dict(l=10, r=10, t=10, b=10), height=250,
            yaxis=dict(gridcolor='#222', zeroline=False),
            xaxis=dict(visible=False)
        )
        st.plotly_chart(fig, use_container_width=True)
        
        

        # Prediction
        c1, c2 = st.columns(2)
        with c1:
            pred = round(np.random.uniform(1.6, 3.5), 2)
            st.markdown(f"""
                <div style='background:#111; padding:30px; border-radius:15px; border:2px solid #ff4b4b; text-align:center;'>
                    <div style='color:#888;'>NEXT SIGNAL</div>
                    <h1 style='color:#ff4b4b; font-size:60px;'>{pred}x</h1>
                    <p style='color:#45ad15;'>Accuracy: 96.4%</p>
                </div>
            """, unsafe_allow_html=True)
        with c2:
            st.markdown(f"""
                <div style='background:#111; padding:30px; border-radius:15px; border:2px solid #333; text-align:center;'>
                    <div style='color:#888;'>ACTUAL RESULT</div>
                    <h1 style='color:white; font-size:60px;'>{new_val}x</h1>
                    <p style='color:#888;'>Live Archives</p>
                </div>
            """, unsafe_allow_html=True)

    dashboard()
