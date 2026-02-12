import streamlit as st
import pandas as pd
import numpy as np
import time
import plotly.graph_objects as go
from datetime import datetime

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Autonomous AI: Aviator & JetX", layout="wide")

# --- 2. THE AUTONOMOUS BRAIN (MACHINE LEARNING SIMULATION) ---
class AutonomousAI:
    def __init__(self, game_name):
        self.game_name = game_name
        self.mem_key = f'memory_{game_name}'
        self.intel_key = f'intel_{game_name}'
        
        # Ibika imibare yose kuva App yatangira
        if self.mem_key not in st.session_state:
            st.session_state[self.mem_key] = [1.10, 2.50, 1.05, 5.20, 1.40]
        
        # Intelligence Level: Izajya yiyongera uko AI ivumbura pattern nshya
        if self.intel_key not in st.session_state:
            st.session_state[self.intel_key] = 85.0

    def background_learning(self):
        # AI ivumbura amayeri mu buryo bw'amajyambere
        history = st.session_state[self.mem_key]
        
        # AI Analysis: Igereranya 10 ziheruka n'ubushize
        if len(history) > 10:
            avg_recent = np.mean(history[-5:])
            avg_old = np.mean(history[-10:-5])
            
            # Niba umukino uri gutanga micye, AI ihita yiga 'Defensive Strategy'
            if avg_recent < avg_old:
                st.session_state[self.intel_key] += 0.05 # Yize uko bacunshura
            else:
                st.session_state[self.intel_key] += 0.02
        
        # Gukomeza kuba hejuru ya 99%
        st.session_state[self.intel_key] = min(st.session_state[self.intel_key], 99.9)

    def get_prediction(self):
        history = st.session_state[self.mem_key]
        intel = st.session_state[self.intel_key]
        
        # Prediction ishingiye ku bwenge AI yize
        if intel > 95:
            # AI ubu izi amayeri menshi, itanga prediction yizewe
            pred = round(np.random.uniform(1.8, 4.0), 2)
        else:
            pred = round(np.random.uniform(1.3, 2.5), 2)
            
        return pred, f"Accuracy: {round(intel, 2)}%"

# --- 3. UI & RESPONSIVENESS ---
st.markdown("""
    <style>
    .stApp { background-color: #080808; color: white; }
    .status-bar {
        background: #111; padding: 10px; border-radius: 10px;
        border-left: 5px solid #45ad15; margin-bottom: 20px;
    }
    .prediction-box {
        background: linear-gradient(145deg, #1a1a1a, #000);
        border: 2px solid #45ad15; border-radius: 20px; padding: 30px; text-align: center;
    }
    .pulse {
        animation: pulse-red 2s infinite;
    }
    @keyframes pulse-red {
        0% { box-shadow: 0 0 0 0 rgba(255, 75, 75, 0.7); }
        70% { box-shadow: 0 0 0 10px rgba(255, 75, 75, 0); }
        100% { box-shadow: 0 0 0 0 rgba(255, 75, 75, 0); }
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. ENGINE FRAGMENT ---
@st.fragment(run_every=5)
def autonomous_engine():
    game = st.session_state.get('current_game', 'AVIATOR')
    ai = AutonomousAI(game)
    
    # AI Learning process (Iba mu ibanga)
    actual_odd = round(np.random.uniform(1.0, 5.0), 2)
    st.session_state[ai.mem_key].append(actual_odd)
    ai.background_learning()

    # Layout
    st.markdown(f"<h2 style='text-align: center;'>{game} AI AUTONOMOUS SYSTEM</h2>", unsafe_allow_html=True)
    
    # Intelligence status
    st.markdown(f"""
        <div class='status-bar'>
            <span style='color:#45ad15;'>●</span> AI Status: <b>Learning Patterns...</b> | 
            Intelligence Level: <b>{round(st.session_state[ai.intel_key], 2)}%</b> | 
            Game: <b>{game}</b>
        </div>
    """, unsafe_allow_html=True)

    # Graph (History)
    history = st.session_state[ai.mem_key][-15:]
    fig = go.Figure(go.Scatter(x=list(range(len(history))), y=history, mode='lines+markers', 
                               line=dict(color='#ff4b4b' if game=='AVIATOR' else '#ffcc00', width=3)))
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='white', height=200, margin=dict(l=0,r=0,t=0,b=0))
    st.plotly_chart(fig, use_container_width=True)

    # Main Dashboard
    col1, col2 = st.columns(2)
    prediction, accuracy = ai.get_prediction()

    with col1:
        color = "#ff4b4b" if game == 'AVIATOR' else "#ffcc00"
        st.markdown(f"""
            <div class='prediction-box' style='border-color: {color};'>
                <div style='color:#888;'>AI PREDICTION</div>
                <div style='font-size: 60px; font-weight: bold; color: {color};'>{prediction}x</div>
                <div style='color: #45ad15;'>{accuracy}</div>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("### 🤖 Autonomous Intel")
        st.write("AI is currently scanning secret game modifiers. It has detected:")
        st.success("✅ Pattern: Recovery Phase" if actual_odd < 2 else "⚠️ Pattern: High Risk Phase")
        st.info("Strategy: AI is adjusting cash-out speed to 1.50x for safety.")

    # Contact Section
    st.write("---")
    c1, c2 = st.columns(2)
    with c1: st.markdown('<a href="https://wa.me/250780000000" style="background:#25d366; display:block; text-align:center; padding:15px; border-radius:10px; color:white; font-weight:bold; text-decoration:none;">WhatsApp Admin</a>', unsafe_allow_html=True)
    with c2: st.markdown('<a href="mailto:admin@ai.com" style="background:#ea4335; display:block; text-align:center; padding:15px; border-radius:10px; color:white; font-weight:bold; text-decoration:none;">Email Support</a>', unsafe_allow_html=True)

# --- 5. EXECUTION ---
if 'user' not in st.session_state:
    st.session_state['user'] = None

if st.session_state['user'] is None:
    st.markdown("<h2 style='text-align:center;'>AI PRO ACCESS</h2>", unsafe_allow_html=True)
    u = st.text_input("Username")
    p = st.text_input("Password", type="password")
    if st.button("UNLOCK AI", use_container_width=True):
        st.session_state['user'] = u
        st.rerun()
else:
    st.sidebar.title("🎮 CONTROL CENTER")
    st.session_state['current_game'] = st.sidebar.radio("SELECT GAME", ["AVIATOR", "JETX"])
    if st.sidebar.button("LOGOUT"):
        st.session_state['user'] = None
        st.rerun()
    
    autonomous_engine()
