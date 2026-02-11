import streamlit as st
import pandas as pd
import numpy as np
import time
import plotly.graph_objects as go

# --- 1. CONFIG ---
st.set_page_config(page_title="Betpawa AI Auto-Live", layout="wide")

# --- 2. CSS FOR STYLING ---
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

# --- 3. LIVE DATA FUNCTION ---
def get_betpawa_odds():
    # Simulation y'imibare igezweho kuri Betpawa
    # Ibi ni byo bizajya bihinduka automatically
    return [round(np.random.uniform(1.0, 4.0), 2) for _ in range(12)]

# --- 4. MAIN APP ---
if 'user' not in st.session_state:
    st.session_state['user'] = None

if st.session_state['user'] is None:
    # Login simple
    st.markdown("<div class='betpawa-header'>BETPAWA AI LOGIN</div>", unsafe_allow_html=True)
    u = st.text_input("Username")
    p = st.text_input("Password", type="password")
    if st.button("LOGIN"):
        st.session_state['user'] = u
        st.rerun()
else:
    # --- AUTO-UPDATE LOOP ---
    # Kurema ahantu (Placeholder) hazajya hahinduka nta refresh
    placeholder = st.empty()

    while True:
        with placeholder.container():
            st.markdown("<div class='betpawa-header'>LIVE BETPAWA AI SCANNER</div>", unsafe_allow_html=True)
            
            # 1. Fetch live odds
            live_odds = get_betpawa_odds()
            
            # 2. Display Top Odds Bar
            cols = st.columns(8)
            for i, odd in enumerate(live_odds[-8:]):
                bg = "#3498db" if odd < 2 else "#9132f0" if odd < 10 else "#ff00ff"
                cols[i].markdown(f'<div class="odd-box" style="background-color:{bg};">{odd}x</div>', unsafe_allow_html=True)

            # 3. Live Graph
            st.write("---")
            fig = go.Figure(go.Scatter(x=list(range(len(live_odds))), y=live_odds, 
                                       mode='lines+markers', line=dict(color='#45ad15', width=3)))
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', 
                              font_color='white', height=300, margin=dict(l=0, r=0, t=20, b=0))
            st.plotly_chart(fig, use_container_width=True)

            # 4. AI Analysis Munsi ya Graph
            c1, c2 = st.columns([2, 1])
            
            with c1:
                st.subheader("🤖 Smart AI Assistant")
                last_odd = live_odds[-1]
                
                # Logic ya AI ashingiye kuri Live Data
                if last_odd < 1.5:
                    msg = f"⚠️ Alert: Indege iheruka yari nto ({last_odd}x). Round itaha ifite amahirwe yo kurenga 2.20x."
                else:
                    msg = f"✅ Trend ikomeje kuba nziza. Live Odds ubu ni {last_odd}x. Cash out at 1.80x for safety."
                
                st.markdown(f'<div class="ai-alert">{msg}</div>', unsafe_allow_html=True)
                st.caption(f"Last scanned: {time.strftime('%H:%M:%S')}")

            with c2:
                st.subheader("🎯 Current Signal")
                prediction = round(np.random.uniform(1.5, 3.5), 2)
                st.markdown(f"""
                    <div style="background:#111; padding:20px; border-radius:10px; border:2px solid #45ad15; text-align:center;">
                        <h4 style="margin:0;">NEXT ODD</h4>
                        <h1 style="color:#45ad15; margin:0;">{prediction}x</h1>
                    </div>
                """, unsafe_allow_html=True)

            # 5. Sidebar Options
            if st.sidebar.button("Logout"):
                st.session_state['user'] = None
                st.rerun()
            
            st.sidebar.info("System is auto-refreshing every 5 seconds.")

            # --- WAIT FOR 5 SECONDS BEFORE NEXT UPDATE ---
            time.sleep(5)
            # Code ihita isubira hejuru (while True) igahindura byose nta refresh
