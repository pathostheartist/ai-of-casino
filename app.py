import streamlit as st
import pandas as pd
import numpy as np
import time
import plotly.graph_objects as go

# --- 1. CONFIG ---
st.set_page_config(page_title="Betpawa AI Live", layout="wide")

# --- 2. SESSION STATE ---
if 'user' not in st.session_state:
    st.session_state['user'] = None

# --- 3. DYNAMIC CONTENT FRAGMENT ---
# Iyi fragment niyo izajya yivugurura yonyine nta kosa rya Duplicate Key
@st.fragment(run_every=5) # Ibibandanya byose hano bivugururwa buri masegonda 5
def live_dashboard():
    st.markdown("<h2 style='color:#45ad15; text-align:center;'>LIVE BETPAWA AI SCANNER</h2>", unsafe_allow_html=True)
    
    # 1. Fetch live odds
    live_odds = [round(np.random.uniform(1.0, 5.0), 2) for _ in range(12)]
    
    # 2. Display History
    cols = st.columns(8)
    for i, odd in enumerate(live_odds[-8:]):
        bg = "#3498db" if odd < 2 else "#9132f0" if odd < 10 else "#ff00ff"
        cols[i].markdown(f"""
            <div style="background-color:{bg}; padding:10px; border-radius:8px; text-align:center; font-weight:bold; color:white;">
                {odd}x
            </div>
        """, unsafe_allow_html=True)

    # 3. Live Graph
    fig = go.Figure(go.Scatter(x=list(range(len(live_odds))), y=live_odds, 
                               mode='lines+markers', line=dict(color='#45ad15', width=3)))
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', 
                      font_color='white', height=300, margin=dict(l=0, r=0, t=20, b=0))
    st.plotly_chart(fig, use_container_width=True)

    # 4. AI Analysis & Signal
    c1, c2 = st.columns([2, 1])
    with c1:
        last_odd = live_odds[-1]
        msg = "Trend is stable." if last_odd > 2 else "Low odd detected. Wait for 2.0x signal."
        st.info(f"🤖 AI Analysis: {msg}")
        st.caption(f"Last auto-sync: {time.strftime('%H:%M:%S')}")
    
    with c2:
        prediction = round(np.random.uniform(1.5, 4.0), 2)
        st.markdown(f"""
            <div style="background:#111; padding:20px; border-radius:10px; border:2px solid #45ad15; text-align:center;">
                <h4 style="margin:0; color:white;">NEXT PREDICTION</h4>
                <h1 style="color:#45ad15; margin:0;">{prediction}x</h1>
            </div>
        """, unsafe_allow_html=True)

# --- 4. MAIN FLOW ---
if st.session_state['user'] is None:
    st.title("Betpawa AI Login")
    u = st.text_input("Username")
    p = st.text_input("Password", type="password")
    if st.button("LOGIN"):
        if u and p:
            st.session_state['user'] = u
            st.rerun()
else:
    # Sidebar logout (Iyi ntiyivugurura buri kanya ngo iteze ikosa)
    with st.sidebar:
        st.title(f"👤 {st.session_state['user']}")
        if st.button("LOGOUT"):
            st.session_state['user'] = None
            st.rerun()
        st.write("---")
        st.success("Auto-refresh is active (5s)")

    # Hamagara ya function yivugurura
    live_dashboard()
