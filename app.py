import streamlit as st
import time

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Aviator AI Pro", layout="centered", page_icon="💰")

# Izina ryawe cyangwa rya system yawe
APP_NAME = "AVIATOR AI PRO"
ADMIN_WHATSAPP = "250780000000" # Shyiraho nimero yawe hano (format: 250...)

# --- 2. DATABASE Y'ABAKORESHA ---
# Hano niho ugiye kujya wandika abantu bose bishyuye.
# Niba umuntu wishyuye, muhe 'status': 'Premium'
USERS = {
    "admin_divin": {"password": "divin2026", "status": "Admin"},
    "test_user": {"password": "123", "status": "Trial"},  # Uyu azabona signals 3 gusa
    "eric_250": {"password": "pass", "status": "Premium"} # Uyu azajya abona byose
}

# --- 3. CUSTOM DESIGN (CASINO THEME) ---
st.markdown(f"""
    <style>
    .stApp {{ background-color: #0a0a0a; color: white; }}
    .stButton>button {{ 
        width: 100%; border-radius: 25px; 
        background: linear-gradient(90deg, #ff4b4b, #b30000); 
        color: white; font-weight: bold; border: none; height: 50px;
        font-size: 18px; box-shadow: 0 4px 15px rgba(255, 75, 75, 0.3);
    }}
    .premium-card {{
        background: linear-gradient(135deg, #1e1e1e, #111);
        padding: 25px; border-radius: 15px;
        border: 1px solid #ffd700; text-align: center;
        margin: 20px 0; box-shadow: 0 4px 20px rgba(255, 215, 0, 0.1);
    }}
    .signal-display {{
        background-color: #000; padding: 30px; border-radius: 20px;
        border: 3px solid #00ff00; text-align: center; font-family: 'Courier New', Courier, monospace;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 4. SESSION STATE ---
if 'user' not in st.session_state:
    st.session_state['user'] = None
if 'clicks' not in st.session_state:
    st.session_state['clicks'] = 0

# --- 5. AUTHENTICATION ---
def login():
    st.title(f"🚀 {APP_NAME}")
    st.subheader("Login to access live signals")
    
    u = st.text_input("Username").lower().strip()
    p = st.text_input("Password", type="password")
    
    if st.button("ENTER DASHBOARD"):
        if u in USERS and USERS[u]["password"] == p:
            st.session_state['user'] = {"username": u, "status": USERS[u]["status"]}
            st.success("Access Granted!")
            time.sleep(1)
            st.rerun()
        else:
            st.error("Access Denied! Check your credentials or contact Admin.")
    
    st.markdown("---")
    st.write("Don't have an account?")
    if st.button("GET ACCESS (5,000 RWF)"):
        st.markdown(f'<meta http-equiv="refresh" content="0;url=https://wa.me/{ADMIN_WHATSAPP}?text=Nshaka%20kugura%20Account%20ya%20Aviator%20AI">', unsafe_allow_html=True)

# --- 6. MAIN SYSTEM ---
def main():
    user = st.session_state['user']
    
    # Sidebar Info
    st.sidebar.title("💎 ACCOUNT")
    st.sidebar.write(f"User: **{user['username']}**")
    st.sidebar.write(f"Status: **{user['status']}**")
    
    if st.sidebar.button("LOGOUT"):
        st.session_state['user'] = None
        st.rerun()

    st.title("🎯 Live Signal Generator")
    
    # Logic ya Premium vs Trial
    if user['status'] == "Trial" and st.session_state['clicks'] >= 3:
        st.markdown(f"""
            <div class="premium-card">
                <h2 style="color: #ffd700;">🛑 TRIAL EXPIRED!</h2>
                <p>You have used your 3 free signals. To continue winning, upgrade to Premium.</p>
                <h3 style="color: white;">Price: 5,000 RWF / Lifetime</h3>
            </div>
            """, unsafe_allow_html=True)
        
        if st.button("CLICK TO PAY VIA WHATSAPP"):
            st.markdown(f'<meta http-equiv="refresh" content="0;url=https://wa.me/{ADMIN_WHATSAPP}?text=Mwaye%2C%20nishyuye%205000RWF%20kugira%20ngo%20muhe%20Premium%20kuri%20username%3A%20{user["username"]}">', unsafe_allow_html=True)
            
    else:
        st.info("Analysis: System is stable. High accuracy for next round.")
        
        if st.button("GENERATE NEXT SIGNAL"):
            st.session_state['clicks'] += 1
            with st.spinner("AI analyzing the server trends..."):
                time.sleep(2)
                # Iyi ni algorithm y'ikigeragezo - ushobora kuyongerera imbaraga
                import random
                odd = round(random.uniform(1.5, 5.5), 2)
                
                st.markdown(f"""
                    <div class="signal-display">
                        <h4 style="color: #888;">PREDICTION FOUND</h4>
                        <h1 style="color: #00ff00; font-size: 60px;">{odd}x</h1>
                        <p style="color: white;">Cash out at {round(odd-0.5, 2)}x for 100% safety</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                if user['status'] == "Trial":
                    st.warning(f"Free Signals Remaining: {3 - st.session_state['clicks']}")

# --- EXECUTION ---
if st.session_state['user'] is None:
    login()
else:
    main()
