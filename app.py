import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import time
from datetime import datetime

# --- 1. ADMIN SETTINGS ---
ADMIN_USER = "admin_divin"
ADMIN_PASS = "divin2026"
# Iyi link niyo App ikoresha - REBA NIBA ARIYO NEZA
SHEET_URL = "https://docs.google.com/spreadsheets/d/1M2v_43rTRe-ABlg5gkU2gYoT7dxxVq4-IgqNpGCCxmI/edit#gid=0"

st.set_page_config(page_title="Aviator AI Predictor", layout="wide")

# --- 2. CONNECTION FUNCTION (PERMANENT FIX) ---
def get_conn():
    try:
        # Gukoresha connection nshya buri gihe kugira ngo error itaguma muri cache
        return st.connection("gsheets", type=GSheetsConnection)
    except Exception as e:
        st.error(f"System Connection Error. Please refresh.")
        return None

def fetch_data(sheet_index=0):
    conn = get_conn()
    try:
        # Gusoma worksheet ikoresheje Index aho gukoresha Izina
        # Ibi bituma niyo worksheet yaba yitwa Sheet1 cyangwa Ishema, App iyibona
        return conn.read(spreadsheet=SHEET_URL, worksheet=sheet_index, ttl=0)
    except Exception as e:
        st.error(f"🚨 Permission Denied: Reba niba Robot Email ari 'Editor' muri Google Sheet.")
        st.stop()

# --- 3. LOGIN PAGE ---
if 'user' not in st.session_state:
    st.session_state['user'] = None

def auth_page():
    st.title("🚀 Aviator AI Predictor")
    tab1, tab2 = st.tabs(["Login", "Sign Up"])
    
    # Gusoma abakoresha muri Sheet ya mbere (Index 0)
    df = fetch_data(0)

    with tab1:
        u = st.text_input("Username")
        p = st.text_input("Password", type="password")
        if st.button("LOG IN"):
            if u == ADMIN_USER and p == ADMIN_PASS:
                st.session_state['user'] = {"username": "admin", "status": "Admin"}
                st.rerun()
            
            # Guhuza imyirondoro
            user_match = df[(df['username'].astype(str) == u) & (df['password'].astype(str) == p)]
            if not user_match.empty:
                st.session_state['user'] = user_match.iloc[0].to_dict()
                st.rerun()
            else:
                st.error("Username cyangwa Password ntabwo ari byo.")

    with tab2:
        st.subheader("Fungura Account (Free 3 Signals)")
        new_u = st.text_input("Username Nshya")
        new_p = st.text_input("Password Nshya", type="password")
        if st.button("REGISTER"):
            if new_u and new_p:
                if new_u in df['username'].values:
                    st.warning("Izina ryamaze gukoreshwa!")
                else:
                    new_row = pd.DataFrame([{"username": new_u, "password": new_p, "usage": 0, "status": "Trial"}])
                    updated_df = pd.concat([df, new_row], ignore_index=True)
                    # Gu-save-a muri Sheet ya mbere
                    conn = get_conn()
                    conn.update(spreadsheet=SHEET_URL, worksheet=0, data=updated_df)
                    st.success("Byakunze! Jya kuri Login winjire.")

# --- 4. MAIN APP ---
def main_app():
    user = st.session_state['user']
    df = fetch_data(0)
    
    st.sidebar.title(f"👤 {user['username']}")
    
    if user['status'] == "Admin":
        st.title("👨‍💻 Admin Control Panel")
        st.write("Abakoresha Bose:")
        st.dataframe(df) # Admin abona abantu bose muri Sheet
        
        if st.button("Refresh Data"):
            st.rerun()
    else:
        st.title("🏠 Member Dashboard")
        # Shaka amakuru y'umuntu winjiye
        u_info = df[df['username'].astype(str) == user['username']].iloc[0]
        
        col1, col2 = st.columns(2)
        col1.metric("Signals Used", f"{u_info['usage']}/3")
        col2.metric("Status", u_info['status'])
        
        if st.button("GET AI SIGNAL"):
            if u_info['status'] == "Trial" and int(u_info['usage']) >= 3:
                st.error("Trial yarangiye! Ishyura 5,000 RWF kuri Divin.")
            else:
                # Update usage
                if u_info['status'] == "Trial":
                    idx = df[df['username'].astype(str) == user['username']].index[0]
                    df.at[idx, 'usage'] = int(u_info['usage']) + 1
                    conn = get_conn()
                    conn.update(spreadsheet=SHEET_URL, worksheet=0, data=df)
                
                with st.spinner("Analyzing..."):
                    time.sleep(2)
                    st.success("🔥 Signal: 4.80x")

    if st.sidebar.button("Logout"):
        st.session_state['user'] = None
        st.rerun()

# --- RUN SYSTEM ---
if st.session_state['user'] is None:
    auth_page()
else:
    main_app()
