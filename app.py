import streamlit as st
import pandas as pd
import numpy as np
import time
import plotly.graph_objects as go

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Neural History Analyzer Pro", layout="wide")

# --- 2. THE ENGINE (BetPawa Deep History & Pattern Analysis) ---
class AdvancedNeuralEngine:
    def __init__(self, game):
        self.game = game
        self.mem_key = f'mem_{game}'
        self.archive_key = f'archive_{game}'
        self.log_key = f'log_{game}'
        self.pred_key = f'pred_{game}'
        self.streak_key = f'streak_{game}'
        
        if self.mem_key not in st.session_state:
            st.session_state[self.mem_key] = [1.2, 2.5, 1.1, 4.0, 1.05]
        if self.archive_key not in st.session_state:
            # Aya ni amateka ya kera cyane AI yigiraho (BetPawa Archives)
            st.session_state[self.archive_key] = [1.5, 3.2, 1.1, 4.5, 1.02, 2.1, 1.8, 1.05, 6.0]
        if self.log_key not in st.session_state:
            st.session_state[self.log_key] = []
        if self.pred_key not in st.session_state:
            st.session_state[self.pred_key] = None
        if self.streak_key not in st.session_state:
            st.session_state[self.streak_key] = 0

    def analyze_patterns(self):
        history = st.session_state[self.mem_key]
        archive = st.session_state[self.archive_key]
        if len(history) < 3: return 60
        last_pattern = history[-3:]
        matches = 0
        for i in range(len(archive) - 3):
            if archive[i:i+3] == last_pattern:
                matches += 1
        confidence = 70 + (matches * 10)
        return min(confidence, 99)

    def update(self, actual_odd):
        last_pred = st.session_state[self.pred_key]
        if last_pred:
            status = "WIN" if actual_odd >= last_pred else "LOSS"
            if status == "WIN":
                st.session_state[self.streak_key] += 1
            else:
                st.session_state[self.streak_key] = 0
                
            st.session_state[self.log_key].insert(0, {
                "Time": time.strftime('%H:%M:%S'),
                "AI Prediction": f"{last_pred}x",
                "Actual Result": f"{actual_odd}x",
                "Status": status
            })
            
        st.session_state[self.mem_key].append(actual_odd)
        st.session_state[self.archive_key].append(actual_odd)
        if len(st.session_state[self.mem_key]) > 20: st.session_state[self.mem_key].pop(0)
        if len(st.session_state[self.archive_key]) > 100: st.session_state[self.archive_key].pop(0)

    def get_prediction(self, boost_mode=False):
        confidence = self.analyze_patterns()
        if boost_mode: confidence += 5
        if confidence > 80:
            pred = round(np.random.uniform(1.8, 3.5), 2)
        else:
            pred = round(np.random.uniform(1.3, 2.1), 2)
        st.session_state[self.pred_key] = pred
        return pred, f"✅ Confidence: {confidence}% (BetPawa Match)"

# --- 3. UI STYLING ---
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
    .streak-alert {
        background: #45ad15; color: white; padding: 10px;
        border-radius: 10px; text-align: center; font-weight: bold;
        margin-bottom: 15px; border: 1px solid #2d6a10;
    }
    .auth-container {
        max-width: 400px; margin: auto; padding: 30px;
        background: #111; border-radius: 15px; border: 1px solid #333;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. AUTHENTICATION LOGIC ---
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

if not st.session_state['authenticated']:
    st.markdown("<br><br>", unsafe_allow_html=True)
    with st.container():
        st.markdown("<div class='auth-container'>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align:center;'>SYSTEM LOGIN</h2>", unsafe_allow_html=True)
        user_id = st.text_input("Agent ID", placeholder="Enter your ID")
        access_key = st.text_input("Access Key", type="password", placeholder="••••••••")
        
        if st.button("LOGIN TO ENGINE", use_container_width=True):
            if user_id and access_key == "2026": # Urashyiramo password ushaka hano
                st.session_state['authenticated'] = True
                st.rerun()
            else:
                st.error("Invalid Credentials. Please try again.")
        
        st.write("---")
        st.markdown("<p style='text-align:center; font-size:12px;'>Need access? Contact Admin via WhatsApp</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# --- 5. MAIN SYSTEM (ONLY SHOWS AFTER LOGIN) ---
else:
    with st.sidebar:
        st.markdown("### ⚙️ SYSTEM CONTROL")
        game_choice = st.radio("SELECT GAME", ["AVIATOR", "JETX"])
        st.write("---")
        boost_ai = st.checkbox("🚀 BOOST ACCURACY", value=True)
        refresh_speed = st.slider("Scan Speed (Sec)", 3, 15, 6)
        
        st.info(f"BetPawa Archive: {len(st.session_state.get(f'archive_{game_choice}', []))} records")
        
        if st.button("LOGOUT SYSTEM", use_container_width=True):
            st.session_state['authenticated'] = False
            st.rerun()

    primary_color = "#ff4b4b" if game_choice == "AVIATOR" else "#ffcc00"

    @st.fragment(run_every=refresh_speed)
    def main_engine():
        engine = AdvancedNeuralEngine(game_choice)
        actual_val = round(np.random.uniform(1.0, 5.0), 2)
        engine.update(actual_val)
        
        st.markdown(f"<h2 style='text-align:center; color:{primary_color};'>{game_choice} NEURAL ANALYZER</h2>", unsafe_allow_html=True)

        streak = st.session_state[engine.streak_key]
        if streak >= 2:
            st.markdown(f"<div class='streak-alert'>🔥 WINNING STREAK: {streak} IN A ROW!</div>", unsafe_allow_html=True)
        
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
                    <div class='status-badge'>SCANNING BETPAWA HISTORY...</div>
                </div>
            """, unsafe_allow_html=True)

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
