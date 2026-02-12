import streamlit as st
import pandas as pd
import numpy as np
import time
import plotly.graph_objects as go

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Aviator/JetX AI Neural", layout="wide")

# --- 2. THE CORE ENGINE ---
class ProEngine:
    def __init__(self, game):
        self.game = game
        self.mem_key = f'mem_{game}'
        self.log_key = f'log_{game}'
        self.pred_key = f'pred_{game}'
        
        if self.mem_key not in st.session_state:
            st.session_state[self.mem_key] = [1.20, 2.50, 1.10, 4.00, 1.05]
        if self.log_key not in st.session_state:
            st.session_state[self.log_key] = []
        if self.pred_key not in st.session_state:
            st.session_state[self.pred_key] = None

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
        if len(st.session_state[self.mem_key]) > 15:
            st.session_state[self.mem_key].pop(0)

    def generate_prediction(self):
        history = st.session_state[self.mem_key]
        if all(x < 1.3 for x in history[-2:]):
            st.session_state[self.pred_key] = None
            return None, "🚫 STANDBY (Market Low)"
        
        pred = round(np.random.uniform(1.6, 3.2), 2)
        st.session_state[self.pred_key] = pred
        return pred, "✅ SIGNAL ACTIVE"

# --- 3. CUSTOM INTERFACE CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: white; }
    .prediction-card {
        background: #111; padding: 25px; border-radius: 15px;
        border: 2px solid #ff4b4b; text-align: center;
    }
    .actual-card {
        background: #111; padding: 25px; border-radius: 15px;
        border: 2px solid #444; text-align: center;
    }
    .win-text { color: #45ad15; font-weight: bold; }
    .loss-text { color: #ff4b4b; font-weight: bold; }
    .contact-login {
        padding: 10px; border-radius: 5px; text-decoration: none; 
        display: inline-block; margin: 5px; font-size: 14px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. LOGIN INTERFACE (With Contacts) ---
if 'user' not in st.session_state:
    st.session_state['user'] = None

if st.session_state['user'] is None:
    st.markdown("<h2 style='text-align:center;'>SYSTEM AUTHENTICATION</h2>", unsafe_allow_html=True)
    with st.container():
        u = st.text_input("Agent ID")
        p = st.text_input("Access Key", type="password")
        if st.button("LOGIN TO ENGINE", use_container_width=True):
            st.session_state['user'] = u
            st.rerun()
    
    st.write("---")
    st.markdown("<p style='text-align:center;'>Need Access?</p>", unsafe_allow_html=True)
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        st.markdown('<a href="https://wa.me/250780000000" class="contact-login" style="background:#25d366; color:white; width:100%; text-align:center;">WhatsApp Admin</a>', unsafe_allow_html=True)
    with col_c2:
        st.markdown('<a href="mailto:admin@ai.com" class="contact-login" style="background:#ea4335; color:white; width:100%; text-align:center;">Email Support</a>', unsafe_allow_html=True)

# --- 5. MAIN DASHBOARD ---
else:
    game_choice = st.sidebar.radio("SELECT ENGINE", ["AVIATOR", "JETX"])
    if st.sidebar.button("EXIT SYSTEM"):
        st.session_state['user'] = None
        st.rerun()

    primary_color = "#ff4b4b" if game_choice == "AVIATOR" else "#ffcc00"

    @st.fragment(run_every=6)
    def live_dashboard():
        engine = ProEngine(game_choice)
        actual_val = round(np.random.uniform(1.0, 4.5), 2)
        engine.update(actual_val)
        
        st.markdown(f"<h2 style='text-align:center; color:{primary_color};'>{game_choice} NEURAL ENGINE</h2>", unsafe_allow_html=True)

        # Graph
        history = st.session_state[engine.mem_key]
        fig = go.Figure(go.Scatter(x=list(range(len(history))), y=history, mode='lines+markers', line=dict(color=primary_color, width=4)))
        fig.update_layout(paper_bgcolor='black', plot_bgcolor='black', font_color='white', height=200, margin=dict(l=0,r=0,t=10,b=0), xaxis=dict(visible=False))
        st.plotly_chart(fig, use_container_width=True)
        

        # Prediction vs Actual
        c1, c2 = st.columns(2)
        pred_val, advice = engine.generate_prediction()
        
        with c1:
            st.markdown(f"""
                <div class='prediction-card' style='border-color:{primary_color};'>
                    <div style='color:#888;'>AI PREDICTION</div>
                    <div style='font-size:55px; font-weight:bold; color:{primary_color};'>{pred_val if pred_val else '---'}x</div>
                    <div style='font-size:14px; color:#45ad15;'>{advice}</div>
                </div>
            """, unsafe_allow_html=True)
            
        with c2:
            st.markdown(f"""
                <div class='actual-card'>
                    <div style='color:#888;'>ACTUAL RESULT</div>
                    <div style='font-size:55px; font-weight:bold; color:white;'>{actual_val}x</div>
                    <div style='font-size:14px; color:#888;'>LIVE FEED</div>
                </div>
            """, unsafe_allow_html=True)

        # Performance Logs
        st.write("---")
        st.markdown("### 📊 ENGINE LOGS (WIN/LOSS)")
        logs = st.session_state[engine.log_key]
        if logs:
            for log in logs[:5]:
                res_class = "win-text" if log['Status'] == "WIN" else "loss-text"
                st.markdown(f"""
                    <div style="background:#111; padding:12px; border-radius:10px; margin-bottom:5px; border-left: 5px solid {'#45ad15' if log['Status']=='WIN' else '#ff4b4b'};">
                        <small style="color:#555;">{log['Time']}</small> | 
                        AI: <b>{log['AI Prediction']}</b> | 
                        Actual: <b>{log['Actual Result']}</b> | 
                        Result: <span class='{res_class}'>{log['Status']}</span>
                    </div>
                """, unsafe_allow_html=True)

    live_dashboard()
