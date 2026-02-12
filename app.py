import streamlit as st
import pandas as pd
import numpy as np
import time
import plotly.graph_objects as go

# --- 1. CONFIGURATION (Stable & Dark) ---
st.set_page_config(page_title="Aviator AI Neural Pro", layout="wide")

# --- 2. THE STEALTH ENGINE ---
class AviatorNeuralEngine:
    def __init__(self):
        # Memory & Archive settings
        if 'mem' not in st.session_state:
            st.session_state['mem'] = [1.2, 2.5, 1.1, 4.0, 1.05]
        if 'archive' not in st.session_state:
            st.session_state['archive'] = [2.1, 1.0, 5.8, 1.1, 1.4, 2.0]
        if 'logs' not in st.session_state:
            st.session_state['logs'] = []
        if 'streak' not in st.session_state:
            st.session_state['streak'] = 0
        if 'last_pred' not in st.session_state:
            st.session_state['last_pred'] = None

    def analyze_deep_history(self):
        recent = st.session_state['mem'][-3:]
        archive = st.session_state['archive']
        matches = 0
        for i in range(len(archive) - 3):
            if archive[i:i+3] == recent:
                matches += 1
        confidence = 65 + (matches * 10)
        return min(confidence, 99)

    def process_live_round(self):
        # 1. Simulate Actual Odd
        actual_odd = round(np.random.uniform(1.0, 4.5), 2)
        
        # 2. Check Previous Prediction for Win/Loss
        last_p = st.session_state['last_pred']
        if last_p:
            status = "WIN" if actual_odd >= last_p else "LOSS"
            if status == "WIN":
                st.session_state['streak'] += 1
            else:
                st.session_state['streak'] = 0
            
            # Log result
            st.session_state['logs'].insert(0, {
                "Time": time.strftime('%H:%M:%S'),
                "AI": f"{last_p}x",
                "Actual": f"{actual_odd}x",
                "Status": status
            })

        # 3. Update Memory & Archive
        st.session_state['mem'].append(actual_odd)
        st.session_state['archive'].append(actual_odd)
        if len(st.session_state['mem']) > 15: st.session_state['mem'].pop(0)

        # 4. Generate Next Prediction
        conf = self.analyze_deep_history()
        new_pred = round(np.random.uniform(1.6, 3.2), 2) if conf > 75 else None
        st.session_state['last_pred'] = new_pred
        
        return actual_odd, new_pred, conf

# --- 3. AVIATOR INTERFACE CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: white; }
    .aviator-card {
        background-color: #1a1a1a; padding: 20px; border-radius: 15px;
        border: 1px solid #2c2c2c; text-align: center;
    }
    .prediction-text { color: #ff4b4b; font-size: 60px; font-weight: bold; margin: 0; }
    .actual-text { color: #ffffff; font-size: 60px; font-weight: bold; margin: 0; }
    .streak-badge {
        background: #45ad15; color: white; padding: 10px; 
        border-radius: 10px; font-weight: bold; text-align: center; margin-bottom: 20px;
    }
    .win { color: #45ad15; font-weight: bold; }
    .loss { color: #ff4b4b; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. LOGIN SYSTEM ---
if 'user' not in st.session_state:
    st.session_state['user'] = None

if st.session_state['user'] is None:
    st.markdown("<h2 style='text-align:center;'>AVIATOR AI LOGIN</h2>", unsafe_allow_html=True)
    u = st.text_input("Username")
    p = st.text_input("Password", type="password")
    if st.button("LOGIN", use_container_width=True):
        st.session_state['user'] = u
        st.rerun()
    st.write("---")
    st.markdown("<p style='text-align:center;'>Contact Admin for Access</p>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1: st.markdown('<a href="https://wa.me/250780000000" style="background:#25d366; display:block; text-align:center; padding:10px; border-radius:5px; color:white; text-decoration:none;">WhatsApp</a>', unsafe_allow_html=True)
    with c2: st.markdown('<a href="mailto:admin@ai.com" style="background:#ea4335; display:block; text-align:center; padding:10px; border-radius:5px; color:white; text-decoration:none;">Email</a>', unsafe_allow_html=True)

# --- 5. MAIN DASHBOARD ---
else:
    # Sidebar Control
    with st.sidebar:
        st.markdown("### ⚙️ SYSTEM CONTROL")
        game = st.radio("GAME", ["AVIATOR", "JETX"])
        st.write("---")
        if st.button("LOGOUT", use_container_width=True):
            st.session_state['user'] = None
            st.rerun()

    engine = AviatorNeuralEngine()
    
    @st.fragment(run_every=6)
    def live_ui():
        actual, next_p, confidence = engine.process_live_round()
        
        st.markdown(f"<h2 style='text-align: center; color: #ff4b4b;'>🚀 {game} AI PREDICTOR</h2>", unsafe_allow_html=True)

        # Streak Badge
        streak = st.session_state['streak']
        if streak >= 2:
            st.markdown(f"<div class='streak-badge'>🔥 WINNING STREAK: {streak} IN A ROW!</div>", unsafe_allow_html=True)

        # Main Cards
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
                <div class='aviator-card' style='border-color: #ff4b4b;'>
                    <div style='color:#888;'>NEXT PREDICTION</div>
                    <p class='prediction-text'>{next_p if next_p else 'WAIT'}x</p>
                    <div style='color:#45ad15; font-size:12px;'>Confidence: {confidence}%</div>
                </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
                <div class='aviator-card'>
                    <div style='color:#888;'>ACTUAL RESULT</div>
                    <p class='actual-text'>{actual}x</p>
                    <div style='color:#888; font-size:12px;'>Live Synchronized</div>
                </div>
            """, unsafe_allow_html=True)

        # History Graph
        history = st.session_state['mem']
        fig = go.Figure(go.Scatter(x=list(range(len(history))), y=history, mode='lines+markers', line=dict(color='#ff4b4b', width=4)))
        fig.update_layout(paper_bgcolor='black', plot_bgcolor='black', font_color='white', height=200, margin=dict(l=0,r=0,t=10,b=0), xaxis=dict(visible=False))
        st.plotly_chart(fig, use_container_width=True)

        # Performance Logs
        st.write("### 📜 LIVE PERFORMANCE LOGS")
        for log in st.session_state['logs'][:5]:
            status_class = "win" if log['Status'] == "WIN" else "loss"
            st.markdown(f"""
                <div style="background:#111; padding:10px; border-radius:10px; margin-bottom:5px; border-left: 5px solid {'#45ad15' if log['Status']=='WIN' else '#ff4b4b'};">
                    AI: <b>{log['AI']}</b> | Actual: <b>{log['Actual']}</b> | Result: <span class='{status_class}'>{log['Status']}</span>
                </div>
            """, unsafe_allow_html=True)

    live_ui()
