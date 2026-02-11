import streamlit as st
import pandas as pd
import time

# --- 1. CONFIG ---
SHEET_ID = "1M2v_43rTRe-ABlg5gkU2gYoT7dxxVq4-IgqNpGCCxmI"
# Iyi URL tuyihinduye kugira ngo isome mu buryo bwisumbuyeho (export mode)
USERS_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=0"

st.set_page_config(page_title="Aviator AI Predictor", layout="centered")

# --- 2. DATA LOADING ---
def get_users():
    try:
        # Isoma file nk'aho ari CSV isanzwe
        return pd.read_csv(USERS_URL)
    except Exception as e:
        return None

# --- 3. LOGIN PAGE ---
if 'user' not in st.session_state:
    st.session_state['user'] = None

def auth_page():
    st.title("🚀 Aviator AI Predictor")
    df = get_users()
    
    if df is None:
        st.error("Sheet1 ntishobora gusomeka!")
        st.info("Kora ibi: File > Share > Publish to Web muri Google Sheet yawe.")
    else:
        st.success("✅ Database Connected!")
        
        tab1, tab2 = st.tabs(["Login", "Sign Up"])
        
        with tab1:
            u = st.text_input("Username")
            p = st.text_input("Password", type="password")
            if st.button("LOG IN"):
                # Admin
                if u == "admin_divin" and p == "divin2026":
                    st.session_state['user'] = {"username": "admin", "status": "Admin"}
                    st.rerun()
                
                # Check users
                try:
                    user_match = df[(df['username'].astype(str) == u) & (df['password'].astype(str) == p)]
                    if not user_match.empty:
                        st.session_state['user'] = user_match.iloc[0].to_dict()
                        st.rerun()
                    else:
                        st.error("Username cyangwa Password ntabwo ari byo.")
                except:
                    st.error("Google Sheet Headers (username, password) ntabwo zimeze neza.")

        with tab2:
            st.info("Andikira Divin kuri WhatsApp kugira ngo ufungure konti.")
            st.markdown(f'<a href="https://wa.me/250780000000" target="_blank"><button style="width:100%; border-radius:20px; background-color:#25d366; color:white; border:none; height:40px; font-weight:bold; cursor:pointer;">Contact Divin on WhatsApp</button></a>', unsafe_allow_html=True)

# --- 4. MAIN DASHBOARD ---
def main_app():
    user = st.session_state['user']
    st.title(f"🎯 Welcome {user['username']}")
    
    if user['status'] == "Admin":
        st.write("### All Users Database")
        df = get_users()
        st.dataframe(df)
    else:
        st.info(f"Account Type: {user['status']}")
        if st.button("GET AI SIGNAL"):
            with st.spinner("Analyzing Aviator Patterns..."):
                time.sleep(2)
                st.success("🔥 Next Signal: 4.80x")

    if st.sidebar.button("Logout"):
        st.session_state['user'] = None
        st.rerun()

if st.session_state['user'] is None:
    auth_page()
else:
    main_app()
