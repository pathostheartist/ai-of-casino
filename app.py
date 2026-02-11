import streamlit as st
import pandas as pd
import time

# --- CONFIG ---
# Reba neza ko iyi ID ariyo yawe
SHEET_ID = "1M2v_43rTRe-ABlg5gkU2gYoT7dxxVq4-IgqNpGCCxmI"
# Iyi URL tuyihinduye kugira ngo isome 'Sheet1' hatagendewe kuri gid gusa
USERS_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=Sheet1"

st.set_page_config(page_title="Aviator AI Predictor", layout="centered")

def get_users():
    try:
        # Isoma file ikoresheje uburyo bwa kinyamwuga (engine python)
        df = pd.read_csv(USERS_URL, on_bad_lines='skip')
        df.columns = [c.lower().strip() for c in df.columns]
        return df
    except Exception as e:
        return None

# --- AUTH LOGIC ---
if 'user' not in st.session_state:
    st.session_state['user'] = None

df = get_users()

st.title("🚀 Aviator AI Predictor")

if df is None:
    st.error("❌ Sheet1 ntishobora gusomeka!")
    st.info("Icyo ugomba gukora:")
    st.write("1. Jya muri Google Sheet > File > Share > **Publish to Web**.")
    st.write("2. Reba niba ishiti yawe yitwa **Sheet1** (Hasi ibumoso).")
    st.write("3. Reba niba Row 1 irimo: **username**, **password**, **usage**, **status**.")
    if st.button("Gerageza Nanone"):
        st.rerun()
else:
    st.success("✅ Database Connected!")
    
    if st.session_state['user'] is None:
        tab1, tab2 = st.tabs(["Login", "Sign Up"])
        with tab1:
            u = st.text_input("Username").lower().strip()
            p = st.text_input("Password", type="password")
            if st.button("LOG IN"):
                if u == "admin_divin" and p == "divin2026":
                    st.session_state['user'] = {"username": "admin", "status": "Admin"}
                    st.rerun()
                
                if 'username' in df.columns:
                    user_match = df[(df['username'].astype(str).str.lower() == u) & (df['password'].astype(str) == p)]
                    if not user_match.empty:
                        st.session_state['user'] = user_match.iloc[0].to_dict()
                        st.rerun()
                    else:
                        st.error("Username cyangwa Password ntabwo ari byo.")
        with tab2:
            st.info("Kugira ngo ufungure account, andikira Divin kuri WhatsApp.")
            st.markdown(f'<a href="https://wa.me/250780000000" target="_blank"><button style="width:100%; border-radius:20px; background-color:#25d366; color:white; border:none; height:40px; font-weight:bold; cursor:pointer;">WhatsApp Admin</button></a>', unsafe_allow_html=True)
    else:
        # DASHBOARD
        user = st.session_state['user']
        st.write(f"### Welcome {user['username']}")
        if st.button("GET SIGNAL"):
            with st.spinner("Analyzing..."):
                time.sleep(2)
                st.success("🔥 Prediction: 4.80x")
        if st.sidebar.button("Logout"):
            st.session_state['user'] = None
            st.rerun()
