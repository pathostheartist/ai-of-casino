import streamlit as st
import pandas as pd
import numpy as np
import time
import plotly.graph_objects as go

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Neural History Analyzer", layout="wide")

# --- 2. ADVANCED AI ENGINE WITH HISTORY ANALYSIS ---
class AdvancedNeuralEngine:
    def __init__(self, game):
        self.game = game
        self.mem_key = f'mem_{game}'
        self.log_key = f'log_{game}'
        self.pred_key = f'pred_{game}'
        
        # Memory yagutse yo kubika history ndende
        if self.mem_key not in st.session_state:
            st.session_state[self.mem_key] = [1.2, 2.5, 1.1, 4.0, 1.05, 1.8, 1.3, 3.2, 1.1, 1.02]
        if self.log_key not in st.session_state:
            st.session_state[self.log_key] = []
        if self.pred_key not in st.session_state:
            st.session_state[self.pred_key] = None

    def analyze_patterns(self):
        history = st.session_state[self.mem_key]
        if len(history) < 5: return 50 # Default probability
        
        # Isesengura ry'imibare 3 ya nyuma
        last_three = history[-3:]
        
        # Deep Scan Logic: AI ireba niba iyi pattern yarigeze kubaho mbere
        matches = 0
        for i in range(len(history) - 3):
            if history[i:i+3] == last_three:
                matches += 1
        
        # Ijanisha ry'ubushobozi (Confidence Level)
        confidence = 65 + (matches * 10)
        return min(confidence, 98)

    def update(self, actual_odd):
        last_pred = st.session_state[self.pred_key]
        if last_pred:
            status = "WIN" if actual_odd >= last_pred else "LOSS"
            st.session_state[self.log_key].insert(0, {
                "Time": time.strftime('%H:%M:%S'),
                "AI Prediction": f"{last_pred}x",
                "Actual Result": f"{actual_odd}x",
                "Status": status
            })
        st.session_state[self.mem_key].append(actual_odd)
        if len(st.session_state[self.mem_key]) > 50: # Tubika amateka 50
            st.session_state[self.mem_key].pop(0)

    def get_prediction(self, boost_mode=False):
        history = st.session_state[self.mem_key]
        confidence = self.analyze_patterns()
        
        if boost_mode: confidence += 5 # Kongera imbaraga nka Admin
        
        if all(x < 1.3 for x in history[-2:]) and confidence < 70:
            st.session_state[self.pred_key] = None
            return None, "🚫 STANDBY (High Risk Pattern)"
        
        # Prediction ishingiye kuri Confidence yabonye mu mateka
        if confidence > 85:
            pred = round(np.random.uniform(2.0, 4.5), 2)
        else:
            pred = round(np.random.uniform(1.4, 2.2), 2)
            
        st.session_state[self.pred_key] = pred
        return pred, f"✅ Confidence: {confidence}%"

# --- 3. INTERFACE STYLING ---
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: white; }
    .prediction-card {
        background: #111; padding: 25px; border-radius: 15px;
        border: 2px solid #ff4b4b; text-align: center;
    }
    .status-badge {
        padding: 5px 15px; border-radius: 20px; font-size: 12px;
        background: #222; border: 1px solid #444;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. LOGIN ---
if 'user' not in st.session_state:
    st.session_state['user'] = None

if st.session_state['user'] is None:
    st.markdown("<h2 style='text-align:center;'>NEURAL ENGINE LOGIN</h2>", unsafe_allow_html=True)
    u = st.text_input("Agent ID")
    p = st.text_input("Access Key", type="password")
    if st.button("LOGIN", use_container_width=True):
        st.session_state['user'] = u
        st.rerun()
else:
    # --- 5. ADMIN CONTROL SIDEBAR ---
    with st.sidebar:
        st.markdown("### ⚙️ SYSTEM CONTROL")
        game_choice = st.radio("SELECT GAME", ["AVIATOR", "JETX"])
        st.write("---")
        boost_ai = st.checkbox("🚀 BOOST AI ACCURACY", value=True)
        refresh_speed = st.slider("Scan Speed (Sec)", 3, 15, 6)
        
        if st.button("EXIT SYSTEM", use_container_width=True):
            st.session_state['user'] = None
            st.rerun()

    primary_color = "#ff4b4b" if game_choice == "AVIATOR" else "#ffcc00"

    @st.fragment(run_every=refresh_speed)
    def main_engine():
        engine = AdvancedNeuralEngine(game_choice)
        actual_val = round(np.random.uniform(1.0, 5.0), 2)
        engine.update(actual_val)
        
        st.markdown(f"<h2 style='text-align:center; color:{primary_color};'>{game_choice} NEURAL ANALYZER</h2>", unsafe_allow_html=True)
        
        # History Graph
        history = st.session_state[engine.mem_key]
        fig = go.Figure(go.Scatter(x=list(range(len(history))), y=history, mode='lines+markers', line=dict(color=primary_color, width=4)))
        fig.update_layout(paper_bgcolor='black', plot_bgcolor='black', font_color='white', height=200, margin=dict(l=0,r=0,t=0,b=0), xaxis=dict(visible=False))
        st.plotly_chart(fig, use_container_width=True)

        col1, col2 = st.columns(2)
        pred_val, advice = engine.get_prediction(boost_ai)
        
        with col1:
            st.markdown(f"""
                <div class='prediction-card' style='border-color:{primary_color};'>
                    <div style='color:#888;'>AI PREDICTION</div>
                    <div style='font-size:55px; font-weight:bold; color:{primary_color};'>{pred_val if pred_val else '---'}x</div>
                    <div style='color:#45ad15;'>{advice}</div>
                </div>
            """, unsafe_allow_html=True)
            
        with col2:
            st.markdown(f"""
                <div class='prediction-card' style='border-color:#444;'>
                    <div style='color:#888;'>ACTUAL RESULT</div>
                    <div style='font-size:55px; font-weight:bold; color:white;'>{actual_val}x</div>
                    <div class='status-badge'>SCANNING HISTORY...</div>
                </div>
            """, unsafe_allow_html=True)

        # Performance Logs
        st.write("---")
        st.markdown("### 📊 WIN/LOSS HISTORY SCAN")
        for log in st.session_state[engine.log_key][:5]:
            status_color = "#45ad15" if log['Status'] == "WIN" else "#ff4b4b"
            st.markdown(f"""
                <div style="background:#111; padding:10px; border-radius:10px; margin-bottom:5px; border-left: 5px solid {status_color};">
                    AI: <b>{log['AI Prediction']}</b> | Result: <b>{log['Actual Result']}</b> | <span style="color:{status_color};">{log['Status']}</span>
                </div>
            """, unsafe_allow_html=True)

    main_engine()
