import streamlit as st
import pandas as pd
import numpy as np
import time
import plotly.graph_objects as go

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="AI Neural Deep Scanner", layout="wide")

# --- 2. THE DEEP NEURAL ENGINE ---
class DeepNeuralEngine:
    def __init__(self, game):
        self.game = game
        self.mem_key = f'mem_{game}'
        self.archive_key = f'archive_{game}'
        self.log_key = f'log_{game}'
        self.streak_key = f'streak_{game}'
        
        # Memory y'ako kanya (Recent)
        if self.mem_key not in st.session_state:
            st.session_state[self.mem_key] = [1.2, 2.8, 1.1, 3.5, 1.05]
        # Archive ya kera (Long-term)
        if self.archive_key not in st.session_state:
            st.session_state[self.archive_key] = [2.1, 1.05, 5.8, 1.1, 1.4, 2.0, 1.0, 3.2]
        # Logs n'ibindi
        if self.log_key not in st.session_state:
            st.session_state[self.log_key] = []
        if self.streak_key not in st.session_state:
            st.session_state[self.streak_key] = 0

    def analyze_deep_history(self):
        """AI isesengura cycles za kera ikazigereranya n'iz'ubu"""
        recent = st.session_state[self.mem_key][-3:]
        archive = st.session_state[self.archive_key]
        
        matches = 0
        # Igereranya pattern y'ubu n'amateka yose ya kera
        for i in range(len(archive) - 3):
            if archive[i:i+3] == recent:
                matches += 1
        
        confidence = 70 + (matches * 15)
        return min(confidence, 99)

    def update_engine(self, actual_odd, pred_val):
        # 1. Update Streak
        if pred_val and actual_odd >= pred_val:
            st.session_state[self.streak_key] += 1
            status = "WIN"
        else:
            st.session_state[self.streak_key] = 0
            status = "LOSS"

        # 2. Add to Logs
        st.session_state[self.log_key].insert(0, {
            "Time": time.strftime('%H:%M:%S'),
            "AI": f"{pred_val}x" if pred_val else "---",
            "Actual": f"{actual_odd}x",
            "Status": status
        })

        # 3. Add to Memory & Archive
        st.session_state[self.mem_key].append(actual_odd)
        st.session_state[self.archive_key].append(actual_odd)
        
        # Limit memory
        if len(st.session_state[self.mem_key]) > 20: st.session_state[self.mem_key].pop(0)
        if len(st.session_state[self.archive_key]) > 100: st.session_state[self.archive_key].pop(0)

# --- 3. UI & CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: white; }
    .streak-badge {
        background: linear-gradient(90deg, #45ad15, #1d5a0a);
        padding: 10px 20px; border-radius: 10px; font-weight: bold;
        text-align: center; font-size: 18px; border: 1px solid #45ad15;
    }
    .prediction-box {
        background: #111; padding: 20px; border-radius: 15px;
        border: 2px solid #ff4b4b; text-align: center;
    }
    .archive-scanner {
        font-family: 'Courier New', monospace; font-size: 12px; color: #45ad15;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. LOGIN ---
if 'user' not in st.session_state:
    st.session_state['user'] = None

if st.session_state['user'] is None:
    st.markdown("<h2 style='text-align:center;'>DEEP NEURAL LOGIN</h2>", unsafe_allow_html=True)
    u = st.text_input("Agent ID")
    p = st.text_input("Access Key", type="password")
    if st.button("LOGIN", use_container_width=True):
        st.session_state['user'] = u
        st.rerun()
else:
    # --- 5. SIDEBAR ---
    with st.sidebar:
        st.markdown("### ⚙️ ADMIN CONTROL")
        game_choice = st.sidebar.radio("CHOOSE ENGINE", ["AVIATOR", "JETX"])
        st.write("---")
        st.write("📈 Deep Scan Status: **Active**")
        st.write(f"🗄️ Archive Size: **{len(st.session_state.get(f'archive_{game_choice}', []))} entries**")
        if st.sidebar.button("EXIT SYSTEM", use_container_width=True):
            st.session_state['user'] = None
            st.rerun()

    primary_color = "#ff4b4b" if game_choice == "AVIATOR" else "#ffcc00"
    engine = DeepNeuralEngine(game_choice)

    @st.fragment(run_every=6)
    def dashboard():
        # Get Current Prediction before update
        conf = engine.analyze_deep_history()
        pred_val = round(np.random.uniform(1.6, 3.5), 2) if conf > 75 else None
        
        # Simulate Round
        actual_odd = round(np.random.uniform(1.0, 5.0), 2)
        engine.update_engine(actual_odd, pred_val)

        st.markdown(f"<h2 style='text-align:center; color:{primary_color};'>{game_choice} DEEP ANALYZER</h2>", unsafe_allow_html=True)

        # Streak Counter
        streak = st.session_state[engine.streak_key]
        if streak > 1:
            st.markdown(f"<div class='streak-badge'>🔥 WINNING STREAK: {streak} IN A ROW!</div>", unsafe_allow_html=True)
            st.write("")

        # Main Layout
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"""
                <div class='prediction-box' style='border-color:{primary_color};'>
                    <div style='color:#888;'>NEXT SIGNAL</div>
                    <div style='font-size:50px; font-weight:bold; color:{primary_color};'>{pred_val if pred_val else 'WAIT'}x</div>
                    <div class='archive-scanner'>SCANNING DEEP ARCHIVE... {conf}% MATCH</div>
                </div>
            """, unsafe_allow_html=True)
            
        with c2:
            st.markdown(f"""
                <div class='prediction-box' style='border-color:#444;'>
                    <div style='color:#888;'>ACTUAL RESULT</div>
                    <div style='font-size:50px; font-weight:bold; color:white;'>{actual_val}x</div>
                    <div style='color:#888; font-size:12px;'>ROUND SYNCED</div>
                </div>
            """, unsafe_allow_html=True)

        # Graph
        history = st.session_state[engine.mem_key]
        fig = go.Figure(go.Scatter(x=list(range(len(history))), y=history, mode='lines+markers', line=dict(color=primary_color, width=4)))
        fig.update_layout(paper_bgcolor='black', plot_bgcolor='black', font_color='white', height=180, margin=dict(l=0,r=0,t=0,b=0), xaxis=dict(visible=False))
        st.plotly_chart(fig, use_container_width=True)

        # Logs
        st.write("---")
        st.markdown("### 📊 LIVE ENGINE FEED")
        for log in st.session_state[engine.log_key][:5]:
            color = "#45ad15" if log['Status'] == "WIN" else "#ff4b4b"
            st.markdown(f"""
                <div style="background:#111; padding:10px; border-radius:10px; margin-bottom:5px; border-left: 5px solid {color};">
                    AI: <b>{log['AI']}</b> | Result: <b>{log['Actual']}</b> | <span style="color:{color}; font-weight:bold;">{log['Status']}</span>
                </div>
            """, unsafe_allow_html=True)

    dashboard()
