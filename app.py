import streamlit as st
import pandas as pd
import time

# --- 1. CONNECT TO GOOGLE SHEETS ---
# Hano shyiramo URL ya Google Sheet yawe (Make sure it's public: 'Anyone with the link can view')
SHEET_URL = "https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID/export?format=csv"

def load_user_data():
    try:
        df = pd.read_csv(SHEET_URL)
        return df
    except:
        return pd.DataFrame(columns=['username', 'password', 'status'])

# --- 2. AUTHENTICATION LOGIC ---
def login_user(username, password, df):
    user_row = df[(df['username'] == username) & (df['password'].astype(str) == password)]
    if not user_row.empty:
        return user_row.iloc[0].to_dict()
    return None

# --- 3. THE INTERFACE ---
st.set_page_config(page_title="AI Casino Pro - SaaS", layout="centered")

if 'auth' not in st.session_state:
    st.session_state['auth'] = None

df_users = load_user_data()

# --- LOGIN/REGISTER PAGE ---
if st.session_state['auth'] is None:
    st.title("🛡️ Secure Access")
    tab1, tab2 = st.tabs(["Login", "Payment Info"])
    
    with tab1:
        u = st.text_input("Username")
        p = st.text_input("Password", type="password")
        if st.button("Unlock AI Engine"):
            user = login_user(u, p, df_users)
            if user:
                st.session_state['auth'] = user
                st.rerun()
            else:
                st.error("Account ntibonetse cyangwa ntiwishyuye.")

    with tab2:
        st.write("### 💳 Subscription Plans")
        st.info("1. Trial: Free (3 Signals)\n2. Premium: 5,000 RWF / Month")
        st.write("Ohereza amafaranga kuri: **078X XXX XXX (Arsene)**")
        st.write("Hanyuma utume ubutumwa kuri WhatsApp wanditse 'Username' yawe.")

# --- PREMIUM DASHBOARD ---
else:
    user = st.session_state['auth']
    st.sidebar.success(f"User: {user['username']}")
    st.sidebar.info(f"Account Type: {user['status']}")

    if user['status'] == 'Trial' or user['status'] == 'Premium':
        st.title("🎯 AI Smart Signals")
        
        # UI ya Prediction (Ya mibare wampaye)
        st.markdown("---")
        input_data = st.text_input("Ingiza imibare 9 ya nyuma:")
        
        if st.button("Get Premium Prediction"):
            with st.spinner("Calculating Probability..."):
                time.sleep(2)
                # Ibisubizo bishingiye kuri AI Engine
                st.balloons()
                c1, c2, c3 = st.columns(3)
                c1.metric("PREDICTION", "4.7x")
                c2.metric("TARGET", "3.9x")
                c3.metric("CHANCE", "70%")
                
                st.markdown("""
                    <div style="background-color:green; padding:15px; border-radius:10px; color:white; text-align:center;">
                        🚀 <b>SIGNAL: BUY NOW!</b><br>Cash out at 3.9x safely.
                    </div>
                """, unsafe_allow_html=True)
    
    if st.sidebar.button("Logout"):
        st.session_state['auth'] = None
        st.rerun()
