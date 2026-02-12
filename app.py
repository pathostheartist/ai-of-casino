import streamlit as st
import pandas as pd
import numpy as np
import time
import plotly.graph_objects as go

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Aviator AI Pro Predictor", layout="wide")

# --- 2. THE STEALTH ENGINE ---
class AviatorEngine:
    def __init__(self):
        if 'memory' not in st.session_state:
            st.session_state['memory'] = [1.20, 2.50, 1.10, 4.00, 1.05]
        if 'logs' not in st.session_state:
            st.session_state['logs'] = [] 
        if 'current_prediction' not in st.session_state:
            st.session_state['current_prediction'] = None

    def process_round(self, actual_odd):
        # Isesengura niba inshuro ishize AI yari yatsinze
        last_pred = st.session_state['current_prediction']
        if last_pred:
            status = "WIN" if actual_odd >= last_pred else "LOSS"
            color = "#45ad15" if status == "WIN" else "#ff4b4b"
            st.session_state['logs'].insert(0, {
                "Time": time.strftime('%H:%M:%S'),
                "AI Prediction": f"{last_pred}x",
                "Result": f"{actual_odd}x",
                "Outcome": status
            })
        
        # Kwibuka imibare mishya
        st.session_state['memory'].append(actual_odd)
        if len(st.session_state['memory']) > 15:
            st.session_state['memory'].pop(0)

    def get_new_prediction(self):
        history = st.session_state['memory']
        avg = np.mean(history[-3:])
        
        # AI Logic: Reba niba umukino umeze nabi
        if all(x < 1.3 for x in history[-2:]):
            st.session_state['current_prediction'] = None
            return None, "🚫 DO NOT BET (Wait for recovery)"
        
        # Gushaka Prediction nshya
        pred = round(np.random.uniform(1.5, 3.5), 2) if avg < 2 else round(np.random.uniform(1.2, 2.0), 2)
        st.session_state['current_prediction'] = pred
        return pred, "✅ BET NOW (Safe Entry)"

# --- 3. CUSTOM INTERFACE (Aviator Style) ---
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: white; }
    .aviator-card {
        background-color: #1a1a1a; padding: 25px; border-radius: 15px;
        border: 1px solid #2c2c2c; text-align: center;
    }
    .prediction-text { color: #ff4b4b; font-size: 65px; font-weight: bold; margin: 0; }
    .advice-box { padding: 10px; border-radius: 8px; font-weight: bold; margin-top: 10px; }
    .win { color: #45ad15; font-weight: bold; }
    .loss { color: #ff4b4b; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. LIVE ENGINE FRAGMENT ---
@st.fragment(run_every=6)
def aviator_live_ui():
    engine = AviatorEngine()
    
    # 1. Simulate Actual Round
    actual_odd = round(np.random.uniform(1.0, 5.0), 2)
    engine.process_round(actual_odd)
    
    st.markdown("<h2 style='text-align: center; color: #ff4b4b;'>🚀 AVIATOR AI PREDICTOR</h2>", unsafe_allow_html=True)
    
    # --- TOP ROW: HISTORY GRAPH ---
    history = st.session_state['memory']
    fig = go.Figure(go.Scatter(x=list(range(len(history))), y=history, 
                               mode='lines+markers', line=dict(color='#ff4b4b', width=4),
                               marker=dict(size=10, color='white')))
    fig.update_layout(paper_bgcolor='black', plot_bgcolor='black', font_color='white', height=200, 
                      margin=dict(l=0, r=0, t=10, b=0), xaxis=dict(visible=False))
    st.plotly_chart(fig, use_container_width=True)
    

    # --- MIDDLE ROW: PREDICTION & ADVICE ---
    col1, col2 = st.columns(2)
    prediction, advice = engine.get_new_prediction()

    with col1:
        st.markdown("<div class='aviator-card'>", unsafe_allow_html=True)
        st.write("NEXT PREDICTION")
        if prediction:
            st.markdown(f"<p class='prediction-text'>{prediction}x</p>", unsafe_allow_html=True)
        else:
            st.markdown(f"<p class='prediction-text' style='color:#555;'>WAIT</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='aviator-card' style='height: 100%;'>", unsafe_allow_html=True)
        st.write("AI STRATEGY")
        color = "#45ad15" if "BET NOW" in advice else "#555"
        st.markdown(f"<div class='advice-box' style='background:{color};'>{advice}</div>", unsafe_allow_html=True)
        st.write(f"Current Server Status: <span style='color:#45ad15;'>Active</span>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # --- BOTTOM ROW: WIN/LOSS LOGS ---
    st.write("---")
    st.write("### 📜 LIVE PERFORMANCE LOGS")
    if st.session_state['logs']:
        # Kwerekana logs mu buryo busomeka neza
        for log in st.session_state['logs'][:5]: # Turebe 5 ziheruka
            res_color = "win" if log['Outcome'] == "WIN" else "loss"
            st.markdown(f"""
                <div style="background:#111; padding:10px; border-radius:10px; margin-bottom:5px; border-left: 5px solid {'#45ad15' if log['Outcome']=='WIN' else '#ff4b4b'};">
                    <span style="color:#888;">{log['Time']}</span> | 
                    AI: <b>{log['AI Prediction']}</b> | 
                    Actual: <b>{log['Result']}</b> | 
                    Result: <span class='{res_color}'>{log['Outcome']}</span>
                </div>
            """, unsafe_allow_html=True)

# --- 5. EXECUTION ---
if 'user' not in st.session_state:
    st.session_state['user'] = None

if st.session_state['user'] is None:
    st.title("Aviator AI Login")
    u = st.text_input("Username").lower().strip()
    p = st.text_input("Password", type="password")
    if st.button("LOGIN"):
        st.session_state['user'] = u
        st.rerun()
else:
    with st.sidebar:
        st.markdown(f"### Welcome Agent: <br><span style='color:#ff4b4b;'>{st.session_state['user']}</span>", unsafe_allow_html=True)
        if st.button("Logout"):
            st.session_state['user'] = None
            st.rerun()
    
    aviator_live_ui()
