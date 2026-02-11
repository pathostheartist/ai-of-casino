import streamlit as st
import pandas as pd
import time

# --- CONFIG ---
# Iyi ID ni yawe, ntuyihindure
SHEET_ID = "1M2v_43rTRe-ABlg5gkU2gYoT7dxxVq4-IgqNpGCCxmI"

# Ubu buryo bwa URL bukora kuri buri Sheet yose yafunguriwe 'Anyone with the link'
USERS_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

st.set_page_config(page_title="Aviator AI Predictor", layout="centered")

# Custom Styling kugira ngo App ise neza
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    .stButton>button { width: 100%; border-radius: 10px; background-color: #ff4b4b; color: white; }
    </style>
    """, unsafe_allow_html=True)

def get_users():
    try:
        # Isoma amakuru mu buryo bworoheje
        data = pd.read_csv(USERS_URL)
        # Guhindura inkingi (Headers) zose kuba inyuguti nto
        data.columns = [str(c).lower().strip() for c in data.columns]
        return data
    except Exception as e:
        st.error(f"Error: {e}")
        return None

# --- AUTHENTICATION ---
if 'user' not in st.session_state:
    st.session_state['user'] = None

df = get_users()

st.title("🚀 Aviator AI Predictor")

if df is not None:
    # Niba hari ikibazo mu nkingi (Headers), izi ni izo dushaka
    required_columns = ['username', 'password']
    
    # Reba niba headers zihuye
    if all(col in df.columns for col in required_columns):
        if st.session_state['user'] is None:
            tab1, tab2 = st.tabs(["Login", "Sign Up"])
            
            with tab1:
                u = st.text_input("Username").lower().strip()
                p = st.text_input("Password", type="password")
                if st.button("LOG IN"):
                    # Admin Login
                    if u == "admin_divin" and p == "divin2026":
                        st.session_state['user'] = {"username": "admin", "status": "Admin"}
                        st.rerun()
                    
                    # User Login
                    user_match = df[(df['username'].astype(str).str.lower() == u) & (df['password'].astype(str) == p)]
                    if not user_match.empty:
                        st.session_state['user'] = user_match.iloc[0].to_dict()
                        st.rerun()
                    else:
                        st.error("Username cyangwa Password ntabwo ari byo.")
            
            with tab2:
                st.info("Kugira ngo ufungure account, andikira Divin kuri WhatsApp.")
                st.markdown(f'<a href="https://wa.me/250780000000" target="_blank"><button style="padding:10px; border-radius:10px; background-color:#25d366; color:white; border:none; width:100%; cursor:pointer; font-weight:bold;">Contact Admin (WhatsApp)</button></a>', unsafe_allow_html=True)
        
        else:
            # DASHBOARD NYIRIZINA
            user = st.session_state['user']
            st.success(f"Murakaza neza, {user['username']}!")
            st.write(f"Account Status: **{user.get('status', 'Trial')}**")
            
            if st.button("GET NEXT SIGNAL"):
                with st.spinner("AI is analyzing trends..."):
                    time.sleep(2)
                    st.success("🔥 Next Signal: 4.80x")
            
            if st.sidebar.button("Logout"):
                st.session_state['user'] = None
                st.rerun()
    else:
        st.warning("⚠️ Headers za Google Sheet ntabwo zimeze neza.")
        st.write("Muri Row 1 andika: **username**, **password**, **usage**, **status**")
        st.write("Inkingi ubu zihari ni:", list(df.columns))
else:
    st.error("❌ Porogaramu yanze gusoma Google Sheet.")
    st.info("Uzuza ibi bikurikira:")
    st.write("1. Kanda **Share** muri Google Sheet > **Anyone with the link** (Editor).")
    st.write("2. Jya muri **File** > **Share** > **Publish to Web**.")
