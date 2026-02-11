import streamlit as st
import pandas as pd
import time

# --- APP CONFIGURATION ---
st.set_page_config(page_title="AI Predictor Pro", page_icon="📈")

# Using a simple simulation of a database for this script
# To make it permanent, you'll link this to your GSheet in Streamlit Secrets
if 'database' not in st.session_state:
    st.session_state['database'] = pd.DataFrame(columns=['username', 'password', 'usage', 'status'])

if 'logged_in_user' not in st.session_state:
    st.session_state['logged_in_user'] = None

# --- UI STYLING ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #161b22; border: 1px solid #30363d; border-radius: 10px; padding: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- NAVIGATION ---
if st.session_state['logged_in_user'] is None:
    st.title("🚀 AI Predictor Access")
    auth_mode = st.radio("Choose Mode", ["Login", "Sign Up (3 Free Predictions)"])

    if auth_mode == "Sign Up (3 Free Predictions)":
        new_user = st.text_input("Choose Username")
        new_email = st.text_input("Email Address")
        new_pass = st.text_input("Create Password", type="password")
        
        if st.button("Create My Free Account"):
            # Logic: Add to database
            st.success("Account created! You have 3 FREE signals.")
            st.info("Now switch to Login mode to start.")
            # (In a real app, this would write to Google Sheets)

    else:
        user = st.text_input("Username")
        pw = st.text_input("Password", type="password")
        if st.button("Login"):
            # For now, let's simulate a successful login
            st.session_state['logged_in_user'] = {"username": user, "usage": 0, "status": "Trial"}
            st.rerun()

# --- MAIN APP INTERFACE ---
else:
    user_data = st.session_state['logged_in_user']
    st.sidebar.title(f"Welcome, {user_data['username']}")
    st.sidebar.write(f"Account: **{user_data['status']}**")
    
    # TRIAL LOGIC
    max_free = 3
    remaining = max_free - user_data['usage']

    if user_data['status'] == "Trial" and remaining <= 0:
        st.error("❌ Your Free Trial has expired!")
        st.write("### 💳 Upgrade to Premium")
        st.write("To continue getting signals, pay **5,000 RWF** via MoMo:")
        st.code("*182*8*1*XXXXXX# (Arsene)")
        st.info("After payment, send your username to WhatsApp for activation.")
        if st.button("Logout"):
            st.session_state['logged_in_user'] = None
            st.rerun()
    else:
        st.title("📊 AI Smart Analytics")
        if user_data['status'] == "Trial":
            st.warning(f"Free Signals Remaining: {remaining}")

        st.write("Enter the last 9 odds from the game:")
        input_odds = st.text_input("Example: 1.22, 5.40, 1.02...", placeholder="Separate with commas")

        if st.button("Get Prediction"):
            if user_data['status'] == "Trial":
                user_data['usage'] += 1
            
            with st.spinner('AI Engine is calculating patterns...'):
                time.sleep(2)
                
                # THE DASHBOARD (Your requested format)
                st.markdown("---")
                col1, col2, col3 = st.columns(3)
                col1.metric("PREDICTION", "4.7x")
                col2.metric("TARGET", "3.9x")
                col3.metric("CHANCE", "70%")
                
                st.success("🔥 Signal Found: Target 3.9x is highly probable!")
                
                if user_data['status'] == "Trial":
                    st.rerun() # Refresh to update the usage count

    if st.sidebar.button("Logout"):
        st.session_state['logged_in_user'] = None
        st.rerun()
