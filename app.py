import streamlit as st
import time

# --- 1. CONFIGURATION & DATABASE (Simulated) ---
# Mu buzima busanzwe hano twakoresha Firebase cyangwa Google Sheets
USERS = {
    "arsene": {"password": "123", "status": "premium"},
    "guest": {"password": "guest", "status": "trial", "signals_left": 3}
}

def check_login(username, password):
    if username in USERS and USERS[username]["password"] == password:
        return USERS[username]
    return None

# --- 2. THE APP INTERFACE ---
st.set_page_config(page_title="Casino AI Premium", layout="centered")

if 'user' not in st.session_state:
    st.session_state['user'] = None

# --- LOGIN PAGE ---
if st.session_state['user'] is None:
    st.title("🔐 Member Login")
    user_input = st.text_input("Username")
    pass_input = st.text_input("Password", type="password")
    
    if st.button("Login"):
        user_data = check_login(user_input, pass_input)
        if user_data:
            st.session_state['user'] = user_data
            st.rerun()
        else:
            st.error("Username cyangwa Password ntabwo ari byo.")
    
    st.info("Niba ushaka Trial, koresha: guest / guest")

# --- MAIN DASHBOARD (Only for logged in users) ---
else:
    user = st.session_state['user']
    st.sidebar.title(f"Welcome, {user_input}!")
    
    # 3. TRIAL & PAYMENT SYSTEM
    if user['status'] == "trial" and user['signals_left'] <= 0:
        st.warning("⚠️ Trial yawe yarangiye! Ishyura 5,000 RWF kuri MoMo (078xxxxxxx) ubone Full Access.")
        if st.button("Logout"):
            st.session_state['user'] = None
            st.rerun()
    else:
        # Hano niho ya AI Dashboard iherereye
        st.title("🎯 AI Premium Signals")
        
        if user['status'] == "trial":
            st.caption(f"Trial Mode: Usigaje signals {user['signals_left']}")

        # Input Section
        odds = st.text_input("Ingiza odds 9 za nyuma:")
        
        if st.button("GET SIGNAL"):
            if user['status'] == "trial":
                user['signals_left'] -= 1
            
            with st.spinner('Analyzing...'):
                time.sleep(1.5)
                # Ibisubizo bya AI (Bya bindi wifuzaga)
                st.success("✅ Pattern Found!")
                c1, c2, c3 = st.columns(3)
                c1.metric("PRED", "4.7x")
                c2.metric("TARGET", "3.9x")
                c3.metric("CHANCE", "70%")
                
                if user['status'] == "trial":
                    st.rerun() # Refresh kugira ngo signals_left igabanuke
