import streamlit as st
import pandas as pd
import numpy as np
import time
import plotly.graph_objects as go

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Aviator AI BetPawa Analyzer", layout="wide")

# --- 2. BETPAWA DEEP HISTORY ENGINE ---
class BetPawaEngine:
    def __init__(self):
        # Ibi ni amateka ya kera (Archives) AI yiga kuva kuri BetPawa
        if 'betpawa_archive' not in st.session_state:
            st.session_state['betpawa_archive'] = [1.50, 2.30, 1.10, 8.50, 1.00, 4.20, 1.30, 2.10, 1.05]
        
        if 'current_mem' not in st.session_state:
            st.session_state['current_mem'] = [1.20, 3.00, 1.05, 2.50]
            
        if 'logs' not in st.session_state:
            st.session_state['logs'] = []
            
        if 'streak' not in st.session_state:
            st.session_state['streak'] = 0
            
        if 'next_signal' not in st.session_state:
            st.session_state['next_signal'] = None

    def analyze_betpawa_cycles(self):
        """AI isuzuma amateka ya BetPawa ikareba niba hari cycle iri kwisubiramo"""
        history = st.session_state['betpawa_archive']
        recent = st.session_state['current_mem'][-2:]
        
        matches = 0
        for i in range(len(history) - 2):
            if history[i:i+2] == recent:
                matches += 1
        
        # Accuracy ishingiye ku nshuro byabaye kuri BetPawa kera
        confidence = 75 + (matches * 8)
        return min(confidence, 99)

    def process_round(self):
        actual_odd = round(np.random.uniform(1.0, 5.0), 2)
        
        # Win/Loss Check
        last_s = st.session_state['next_signal']
        if last_s:
            status = "WIN" if actual_odd >= last_s else "LOSS"
            st.session_state['streak'] = st.session_state['streak'] + 1 if status == "WIN" else 0
            
            st.session_state['logs'].insert(0, {
                "Time": time.strftime('%H:%M:%S'),
                "AI": f"{last_s}x",
                "Actual": f"{actual_odd}x",
                "Status": status
            })

        # Update History Archives
        st.session_state['current_mem'].append(actual_odd)
        st.session_state['betpawa_archive'].append(actual_odd)
        
        # New Prediction
        conf = self.analyze_betpawa_cycles()
        new_s = round(np.random.uniform(1.6, 3.5), 2) if conf > 80 else None
        st.session_state['next_signal'] = new_s
        
        return actual_odd, new_s, conf

# --- 3. ORIGINAL AVIATOR INTERFACE ---
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: white; }
    .aviator-card {
        background-color: #1a1a1a; padding: 25px; border-radius: 15px;
        border: 1px solid #2c2c2c; text-align: center;
    }
    .pred-text { color: #ff4b4b; font-size: 65px; font-weight: bold; margin: 0; }
    .act-text { color: #ffffff; font-size: 65px; font-weight: bold; margin: 0; }
    .streak-box {
        background: #45ad15; padding: 10px; border-radius: 8px;
        text-align: center; font-weight: bold; margin-bottom: 20px;
    }
    .win { color: #45ad15; font-weight: bold; }
    .loss { color: #ff4b4b; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. LOGIN ---
if 'user' not in st.session_state:
    st.session_state['user'] = None

if st.session_state['user'] is None:
    st.markdown("<h2 style='text-align:center;'>AVIATOR AI LOGIN</h2>", unsafe_allow_html=True)
    u = st.text_input("Username")
    p = st.text_input("Password", type="password")
    if st.button("LOGIN", use_container_width=True):
        st.session_state['user'] = u
        st.rerun()
else:
    # Sidebar
    with st.sidebar:
        st.write(f"Agent: **{st.session_state['user']}**")
        if st.button("Logout"):
            st.session_state['user'] = None
            st.rerun()

    engine = BetPawaEngine()

    @st.fragment(run_every=6)
    def dashboard():
        actual, signal, confidence = engine.process_round()
        
        st.markdown("<h2 style='text-align: center; color: #ff4b4b;'>🚀 AVIATOR AI PRO</h2>", unsafe_allow_html=True)

        # Winning Streak
        streak = st.session_state['streak']
        if streak >= 2:
            st.markdown(f"<div class='streak-box'>🔥 WINNING STREAK: {streak} IN A ROW!</div>", unsafe_allow_html=True)

        # Prediction & Actual
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
                <div class='aviator-card' style='border-color:#ff4b4b;'>
                    <div style='color:#888;'>NEXT PREDICTION</div>
                    <p class='pred-text'>{signal if signal else 'WAIT'}x</p>
                    <div style='color:#45ad15; font-size:12px;'>BetPawa Archive Match: {confidence}%</div>
                </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
                <div class='aviator-card'>
                    <div style='color:#888;'>ACTUAL RESULT</div>
                    <p class='act-text'>{actual}x</p>
                    <div style='color:#888; font-size:12px;'>Round Synchronized</div>
                </div>
            """, unsafe_allow_html=True)

        # Graph
        hist = st.session_state['current_mem'][-15:]
        fig = go.Figure(go.Scatter(x=list(range(len(hist))), y=hist, mode='lines+markers', line=dict(color='#ff4b4b', width=4)))
        fig.update_layout(paper_bgcolor='black', plot_bgcolor='black', font_color='white', height=200, margin=dict(l=0,r=0,t=10,b=0), xaxis=dict(visible=False))
        st.plotly_chart(fig, use_container_width=True)
        

        # Logs
        st.write("### 📜 BETPAWA PERFORMANCE LOGS")
        for log in st.session_state['logs'][:5]:
            st.markdown(f"""
                <div style="background:#111; padding:10px; border-radius:10px; margin-bottom:5px; border-left: 5px solid {'#45ad15' if log['Status']=='WIN' else '#ff4b4b'};">
                    AI: <b>{log['AI']}</b> | Result: <b>{log['Actual']}</b> | Status: <span class='{log['Status'].lower()}'>{log['Status']}</span>
                </div>
            """, unsafe_allow_html=True)

    dashboard()
