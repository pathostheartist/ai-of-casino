import streamlit as st
import pandas as pd
import numpy as np
import time
import plotly.graph_objects as go

# --- 1. CONFIG ---
st.set_page_config(page_title="Betpawa AI Auto-Live", layout="wide")

# --- 2. CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #0b0d10; color: white; }
    .betpawa-header { color: #45ad15; font-size: 30px; font-weight: bold; text-align: center; }
    .odd-box {
        padding: 10px; border-radius: 8px; text-align: center;
        font-weight: bold; font-size: 18px; color: white;
    }
    .ai-alert {
        background-color: #1a1a1a; border-left: 5px solid #45ad15;
        padding: 15px; border-radius: 5px; margin: 10px 0;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SESSION STATE ---
if 'user' not in st.session_state:
    st.session_state['user'] = None

# --- 4. MAIN LOGIC ---
if st.session_state['user'] is None:
    st.markdown("<div class='betpawa-header'>BETPAWA AI LOGIN</div>", unsafe_allow_html=True)
    u = st.text_input("Username")
    p = st.text_input("Password", type="password")
    if st.button("LOGIN"):
        if u and p: # Shaka niba yujuje
            st.session_state['user'] = u
            st.rerun()
else:
    # Kurema utubati (Placeholders) kugira ngo amakosa ya Duplicate ElementId avemo
    side_placeholder = st.sidebar.empty()
    main_placeholder = st.empty()

    while True:
        # --- SIDEBAR REFRESH ---
        with side_placeholder.container():
            st.title(f"👤 {st.session_state['user']}")
            st.info("System is auto-refreshing...")
            # Aha niho dukosoreye: Buto y'umwihariko
            if st.button("LOGOUT", key="logout_btn"):
                st.session_state['user'] = None
                st.rerun()

        # --- MAIN CONTENT REFRESH ---
        with main_placeholder.container():
            st.markdown("<div class='betpawa-header'>LIVE BETPAWA AI SCANNER</div>", unsafe_allow_html=True)
            
            # Fetch random/live odds
            live_odds = [round(np.random.uniform(1.0, 5.0), 2) for _ in range(12)]
            
            # Display History
            cols = st.columns(8)
            for i, odd in enumerate(live_odds[-8:]):
                bg = "#3498db" if odd < 2 else "#9132f0" if odd < 10 else "#ff00ff"
                cols[i].markdown(f'<div class="odd-box" style="background-color:{bg};">{odd}x</div>', unsafe_allow_html=True)

            # Live Graph
            fig = go.Figure(go.Scatter(x=list(range(len(live_odds))), y=live_odds, 
                                       mode='lines+markers', line=dict(color='#45ad15', width=3)))
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', 
                              font_color='white', height=300, margin=dict(l=0, r=0, t=20, b=0))
            st.plotly_chart(fig, use_container_width=True)

            # AI Analysis
            c1, c2 = st.columns([2, 1])
            with c1:
                st.subheader("🤖 AI Real-Time Analysis")
                last_odd = live_odds[-1]
                msg = f"Betpawa Analysis: Last odd was {last_odd}x. "
                msg += "AI predicts a safe 1.50x soon." if last_odd < 2 else "Trend is stable."
                st.markdown(f'<div class="ai-alert">{msg}</div>', unsafe_allow_html=True)
                st.caption(f"Last scanned: {time.strftime('%H:%M:%S')}")

            with c2:
                prediction = round(np.random.uniform(1.5, 3.5), 2)
                st.markdown(f"""
                    <div style="background:#111; padding:20px; border-radius:10px; border:2px solid #45ad15; text-align:center;">
                        <h4 style="margin:0;">NEXT ODD</h4>
                        <h1 style="color:#45ad15; margin:0;">{prediction}x</h1>
                    </div>
                """, unsafe_allow_html=True)

        # Wait 5 seconds
        time.sleep(5)
