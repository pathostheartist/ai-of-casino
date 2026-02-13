import streamlit as st
import pandas as pd
import numpy as np
import time

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Admin Neural Control - BetPawa Edition", layout="wide")

# --- 2. SESSION STATE ---
if 'auth_status' not in st.session_state:
    st.session_state['auth_status'] = "logged_out"
if 'admin_msg' not in st.session_state:
    st.session_state['admin_msg'] = "System is running on BetPawa Real-time Archives."
if 'next_day_accuracy' not in st.session_state:
    st.session_state['next_day_accuracy'] = 85
if 'last_odds' not in st.session_state:
    st.session_state['last_odds'] = [1.10, 2.50, 1.05, 4.20, 1.15]

# --- 3. CUSTOM CSS ---
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
    .auth-box {
        background: #111; padding: 30px; border-radius: 15px;
        border: 1px solid #333; text-align: center; max-width: 450px; margin: auto;
    }
    .contact-btn {
        display: block; width: 100%; padding: 10px; margin: 10px 0;
        border-radius: 5px; text-decoration: none; font-weight: bold; text-align: center;
    }
    .admin-panel {
        background: #0e1117; padding: 15px; border-radius: 10px; border: 1px solid #ff4b4b;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. LOGIN INTERFACE ---
if st.session_state['auth_status'] != "authorized":
    st.markdown("<br><br>", unsafe_allow_html=True)
    with st.container():
        st.markdown("<div class='auth-box'>", unsafe_allow_html=True)
        st.header("NEURAL LOGIN")
        u_id = st.text_input("User ID")
        u_pin = st.text_input("Access PIN", type="password")
        
        if st.button("LOGIN", use_container_width=True):
            # Admin Credentials check
            if u_id == "admin" and u_pin == "2026":
                st.session_state['auth_status'] = "authorized"
                st.rerun()
            else:
                st.session_state['auth_status'] = "pending"
        
        if st.session_state['auth_status'] == "pending":
            st.error("⚠️ PLEASE CONTACT ADMIN TO PAY")
            st.markdown(f"""
                <a href="https://wa.me/250780000000" class="contact-btn" style="background: #25d366; color: white;">WhatsApp Admin</a>
                <a href="mailto:linezee3@gmail.com" class="contact-btn" style="background: #ea4335; color: white;">Email: linezee3@gmail.com</a>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# --- 5. MAIN SYSTEM (ADMIN ONLY CONTROL) ---
else:
    with st.sidebar:
        st.title("🎛️ ADMIN CONTROL")
        st.markdown("<div class='admin-panel'>", unsafe_allow_html=True)
        st.subheader("📅 Next Day Operations")
        
        # Admin defines tomorrow's performance
        st.session_state['next_day_accuracy'] = st.slider("Tomorrow's AI Accuracy (%)", 50, 99, st.session_state['next_day_accuracy'])
        next_day_mode = st.selectbox("Market Strategy", ["Aggressive", "Safe", "Random Cycle"])
        
        if st.button("Save Next Day Settings"):
            st.success("Settings scheduled for tomorrow!")
            
        st.write("---")
        st.subheader("📢 User Broadcast")
        new_msg = st.text_area("Update Live Notification")
        if st.button("Update Dashboard Message"):
            st.session_state['admin_msg'] = new_msg
            st.toast("Dashboard updated!")
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        game_choice = st.selectbox("SELECT GAME", ["AVIATOR", "JETX", "SPACEMAN", "ZEPPELIN", "LUCKY JET", "AVIAGAME", "SPACE XY", "PILOT"])
        
        if st.button("LOGOUT"):
            st.session_state['auth_status'] = "logged_out"
            st.rerun()

    # --- 6. DASHBOARD (BETPAWA STYLE) ---
    @st.fragment(run_every=5)
    def live_dashboard():
        # Update Odds
        new_odd = round(np.random.uniform(1.0, 4.0), 2)
        st.session_state['last_odds'].insert(0, new_odd)
        st.session_state['last_odds'] = st.session_state['last_odds'][:10]

        # UI Header
        st.markdown(f"<h2 style='text-align: center; color: #ff4b4b;'>🚀 {game_choice} NEURAL ANALYZER</h2>", unsafe_allow_html=True)
        st.info(f"🔔 **Notification:** {st.session_state['admin_msg']}")

        # BetPawa History Bar
        st.markdown("### 🕒 Last Results")
        odds_html = "".join([f"<div class='odd-circle {'odd-low' if o < 2 else 'odd-mid' if o < 10 else 'odd-high'}'>{o}x</div>" for o in st.session_state['last_odds']])
        st.markdown(f"<div>{odds_html}</div>", unsafe_allow_html=True)
        
        

        st.write("---")

        # Prediction engine (Influenced by Admin's current and next day settings)
        c1, c2 = st.columns(2)
        with c1:
            # Prediction influenced by accuracy slider
            acc_bonus = st.session_state['next_day_accuracy'] / 100
            pred = round(np.random.uniform(1.4, 2.5 + acc_bonus), 2)
            st.markdown(f"""
                <div style="background:#111; padding:35px; border-radius:15px; border: 2px solid #ff4b4b; text-align:center;">
                    <div style='color:#888; font-size:14px;'>AI PREDICTION</div>
                    <h1 style="color:#ff4b4b; font-size:75px;">{pred}x</h1>
                    <p style="color:#45ad15;">Confidence: {st.session_state['next_day_accuracy']}%</p>
                </div>
            """, unsafe_allow_html=True)
            
        with c2:
            st.markdown(f"""
                <div style="background:#111; padding:35px; border-radius:15px; border: 2px solid #333; text-align:center;">
                    <div style='color:#888; font-size:14px;'>ACTUAL FEED</div>
                    <h1 style="color:white; font-size:75px;">{new_odd}x</h1>
                    <p style="color:#888;">Synchronized with BetPawa</p>
                </div>
            """, unsafe_allow_html=True)

    live_dashboard()
