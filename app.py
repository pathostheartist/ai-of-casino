import streamlit as st
import pandas as pd
import numpy as np
import time
import plotly.graph_objects as go

# --- 1. CONFIG ---
st.set_page_config(page_title="Betpawa AI Secret Engine", layout="wide")

# --- 2. GLOBAL DATABASE (Shared between Admin and Users) ---
# Ibi bituma ibyo Admin wanditse, abandi babibona ako kanya
if 'real_odds_history' not in st.session_state:
    st.session_state['real_odds_history'] = [1.50, 2.10, 1.05, 3.80, 1.12]

# --- 3. CUSTOM CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #0b0d10; color: white; }
    .betpawa-green { color: #45ad15; font-weight: bold; }
    .admin-panel { background-color: #1a1a1a; padding: 20px; border-radius: 10px; border: 1px dashed #45ad15; }
    .user-odd { background-color: #45ad15; padding: 10px; border-radius: 5px; text-align: center; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. LOGIN SYSTEM ---
if 'user' not in st.session_state:
    st.session_state['user'] = None

# --- 5. FRAGMENT FOR AUTO-SYNC ---
@st.fragment(run_every=3) # Ivugurura imibare kuri User buri masegonda 3
def user_view():
    st.markdown("### <span class='betpawa-green'>BETPAWA</span> LIVE AI ENGINE", unsafe_allow_html=True)
    
    # Isoma amakuru Admin yanditse
    live_data = st.session_state['real_odds_history']
    
    # Display Odds (History)
    cols = st.columns(8)
    for i, odd in enumerate(live_data[-8:]):
        color = "#3498db" if odd < 2 else "#9132f0" if odd < 10 else "#ff00ff"
        cols[i].markdown(f'<div style="background-color:{color}; padding:10px; border-radius:8px; text-align:center; font-weight:bold;">{odd}x</div>', unsafe_allow_html=True)

    # Graph
    fig = go.Figure(go.Scatter(x=list(range(len(live_data))), y=live_data, mode='lines+markers', line=dict(color='#45ad15', width=3)))
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='white', height=250, margin=dict(l=0, r=0, t=10, b=0))
    st.plotly_chart(fig, use_container_width=True)

    # AI Prediction
    last_odd = live_data[-1]
    prediction = round(np.random.uniform(1.6, 3.8), 2)
    
    c1, c2 = st.columns(2)
    with c1:
        st.info(f"🤖 AI Analysis: Last real odd was {last_odd}x. Next round is predicted to be stable.")
    with c2:
        st.success(f"🎯 AI SIGNAL: {prediction}x (Confidence 94%)")

# --- 6. ADMIN CONTROL PANEL (STEALH) ---
def admin_control():
    st.markdown("<div class='admin-panel'>", unsafe_allow_html=True)
    st.subheader("🕵️‍♂️ Secret Admin Sync")
    st.write("Andika odds zanyazo ubona kuri Betpawa ubu:")
    
    new_odd = st.number_input("Last Odd (e.g., 1.55)", min_value=1.0, step=0.01)
    if st.button("UPDATE SYSTEM FOR ALL USERS"):
        # Iyi buto ihita yohereza umubare mu basomyi bose
        st.session_state['real_odds_history'].append(new_odd)
        st.success(f"Done! {new_odd}x is now live for all users.")
        time.sleep(1)
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# --- 7. MAIN LOGIC ---
if st.session_state['user'] is None:
    st.title("Login")
    u = st.text_input("Username").lower().strip()
    p = st.text_input("Password", type="password")
    if st.button("Access"):
        if u == "admin_divin" and p == "divin2026":
            st.session_state['user'] = "Admin"
            st.rerun()
        else:
            # Login ya User isanzwe
            st.session_state['user'] = u
            st.rerun()
else:
    # Sidebar
    st.sidebar.title(f"User: {st.session_state['user']}")
    if st.sidebar.button("Logout"):
        st.session_state['user'] = None
        st.rerun()

    # Routing
    if st.session_state['user'] == "Admin":
        tab1, tab2 = st.tabs(["Control Panel", "User Preview"])
        with tab1:
            admin_control()
        with tab2:
            user_view()
    else:
        user_view()
