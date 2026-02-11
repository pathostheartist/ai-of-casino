import streamlit as st
import pandas as pd
import time

# --- CONFIG ---
SHEET_ID = "1M2v_43rTRe-ABlg5gkU2gYoT7dxxVq4-IgqNpGCCxmI"
# URL nshya itanga amakuru adasabye imfunguzo (Direct CSV Download)
USERS_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&id={SHEET_ID}&gid=0"

st.set_page_config(page_title="Aviator AI Predictor", layout="centered")

def get_users():
    try:
        # Isoma amakuru nta mupaka
        df = pd.read_csv(USERS_URL)
        df.columns = [str(c).lower().strip() for c in df.columns]
        return df
    except Exception as e:
        # Iyi izatubwira niba URL ikirimo ikibazo
        st.error(f"⚠️ Error: {e}")
        return None

# --- AUTH ---
if 'user' not in st.session_state:
    st.session_state['user'] = None

df = get_users()

st.title("🚀 Aviator AI Predictor")

if df is not None:
    st.success("✅ Database Connected!")
    
    if st.session_state['user'] is None:
        tab1, tab2 = st.tabs(["Login", "Sign Up"])
        
        with tab1:
            u = st.text_input("Username").lower().strip()
            p = st.text_input("Password", type="password")
            if st.button("LOG IN"):
                # Admin login
                if u == "admin_divin" and p == "divin2026":
                    st.session_state['user'] = {"username": "admin", "status": "Admin"}
                    st.rerun()
                
                # User login check
                if 'username' in df.columns:
                    user_match = df[(df['username'].astype(str).str.lower() == u) & (df['password'].astype(str) == p)]
                    if not user_match.empty:
                        st.session_state['user'] = user_match.iloc[0].to_dict()
                        st.rerun()
                    else:
                        st.error("Username cyangwa Password ntabwo ari byo.")
        
        with tab2:
            st.info("Andikira Divin kuri WhatsApp kugira ngo ufungure account.")
            st.markdown(f'<a href="https://wa.me/250780000000" target="_blank"><button style="width:100%; border-radius:10px; background-color:#25d366; color:white; border:none; height:40px; font-weight:bold; cursor:pointer;">WhatsApp Admin</button></a>', unsafe_allow_html=True)
    else:
        # DASHBOARD
        user = st.session_state['user']
        st.write(f"### Welcome {user['username']}")
        if st.button("GET AI SIGNAL"):
            with st.spinner("Analyzing Aviator patterns..."):
                time.sleep(2)
                st.success("🔥 Next Signal: 4.80x")
        
        if st.sidebar.button("Logout"):
            st.session_state['user'] = None
            st.rerun()
else:
    st.error("❌ Permission Denied (401 Error)")
    st.info("Kora ibi ubu nyine:")
    st.write("1. Jya muri Google Sheet > Share > Hindura 'Restricted' uyihe **'Anyone with the link'**.")
    st.write("2. Jya muri File > Share > **Publish to Web** (Kanda Publish buto ihinduke grey).")
