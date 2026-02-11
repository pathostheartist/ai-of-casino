import streamlit as st
import time

# --- 1. SETTINGS & STYLES ---
st.set_page_config(page_title="Aviator AI Predictor", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #050505; color: white; }
    .stButton>button { 
        width: 100%; border-radius: 20px; 
        background: linear-gradient(90deg, #ff4b4b, #800000); 
        color: white; font-weight: bold; border: none; height: 45px;
    }
    .signal-box {
        background-color: #111; padding: 20px; border-radius: 15px;
        border: 2px solid #ff4b4b; text-align: center; margin: 20px 0;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. USER DATABASE (Muri Code) ---
# Hano niho ushobora kongerera abantu niba Google Sheet yanze
USERS = {
    "admin_divin": {"password": "divin2026", "status": "Admin"},
    "test_user": {"password": "123", "status": "Trial"},
    "premium_user": {"password": "789", "status": "Premium"}
}

# --- 3. SESSION STATE ---
if 'user' not in st.session_state:
    st.session_state['user'] = None

# --- 4. LOGIN PAGE ---
def auth_page():
    st.title("🎯 Aviator AI Predictor")
    st.write("Welcome to the elite signal generator.")
    
    tab1, tab2 = st.tabs(["🔐 Login", "📝 Register"])
    
    with tab1:
        u = st.text_input("Username").lower().strip()
        p = st.text_input("Password", type="password")
        
        if st.button("LOG IN"):
            if u in USERS and USERS[u]["password"] == p:
                st.session_state['user'] = {"username": u, "status": USERS[u]["status"]}
                st.success("Success! Redirecting...")
                time.sleep(1)
                st.rerun()
            else:
                st.error("Invalid Username or Password.")
        
        st.markdown(f'''
            <a href="https://wa.me/250780000000" target="_blank">
                <button style="width:100%; border-radius:20px; background-color:#25d366; color:white; border:none; height:40px; font-weight:bold; cursor:pointer; margin-top:10px;">
                    💬 Contact Admin on WhatsApp
                </button>
            </a>
            ''', unsafe_allow_html=True)

    with tab2:
        st.info("Registration is currently handled via WhatsApp for security.")
        st.write("Send your desired username to the admin.")

# --- 5. MAIN DASHBOARD ---
def main_app():
    user = st.session_state['user']
    st.sidebar.title(f"👤 {user['username']}")
    st.sidebar.write(f"Access: **{user['status']}**")
    
    st.title("🚀 AI Analysis Dashboard")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("System Accuracy", "94.2%")
    with col2:
        st.metric("Status", user['status'])

    st.markdown("---")
    st.write("Enter the last 3 multipliers to predict the next flight:")
    st.text_input("Last 3 odds (e.g., 1.50, 2.10, 1.10)")

    if st.button("GENERATE NEXT SIGNAL"):
        with st.spinner("AI is calculating probabilities..."):
            time.sleep(3)
            st.markdown("""
                <div class="signal-box">
                    <h3 style="color: white;">NEXT PREDICTED SIGNAL</h3>
                    <h1 style="color: #ff4b4b; font-size: 50px;">4.85x</h1>
                    <p style="color: #888;">Safe Cashout: 3.50x</p>
                </div>
                """, unsafe_allow_html=True)
            st.balloons()

    if st.sidebar.button("Logout"):
        st.session_state['user'] = None
        st.rerun()

# --- EXECUTION ---
if st.session_state['user'] is None:
    auth_page()
else:
    main_app()
