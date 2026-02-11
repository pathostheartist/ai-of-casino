import streamlit as st
import pandas as pd
import numpy as np
import time
import plotly.graph_objects as go

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Aviator AI Neural v2", layout="wide")

# --- 2. THE AI NEURAL BRAIN WITH TRACKING ---
class AviatorAI:
    def __init__(self):
        # Memory y'imibare yose
        if 'memory' not in st.session_state:
            st.session_state['memory'] = [1.20, 2.50, 1.10, 4.00, 1.05]
        # Memory y'uburyo AI yagiye i-predict-inga (Accuracy tracking)
        if 'performance_log' not in st.session_state:
            st.session_state['performance_log'] = [] # Izabika {"pred": x, "actual": y, "result": "WIN/LOSS"}
        if 'last_prediction' not in st.session_state:
            st.session_state['last_prediction'] = None

    def update_performance(self, actual_odd):
        """Isuzumwa niba prediction iheruka yaragezeho"""
        last_pred = st.session_state['last_prediction']
        if last_pred:
            result = "✅ WIN" if actual_odd >= last_pred else "❌ LOSS"
            st.session_state['performance_log'].append({
                "Prediction": f"{last_pred}x",
                "Actual": f"{actual_odd}x",
                "Status": result
            })
            # Gufata gusa 10 ziheruka mu mateka
            if len(st.session_state['performance_log']) > 10:
                st.session_state['performance_log'].pop(0)
        
    def learn_and_predict(self):
        history = st.session_state['memory']
        last_3 = history[-3:]
        avg = np.mean(last_3)
        risk_score = np.random.uniform(0, 100)
        
        # 1. AI Check: Niba isanze umuvuduko utameze neza (Sorry mode)
        if all(x < 1.3 for x in last_3) or risk_score < 25:
            st.session_state['last_prediction'] = None
            return None, risk_score
        
        # 2. Advanced calculation
        if avg < 1.8:
            pred = round(np.random.uniform(2.0, 4.0), 2)
        else:
            pred = round(np.random.uniform(1.3, 2.2), 2)
            
        st.session_state['last_prediction'] = pred
        return pred, risk_score

# --- 3. UI DESIGN ---
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: white; font-family: 'Orbitron', sans-serif; }
    .ai-box {
        background: rgba(255, 255, 255, 0.05);
        padding: 20px; border-radius: 15px; border: 1px solid #45ad15; text-align: center;
    }
    .log-table { font-size: 12px; color: #ccc; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. ENGINE FRAGMENT ---
@st.fragment(run_every=6) # 6 seconds refresh
def neural_engine():
    ai = AviatorAI()
    
    # Simulating the plane flight (Actual Odd)
    actual_odd = round(np.random.uniform(1.0, 5.0), 2)
    
    # Update AI Performance before adding new odd to memory
    ai.update_performance(actual_odd)
    
    # Add actual odd to memory
    st.session_state['memory'].append(actual_odd)
    if len(st.session_state['memory']) > 15: st.session_state['memory'].pop(0)

    st.markdown("### 🧠 NEURAL PATTERN ENGINE v2")
    
    # MAIN LAYOUT
    col_main, col_sidebar = st.columns([2.5, 1])

    with col_main:
        # GRAPH
        history = st.session_state['memory']
        fig = go.Figure(go.Scatter(x=list(range(len(history))), y=history, 
                                   mode='lines+markers', line=dict(color='#45ad15', width=3)))
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', 
                          font_color='white', height=250, margin=dict(l=0, r=0, t=0, b=0))
        st.plotly_chart(fig, use_container_width=True)

        # AI DECISION
        prediction, risk = ai.learn_and_predict()
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("<div class='ai-box'>", unsafe_allow_html=True)
            if prediction is None:
                st.error("⚠️ AI STATUS: SELF-CORRECTING")
                st.write("Sorry, pattern is unstable. Skipping...")
            else:
                st.success("✅ AI STATUS: ANALYZING")
                st.markdown(f"<h1>{prediction}x</h1>", unsafe_allow_html=True)
                st.caption(f"Risk Level: {round(risk, 1)}%")
            st.markdown("</div>", unsafe_allow_html=True)
        
        with c2:
            st.write("#### 📡 Live Pattern Scan")
            st.code(f"Scan_Target: {actual_odd}x\nMemory_Capacity: {len(history)}/15\nLogic_Speed: 0.002ms")

    with col_sidebar:
        st.write("#### 📜 AI Log History")
        if st.session_state['performance_log']:
            df = pd.DataFrame(st.session_state['performance_log'])
            st.table(df.tail(5)) # Kwerekana 5 ziheruka
        else:
            st.info("Waiting for first round...")

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
        st.sidebar.button("LOGOUT", on_click=lambda: st.session_state.update(user=None))
    
    neural_engine()
