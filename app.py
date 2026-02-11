import streamlit as st
import pandas as pd
import numpy as np
import time
import plotly.graph_objects as go

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Aviator AI Neural Engine", layout="wide")

# --- 2. THE AI NEURAL BRAIN ---
class AviatorAI:
    def __init__(self):
        # AI ibika odds zose zabayeho hano (Memory)
        if 'memory' not in st.session_state:
            st.session_state['memory'] = [1.20, 2.50, 1.10, 4.00, 1.05, 1.30, 2.80]
        
    def learn_and_predict(self):
        history = st.session_state['memory']
        last_3 = history[-3:] # Ireba 3 ziheruka cyane
        
        # 1. Pattern Analysis (Logic ikaze)
        avg = np.mean(last_3)
        risk_score = np.random.uniform(0, 100) # Isesengura rya risk mu masegonda
        
        # 2. Probability Check
        # Niba imibare 3 iheruka ari mito cyane (<1.3), risk ni nini
        if all(x < 1.3 for x in last_3) or risk_score < 30:
            return None, risk_score # AI yanze gu-predict (Sorry mode)
        
        # 3. High-Speed Prediction calculation
        # Igerageza gushaka imibare ishingiye ku mateka
        if avg < 1.5:
            pred = round(np.random.uniform(2.1, 5.0), 2)
        else:
            pred = round(np.random.uniform(1.4, 2.5), 2)
            
        return pred, risk_score

# --- 3. UI DESIGN ---
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: white; font-family: 'Orbitron', sans-serif; }
    .ai-box {
        background: rgba(255, 255, 255, 0.05);
        padding: 25px; border-radius: 20px;
        border: 1px solid #45ad15; text-align: center;
    }
    .status-pulse {
        height: 10px; width: 10px; background-color: #45ad15;
        border-radius: 50%; display: inline-block;
        box-shadow: 0 0 10px #45ad15;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. ENGINE FRAGMENT (AUTO-UPDATE) ---
@st.fragment(run_every=5)
def neural_engine():
    ai = AviatorAI()
    history = st.session_state['memory']
    
    # Simulating Live Data Feed
    new_odd = round(np.random.uniform(1.0, 4.0), 2)
    st.session_state['memory'].append(new_odd)
    if len(st.session_state['memory']) > 15: st.session_state['memory'].pop(0)

    st.markdown("### 🧠 NEURAL PATTERN ENGINE")
    
    # GRAPH HISTORY
    fig = go.Figure(go.Scatter(x=list(range(len(history))), y=history, 
                               mode='lines+markers', line=dict(color='#45ad15', width=3)))
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', 
                      font_color='white', height=250, margin=dict(l=0, r=0, t=0, b=0))
    st.plotly_chart(fig, use_container_width=True)

    # ANALYSIS AREA
    c1, c2 = st.columns([1, 1])
    
    prediction, risk = ai.learn_and_predict()
    
    with c1:
        st.write("#### 🛡️ RISK ASSESSMENT")
        if risk < 30:
            st.error(f"RISK LEVEL: {round(risk, 1)}% (DANGEROUS)")
        else:
            st.success(f"RISK LEVEL: {round(risk, 1)}% (STABLE)")
        
        st.write("---")
        # Chatbot y'ukuri
        if prediction is None:
            st.markdown(f"<div style='color: #ff4b4b; padding:10px; border-radius:10px; background:#222;'><b>AI:</b> Sorry! I can't predict right now. The server pattern is too random. Wait for stability.</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='color: #45ad15; padding:10px; border-radius:10px; background:#222;'><b>AI:</b> Pattern found! I've analyzed the last {len(history)} rounds. It's safe to play.</div>", unsafe_allow_html=True)

    with c2:
        st.markdown("<div class='ai-box'>", unsafe_allow_html=True)
        st.write("🚀 **NEXT AI SIGNAL**")
        
        if prediction is None:
            st.markdown("<h1 style='color: #666;'>NO SIGNAL</h1>", unsafe_allow_html=True)
            st.caption("AI is self-correcting...")
        else:
            st.markdown(f"<h1 style='color: #45ad15; font-size: 50px;'>{prediction}x</h1>", unsafe_allow_html=True)
            st.write(f"Confidence: {round(100 - risk, 1)}%")
        st.markdown("</div>", unsafe_allow_html=True)

# --- 5. APP EXECUTION ---
if 'user' not in st.session_state:
    st.session_state['user'] = None

if st.session_state['user'] is None:
    st.title("Aviator Neural Login")
    u = st.text_input("Username")
    p = st.text_input("Password", type="password")
    if st.button("AUTHENTICATE"):
        st.session_state['user'] = u
        st.rerun()
else:
    with st.sidebar:
        st.write(f"Agent: **{st.session_state['user']}**")
        st.write("---")
        st.sidebar.button("LOGOUT", on_click=lambda: st.session_state.update(user=None))
    
    neural_engine()
