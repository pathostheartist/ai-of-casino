import streamlit as st
import urllib.parse

# --- 1. SYSTEM CONFIGURATION ---
st.set_page_config(page_title="AI Predator Full System", layout="wide")

# Custom CSS for Professional Dark Mode
st.markdown("""
    <style>
    .main { background-color: #0a0a0a; color: #ffffff; }
    .stButton>button { background: linear-gradient(45deg, #00FF41, #008F11); color: black; font-weight: bold; border: none; height: 3em; }
    .biz-card { background-color: #161616; padding: 20px; border-radius: 10px; border: 1px solid #333; margin-bottom: 20px; }
    </style>
""", unsafe_allow_html=True)

# --- 2. HEADER ---
st.title("🏹 AI BUSINESS PREDATOR: FULL SYSTEM")
st.write("2026 Edition - Automated Business Intelligence")

# --- 3. THE HUNTER & THE CLOSER (USER INTERFACE) ---
tabs = st.tabs(["🎯 Target Hunter", "🛠️ AI Service Tools", "📊 Revenue Tracker"])

with tabs[0]:
    st.header("Step 1: Identify & Reach Out")
    col1, col2 = st.columns([1, 1.5])
    
    with col1:
        st.markdown('<div class="biz-card">', unsafe_allow_html=True)
        biz_name = st.text_input("Izina rya Business")
        biz_owner = st.text_input("Nyirayo (Niba umuzi)")
        biz_cat = st.selectbox("Icyo bakora", ["Restaurant", "Fashion", "Real Estate", "Tech Store", "Beauty Salon"])
        biz_problem = st.selectbox("Ikibazo ugiye gukemura", [
            "Nta Website bafite (Loss of trust)",
            "Menu/Price list yabo ni mbi",
            "Ntabwo bagaragara kuri Google Maps",
            "Instagram yabo ntabwo ikurura abantu"
        ])
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        if st.button("GENERATE ULTIMATE PROPOSAL"):
            if biz_name:
                # Advanced AI Logic for the Proposal
                proposal = f"""*Mwaramutse {biz_owner if biz_owner else 'ba nyiri ' + biz_name},*

Nitegereje uburyo {biz_name} ikora muri uyu mujyi, mbona service yanyu ya {biz_cat} ni nziza. Ariko hari ikibazo nabonye: *{biz_problem}*.

Ibi bituma abakiriya benshi bahitamo kujya mu bandi. Nk'inzobere muri **AI Systems**, nateguye uburyo (AI Automation) bwabafasha gukemura iki kibazo mu masaha 24 gusa, maze mukikuba 2x mu bakiriya.

Ese nshobora kukoherereza Demo y'iminota 2 nkwereke uko bikora? 

Urakoze, ni Divin."""
                
                st.subheader("🚀 Ready to Send:")
                st.info(proposal)
                
                # WhatsApp Integration
                encoded_msg = urllib.parse.quote(proposal)
                st.markdown(f'<a href="https://wa.me/?text={encoded_msg}" target="_blank" style="background-color: #25d366; color: white; padding: 15px; border-radius: 8px; text-decoration: none; display: block; text-align: center; font-weight: bold;">📲 SEND VIA WHATSAPP</a>', unsafe_allow_html=True)
            else:
                st.warning("Banza ushyiremo izina rya Business!")

with tabs[1]:
    st.header("Step 2: Provide the Service (The AI Tools)")
    st.write("Iyo umukiriya akubwiye 'YES', koresha izi mbuga gukora akazi mu masegonda:")
    
    tools = [
        {"Service": "Website Creator", "Tool": "Durable.co / 10Web", "Time": "30 Seconds"},
        {"Service": "Professional Logo", "Tool": "Looka.com / Canva AI", "Time": "1 Minute"},
        {"Service": "Marketing Video", "Tool": "InVideo AI / HeyGen", "Time": "2 Minutes"},
        {"Service": "Menu/Flyer Design", "Tool": "Canva Magic Design", "Time": "1 Minute"}
    ]
    st.table(tools)
    st.info("💡 **Predator Secret:** Kora sample imwe muri izi uyimuhere ubuntu (Free Trial), hanyuma umubwire ko ibindi bishaka kwishyurwa.")

with tabs[2]:
    st.header("Step 3: Track Your Money")
    goal = st.number_input("Goal yawe y'ukwezi (FRW)", value=500000)
    current = st.slider("Ayo umaze kwinjiza (FRW)", 0, goal, 0)
    st.progress(current / goal)
    st.write(f"Ubu ugeze kuri **{(current/goal)*100:.1f}%** ya goal yawe!")

# --- 4. FOOTER ---
st.markdown("---")
st.caption("AI Predator System v2.0 - Designed for Divin. Execute with precision.")
