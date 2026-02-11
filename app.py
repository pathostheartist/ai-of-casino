import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import time

# --- 1. SETTINGS & STYLE ---
st.set_page_config(page_title="Aviator AI - Admin System", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #050505; color: white; }
    .stButton>button { width: 100%; border-radius: 20px; background: linear-gradient(90deg, #00ffcc, #0088ff); color: black; font-weight: bold; }
    .premium-box { background-color: #1a1a1a; padding: 20px; border-radius: 15px; border: 1px solid #00ffcc; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATABASE CONNECTION ---
conn = st.connection("gsheets", type=GSheetsConnection)

def get_data():
    return conn.read(worksheet="Sheet1", ttl=0)

# --- 3. SESSION STATE ---
if 'user' not in st.session_state:
    st.session_state['user'] = None

# --- 4. AUTHENTICATION (SIGN UP & LOGIN) ---
def auth_page():
    st.title("🎯 Aviator AI Predictor")
    tab1, tab2 = st.tabs(["Login", "Sign Up (Free Trial)"])
    df = get_data()

    with tab1:
        u = st.text_input("Username")
        p = st.text_input("Password", type="password")
        if st.button("LOGIN"):
            user_match = df[(df['username'] == u) & (df['password'].astype(str) == p)]
            if not user_match.empty:
                st.session_state['user'] = user_match.iloc[0].to_dict()
                st.rerun()
            else:
                st.error("Wrong credentials!")

    with tab2:
        new_u = st.text_input("Choose Username")
        new_p = st.text_input("Choose Password", type="password")
        if st.button("REGISTER & GET 3 FREE SIGNALS"):
            if new_u and new_p:
                if new_u in df['username'].values:
                    st.warning("Username taken!")
                else:
                    # New user with 0 usage and Trial status
                    new_row = pd.DataFrame([{"username": new_u, "password": new_p, "usage": 0, "status": "Trial"}])
                    updated_df = pd.concat([df, new_row], ignore_index=True)
                    conn.update(worksheet="Sheet1", data=updated_df)
                    st.success("Account Created! Go to Login tab.")
            else:
                st.error("Fill all fields!")

# --- 5. ADMIN DASHBOARD (FOR DIVIN) ---
def admin_dashboard(df):
    st.title("👨‍C Admin Panel (Divin)")
    st.write("Manage Users & Payments")
    
    # Filter only Trial users who might have paid
    users_to_manage = df[df['username'] != 'admin']
    
    for index, row in users_to_manage.iterrows():
        col1, col2, col3 = st.columns([2, 2, 2])
        col1.write(f"**{row['username']}**")
        col2.write(f"Status: {row['status']} (Used: {row['usage']})")
        
        if row['status'] == 'Trial':
            if col3.button(f"Approve Premium", key=f"btn_{row['username']}"):
                df.at[index, 'status'] = 'Premium'
                conn.update(worksheet="Sheet1", data=df)
                st.success(f"{row['username']} is now Premium!")
                time.sleep(1)
                st.rerun()
    
    if st.button("Back to Predictions"):
        st.session_state['user']['username'] = 'admin_view' # Toggle view
        st.rerun()

# --- 6. USER PREDICTION DASHBOARD ---
def main_app():
    user = st.session_state['user']
    df = get_data()
    
    # Admin Special Access
    if user['username'] == 'admin':
        if st.sidebar.button("🛡️ OPEN ADMIN PANEL"):
            admin_dashboard(df)
            return

    # User Logic
    user_info = df[df['username'] == user['username']].iloc[0]
    usage = int(user_info['usage'])
    status = user_info['status']

    st.sidebar.title(f"Hello, {user['username']}")
    st.sidebar.write(f"Account: **{status}**")

    if status == "Trial" and usage >= 3:
        st.markdown("""
            <div class="premium-box">
                <h2 style="color:#ff4b4b;">Trial Expired! 🛑</h2>
                <p>Pay <b>5,000 RWF</b> to continue.</p>
                <p>MoMo: <b>078X XXX XXX (Divin)</b></p>
                <p>After payment, Admin will approve your account.</p>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.title("🎯 AI Signal Generator")
        if status == "Trial":
            st.info(f"Free Signals left: {3 - usage}")
        
        odds = st.text_input("Enter last 9 odds:")
        if st.button("GET SIGNAL"):
            if odds:
                if status == "Trial":
                    user_idx = df[df['username'] == user['username']].index[0]
                    df.at[user_idx, 'usage'] = usage + 1
                    conn.update(worksheet="Sheet1", data=df)
                
                with st.spinner("Analyzing..."):
                    time.sleep(1.5)
                    st.success("✅ Prediction: 3.90x (70% Confidence)")
            else:
                st.warning("Input odds first!")

    if st.sidebar.button("Logout"):
        st.session_state['user'] = None
        st.rerun()

# --- ROUTING ---
if st.session_state['user'] is None:
    auth_page()
else:
    main_app()
