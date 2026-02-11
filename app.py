import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import time
from datetime import datetime

# --- 1. ADMIN CREDENTIALS ---
ADMIN_USER = "admin_divin"
ADMIN_PASS = "divin2026"

st.set_page_config(page_title="Aviator AI Pro - Divin", layout="wide")

# Custom CSS for Dark Theme
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: white; }
    .stButton>button { width: 100%; border-radius: 20px; background: linear-gradient(90deg, #ff4b4b, #800000); color: white; font-weight: bold; border: none; height: 45px; }
    .nav-card { background-color: #111; padding: 15px; border-radius: 10px; border-left: 5px solid #ff4b4b; margin-bottom: 10px;}
    .notif-card { background-color: #1a1a1a; padding: 10px; border-radius: 5px; border-bottom: 1px solid #333; margin-bottom: 5px; font-size: 0.85rem; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. CONNECTION ---
SHEET_URL = "https://docs.google.com/spreadsheets/d/1M2v_43rTRe-ABlg5gkU2gYoT7dxxVq4-IgqNpGCCxmI/edit#gid=0"

try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    
    def get_data(sheet_name="Sheet1"):
        # ttl=0 ituma buri gihe asoma amakuru mashya
        return conn.read(spreadsheet=SHEET_URL, worksheet=sheet_name, ttl=0)
except Exception as e:
    st.error("⚠️ Connection Error. Check your Google Sheet Permissions.")
    st.stop()

def add_log(user, action):
    try:
        # Hano twahinduye izina rikaba Sheet2 nk'uko wabinsabye
        logs_df = get_data("Sheet2")
        new_log = pd.DataFrame([{"time": datetime.now().strftime("%H:%M:%S"), "user": user, "action": action}])
        updated_logs = pd.concat([logs_df, new_log], ignore_index=True)
        conn.update(spreadsheet=SHEET_URL, worksheet="Sheet2", data=updated_logs)
    except:
        pass

# --- 3. SESSION STATE ---
if 'user' not in st.session_state:
    st.session_state['user'] = None

# --- 4. AUTHENTICATION ---
def auth_page():
    st.title("🎯 Aviator AI Predictor")
    t1, t2 = st.tabs(["Login", "Sign Up"])
    
    try:
        df = get_data("Sheet1")
    except:
        st.error("Check if the Robot Email is an 'Editor' in your Google Sheet.")
        return

    with t1:
        u = st.text_input("Username")
        p = st.text_input("Password", type="password")
        if st.button("LOG IN"):
            if u == ADMIN_USER and p == ADMIN_PASS:
                st.session_state['user'] = {"username": "admin", "status": "Admin"}
                add_log("ADMIN", "Logged In")
                st.rerun()
            
            user_match = df[(df['username'] == u) & (df['password'].astype(str) == p)]
            if not user_match.empty:
                st.session_state['user'] = user_match.iloc[0].to_dict()
                add_log(u, "Logged In")
                st.rerun()
            else:
                st.error("Invalid credentials!")

    with t2:
        new_u = st.text_input("New Username")
        new_p = st.text_input("New Password", type="password")
        if st.button("REGISTER"):
            if new_u and new_p:
                if new_u in df['username'].values:
                    st.warning("Username taken!")
                else:
                    new_user = pd.DataFrame([{"username": new_u, "password": new_p, "usage": 0, "status": "Trial"}])
                    updated_df = pd.concat([df, new_user], ignore_index=True)
                    conn.update(spreadsheet=SHEET_URL, worksheet="Sheet1", data=updated_df)
                    add_log(new_u, "Registered")
                    st.success("Account Created! Go to Login.")

# --- 5. MAIN APP ---
def main_app():
    user = st.session_state['user']
    df = get_data("Sheet1")
    
    st.sidebar.title(f"👤 {user['username']}")
    
    if user['status'] == "Admin":
        menu = st.sidebar.radio("Navigation", ["Admin Panel", "System Logs"])
    else:
        menu = st.sidebar.radio("Navigation", ["Dashboard", "Get Signal"])

    if menu == "Admin Panel":
        st.title("👨‍💻 Admin Control Panel")
        users = df[df['username'] != 'admin']
        for i, row in users.iterrows():
            c1, c2, c3, c4 = st.columns([2,1,1,1])
            c1.write(f"**{row['username']}**")
            c2.write(row['status'])
            if row['status'] == 'Trial' and c3.button("Approve", key=f"ap_{i}"):
                df.at[i, 'status'] = 'Premium'
                conn.update(spreadsheet=SHEET_URL, worksheet="Sheet1", data=df)
                st.rerun()
            if c4.button("🗑️", key=f"del_{i}"):
                df = df.drop(i)
                conn.update(spreadsheet=SHEET_URL, worksheet="Sheet1", data=df)
                add_log("ADMIN", f"Deleted {row['username']}")
                st.rerun()

    elif menu == "System Logs":
        st.title("🔔 Real-Time Activities")
        try:
            logs = get_data("Sheet2").iloc[::-1]
            for _, log in logs.head(15).iterrows():
                st.markdown(f'<div class="notif-card"><b>[{log["time"]}]</b> {log["user"]}: {log["action"]}</div>', unsafe_allow_html=True)
        except:
            st.info("Make sure you have a 'Sheet2' tab for logs.")

    elif menu == "Dashboard":
        st.title("🏠 Dashboard")
        u_info = df[df['username'] == user['username']].iloc[0]
        st.write(f"Account: **{u_info['status']}** | Usage: **{u_info['usage']}/3**")

    elif menu == "Get Signal":
        st.title("🎯 AI Analyzer")
        u_info = df[df['username'] == user['username']].iloc[0]
        if u_info['status'] == "Trial" and int(u_info['usage']) >= 3:
            st.error("Trial Expired!")
        else:
            if st.button("RUN PREDICTION"):
                if u_info['status'] == "Trial":
                    idx = df[df['username'] == user['username']].index[0]
                    df.at[idx, 'usage'] = int(u_info['usage']) + 1
                    conn.update(spreadsheet=SHEET_URL, worksheet="Sheet1", data=df)
                    add_log(user['username'], "Used Signal")
                st.success("🔥 Signal: 4.80x")

    if st.sidebar.button("Logout"):
        st.session_state['user'] = None
        st.rerun()

if st.session_state['user'] is None:
    auth_page()
else:
    main_app()
