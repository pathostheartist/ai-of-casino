import streamlit as st
import pandas as pd
import time

# --- 1. SETTINGS ---
# Iyi link ihinduremo CSV kugira ngo isomeke nta robot ikenewe
SHEET_ID = "1M2v_43rTRe-ABlg5gkU2gYoT7dxxVq4-IgqNpGCCxmI"
# URL ya Sheet1 (Users)
USERS_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=Sheet1"
# URL ya Sheet2 (Logs)
LOGS_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=Sheet2"

st.set_page_config(page_title="Aviator AI Predictor", layout="wide")

# --- 2. DATA FUNCTIONS ---
def get_users():
    try:
        return pd.read_csv(USERS_URL)
    except:
        st.error("Sheet1 ntishobora gusomeka. Reba niba 'Anyone with the link' iriho.")
        return None

# --- 3. LOGIN PAGE ---
if 'user' not in st.session_state:
    st.session_state['user'] = None

def auth_page():
    st.title("🚀 Aviator AI Predictor")
    df = get_users()
    
    if df is not None:
        tab1, tab2 = st.tabs(["Login", "Sign Up"])
        
        with tab1:
            u = st.text_input("Username")
            p = st.text_input("Password", type="password")
            if st.button("LOG IN"):
                # Admin bypass
                if u == "admin_divin" and p == "divin2026":
                    st.session_state['user'] = {"username": "admin", "status": "Admin"}
                    st.rerun()
                
                # User check
                user_match = df[(df['username'].astype(str) == u) & (df['password'].astype(str) == p)]
                if not user_match.empty:
                    st.session_state['user'] = user_match.iloc[0].to_dict()
                    st.rerun()
                else:
                    st.error("Ntabwo ari byo!")

        with tab2:
            st.info("Kugira ngo wiyandikishe, andikira Divin kuri WhatsApp.")
            st.markdown(f'<a href="https://wa.me/250780000000" target="_blank"><button style="width:100%; border-radius:20px; background-color:#25d366; color:white; border:none; height:40px; font-weight:bold;">Contact Divin</button></a>', unsafe_allow_html=True)

# --- 4. MAIN APP ---
def main_app():
    user = st.session_state['user']
    st.sidebar.title(f"👤 {user['username']}")
    
    if user['status'] == "Admin":
        st.title("👨‍💻 Admin Panel")
        df = get_users()
        st.write("Abakoresha Bose:")
        st.dataframe(df)
    else:
        st.title("🏠 Member Dashboard")
        st.success(f"Murakaza neza, {user['username']}!")
        if st.button("GET AI SIGNAL"):
            with st.spinner("Analyzing..."):
                time.sleep(2)
                st.write("🔥 Next Signal: 3.50x")

    if st.sidebar.button("Logout"):
        st.session_state['user'] = None
        st.rerun()

if st.session_state['user'] is None:
    auth_page()
else:
    main_app()
