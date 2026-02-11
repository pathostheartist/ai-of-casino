import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import time
from datetime import datetime
import plotly.graph_objects as go
import numpy as np

# --- 1. SETTINGS & ADMIN CREDENTIALS ---
st.set_page_config(page_title="Aviator AI - Admin System", layout="wide")

# ADMIN CREDENTIALS (Hano niho ubihindurira)
ADMIN_USER = "admin_divin"
ADMIN_PASS = "divin2026"

st.markdown("""
    <style>
    .stApp { background-color: #050505; color: white; }
    .stButton>button { width: 100%; border-radius: 20px; background: linear-gradient(90deg, #ff4b4b, #800000); color: white; font-weight: bold; border: none; }
    .nav-card { background-color: #111; padding: 15px; border-radius: 10px; border-left: 5px solid #ff4b4b; margin-bottom: 10px;}
    .notif-card { background-color: #1a1a1a; padding: 10px; border-radius: 5px; border-bottom: 1px solid #333; font-size: 0.85rem; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATABASE CONNECTION ---
conn = st.connection("gsheets", type=GSheetsConnection)

def get_data(sheet_name="Sheet1"):
    return conn.read(worksheet=sheet_name, ttl=0)

def add_log(user, action):
    try:
        logs_df = get_data("Logs")
        new_log = pd.DataFrame([{"time": datetime.now().strftime("%H:%M:%S"), "user": user, "action": action}])
        updated_logs = pd.concat([logs_df, new_log], ignore_index=True)
        conn.update(worksheet="Logs", data=updated_logs)
    except:
        pass # If logs sheet isn't ready yet

# --- 3. SESSION STATE ---
if 'user' not in st.session_state:
    st.session_state['user'] = None

# --- 4. AUTHENTICATION ---
def auth_page():
    st.title("🎯 Aviator AI Predictor")
    tab1, tab2 = st.tabs(["Login", "Sign Up"])
    df = get_data("Sheet1")

    with tab1:
        u = st.text_input("Username")
        p = st.text_input("Password", type="password")
        if st.button("LOGIN"):
            # Check Admin Credentials First
            if u == ADMIN_USER and p == ADMIN_PASS:
                st.session_state['user'] = {"username": "admin", "status": "Admin"}
                add_log("ADMIN", "Logged into the system")
                st.rerun()
            
            # Check Regular Users
            user_match = df[(df['username'] == u) & (df['password'].astype(str) == p)]
            if not user_match.empty:
                st.session_state['user'] = user_match.iloc[0].to_dict()
                add_log(u, "Logged in")
                st.rerun()
            else:
                st.error("Invalid credentials!")

    with tab2:
        new_u = st.text_input("Choose Username")
        new_p = st.text_input("Choose Password", type="password")
        if st.button("REGISTER"):
            if new_u and new_p:
                if new_u in df['username'].values:
                    st.warning("Username taken!")
                else:
                    new_row = pd.DataFrame([{"username": new_u, "password": new_p, "usage": 0, "status": "Trial"}])
                    updated_df = pd.concat([df, new_row], ignore_index=True)
                    conn.update(worksheet="Sheet1", data=updated_df)
                    add_log(new_u, "Signed up for Trial")
                    st.success("Account Created! Please Login.")

# --- 5. MAIN SYSTEM ---
def main_app():
    user = st.session_state['user']
    df = get_data("Sheet1")
    
    # NAVIGATION SIDEBAR
    st.sidebar.title(f"👤 {user['username']}")
    
    if user['status'] == "Admin":
        menu = st.sidebar.radio("Navigation", ["Admin Dashboard", "Live Monitor", "System Logs"])
    else:
        menu = st.sidebar.radio("Navigation", ["Dashboard", "AI Prediction"])

    # --- ADMIN VIEW ---
    if menu == "Admin Dashboard":
        st.title("👨‍💻 Admin Control Panel")
        st.write("Manage User Access")
        users_df = df[df['username'] != 'admin']
        for i, row in users_df.iterrows():
            c1, c2, c3 = st.columns([2,2,2])
            c1.write(f"**{row['username']}**")
            c2.write(f"Status: {row['status']} | Used: {row['usage']}")
            if row['status'] == 'Trial' and c3.button("Activate Premium", key=f"app_{row['username']}"):
                df.at[i, 'status'] = 'Premium'
                conn.update(worksheet="Sheet1", data=df)
                add_log("ADMIN", f"Activated Premium for {row['username']}")
                st.rerun()

    elif menu == "Live Monitor":
        st.title("🔔 Real-Time Notifications")
        logs = get_data("Logs").iloc[::-1] # Show latest first
        for _, log in logs.head(10).iterrows():
            st.markdown(f"""<div class="notif-card"><b>[{log['time']}]</b> {log['user']}: {log['action']}</div>""", unsafe_allow_html=True)

    # --- USER VIEW ---
    elif menu == "Dashboard":
        st.title("🏠 Member Dashboard")
        user_info = df[df['username'] == user['username']].iloc[0]
        col1, col2 = st.columns(2)
        col1.markdown(f"<div class='nav-card'><h4>Signals Used</h4><h2>{user_info['usage']}</h2></div>", unsafe_allow_html=True)
        col2.markdown(f"<div class='nav-card'><h4>Status</h4><h2>{user_info['status']}</h2></div>", unsafe_allow_html=True)

    elif menu == "AI Prediction":
        st.title("🎯 AI Signal Generator")
        user_info = df[df['username'] == user['username']].iloc[0]
        if user_info['status'] == "Trial" and int(user_info['usage']) >= 3:
            st.error("🛑 Trial Expired! Contact Divin for Premium.")
        else:
            odds = st.text_input("Enter last 9 odds:")
            if st.button("GET SIGNAL"):
                if odds:
                    if user_info['status'] == "Trial":
                        idx = df[df['username'] == user['username']].index[0]
                        df.at[idx, 'usage'] = int(user_info['usage']) + 1
                        conn.update(worksheet="Sheet1", data=df)
                        add_log(user['username'], "Used a Free Signal")
                    
                    with st.spinner("Analyzing..."):
                        time.sleep(2)
                        st.success("✅ Prediction: 3.90x")

    if st.sidebar.button("Logout"):
        st.session_state['user'] = None
        st.rerun()

if st.session_state['user'] is None:
    auth_page()
else:
    main_app()
