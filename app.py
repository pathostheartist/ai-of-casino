import streamlit as st
import pandas as pd
import numpy as np
import time
import plotly.graph_objects as go

# --- 1. CONFIGURATION (Responsiveness starts here) ---
st.set_page_config(
    page_title="Aviator AI Pro Predictor",
    layout="wide", # Ibi bituma App ikoresha screen yose
    initial_sidebar_state="collapsed"
)

# --- 2. ENGINE LOGIC ---
class AviatorEngine:
    def __init__(self):
        if 'memory' not in st.session_state:
            st.session_state['memory'] = [1.20, 2.50, 1.10, 4.00, 1.05]
        if 'logs' not in st.session_state:
            st.session_state['logs'] = [] 
        if 'current_prediction' not in st.session_state:
            st.session_state['current_prediction'] = None

    def process_round(self, actual_odd):
        last_pred = st.session_state['current_prediction']
        if last_pred:
            status = "WIN" if actual_odd >= last_pred else "LOSS"
            st.session_state['logs'].insert(0, {
                "Time": time.strftime('%H:%M:%S'),
                "AI Prediction": f"{last_pred}x",
                "Result": f"{actual_odd}x",
                "Outcome": status
            })
        st.session_state['memory'].append(actual_odd)
        if len(st.session_state['memory']) > 15:
            st.session_state['memory'].pop(0)

    def get_new_prediction(self):
        history = st.session_state['memory']
        avg = np.mean(history[-3:])
        if all(x < 1.3 for x in history[-2:]):
            st.session_state['current_prediction'] = None
            return None, "🚫 DO NOT BET"
        pred = round(np.random.uniform(1.5, 3.2), 2)
        st.session_state['current_prediction'] = pred
        return pred, "✅ BET NOW"

# --- 3. RESPONSIVE CSS & STYLING ---
st.markdown("""
    <style>
    /* Responsive container */
    .stApp { background-color: #000000; color: white; }
    
    /* Making cards responsive */
    .main-container {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        justify-content: center;
    }
    
    .aviator-card {
        background-color: #1a1a1a;
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #2c2c2c;
        text-align: center;
        flex: 1 1 300px; /* This makes it responsive on mobile */
        margin: 5px;
    }
    
    .prediction-text { color: #ff4b4b; font-size: clamp(40px, 10vw, 70px); font-weight: bold; }
    
    /* Contact Buttons */
    .contact-btn {
        display: block;
        width: 100%;
        padding: 12px;
        margin: 10px 0;
        text-align: center;
        border-radius: 8px;
        text-decoration: none;
        font-weight: bold;
        transition: 0.3s;
    }
    .whatsapp { background-color: #25d366; color: white; }
    .email { background-color: #ea4335; color: white; }
    
    /* Table responsiveness */
    .log-container { overflow-x: auto; }
    
    .win { color: #45ad15; font-weight: bold; }
    .loss { color: #ff4b4b; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. LIVE ENGINE FRAGMENT ---
@st.fragment(run_every=6)
def aviator_live_ui():
    engine = AviatorEngine()
    actual_odd = round(np.random.uniform(1.0, 4.5), 2)
    engine.process_round(actual_odd)
    
    st.markdown("<h2 style='text-align: center; color: #ff4b4b;'>🚀 AVIATOR AI PRO</h2>", unsafe_allow_html=True)
    
    # --- GRAPH ---
    history = st.session_state['memory']
    fig = go.Figure(go.Scatter(x=list(range(len(history))), y=history, 
                               mode='lines+markers', line=dict(color='#ff4b4b', width=4)))
    fig.update_layout(paper_bgcolor='black', plot_bgcolor='black', font_color='white', height=200, 
                      margin=dict(l=0, r=0, t=10, b=0), xaxis=dict(visible=False))
    st.plotly_chart(fig, use_container_width=True)

    # --- RESPONSIVE CARDS ---
    prediction, advice = engine.get_new_prediction()
    
    col1, col2 = st.columns([1, 1]) # Automatically stacks on mobile in newer Streamlit
    
    with col1:
        st.markdown(f"""
            <div class='aviator-card'>
                <div style='color:#888;'>NEXT PREDICTION</div>
                <div class='prediction-text'>{prediction if prediction else 'WAIT'}x</div>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        bg_advice = "#45ad15" if "BET" in advice else "#444"
        st.markdown(f"""
            <div class='aviator-card'>
                <div style='color:#888;'>AI STRATEGY</div>
                <div style='background:{bg_advice}; padding:15px; border-radius:10px; margin-top:10px; font-weight:bold;'>
                    {advice}
                </div>
            </div>
        """, unsafe_allow_html=True)

    # --- CONTACT SECTION (RESPONSIVE) ---
    st.write("---")
    st.markdown("### 💬 SUPPORT & UPGRADE")
    c_col1, c_col2 = st.columns(2)
    
    with c_col1:
        st.markdown('<a href="https://wa.me/250780000000" class="contact-btn whatsapp">Chat on WhatsApp</a>', unsafe_allow_html=True)
    with c_col2:
        # Change 'yourname@email.com' to your real email
        st.markdown('<a href="mailto:divin@email.com?subject=Aviator AI Access" class="contact-btn email">Contact via Email</a>', unsafe_allow_html=True)

    # --- LOGS ---
    st.write("### 📜 PERFORMANCE LOGS")
    if st.session_state['logs']:
        for log in st.session_state['logs'][:5]:
            res_color = "win" if log['Outcome'] == "WIN" else "loss"
            st.markdown(f"""
                <div style="background:#111; padding:10px; border-radius:10px; margin-bottom:5px; border-left: 5px solid {'#45ad15' if log['Outcome']=='WIN' else '#ff4b4b'};">
                    <small style="color:#666;">{log['Time']}</small> | AI: <b>{log['AI Prediction']}</b> | Actual: <b>{log['Result']}</b> | <span class='{res_color}'>{log['Outcome']}</span>
                </div>
            """, unsafe_allow_html=True)

# --- 5. EXECUTION ---
if 'user' not in st.session_state:
    st.session_state['user'] = None

if st.session_state['user'] is None:
    st.markdown("<h2 style='text-align:center;'>AVIATOR AI LOGIN</h2>", unsafe_allow_html=True)
    u = st.text_input("Username").lower().strip()
    p = st.text_input("Password", type="password")
    if st.button("LOGIN", use_container_width=True):
        st.session_state['user'] = u
        st.rerun()
else:
    with st.sidebar:
        st.write(f"Agent: **{st.session_state['user']}**")
        if st.button("Logout", use_container_width=True):
            st.session_state['user'] = None
            st.rerun()
    
    aviator_live_ui()
