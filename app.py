import streamlit as st
import urllib.parse

# 1. SETUP - KUGIRA NGO APP ISA NEZA KURI TELEFONE NA PC
st.set_page_config(page_title="AI Predator", page_icon="💰")

# --- STYLE Y'IBANGA (CYBER-PUNK LOOK) ---
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #00FF41; }
    .stTextInput>div>div>input, .stTextArea>div>textarea {
        background-color: #111; color: #00FF41; border: 1px solid #00FF41;
    }
    .stButton>button {
        background-color: #00FF41; color: black; width: 100%; border-radius: 5px; font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🧛‍♂️ BUSINESS PREDATOR AI")
st.write("Target. Analyze. Close. 💰")

# --- 2. INPUTS ---
col1, col2 = st.columns(2)

with col1:
    name = st.text_input("Izina rya Business", placeholder="Urugero: Simba Cafe")
    owner = st.text_input("Izina rya Nyirayo", placeholder="Urugero: Mr. Bosco")

with col2:
    biz_type = st.selectbox("Icyo bakora", ["Restaurant", "Boutique", "Construction", "Hospitality", "Salon"])
    problem = st.selectbox("Ikibazo ubonye", ["Abakiriya ni bake", "Ntabwo mugaragara kuri Google", "Imbuga nkoranyambaga zishaje"])

# --- 3. LOGIC & GENERATION ---
if st.button("🔥 GENERATE CLOSING SCRIPT"):
    if not name:
        st.error("Wibagiwe gushyiramo izina rya Business!")
    else:
        # AI Script Generation
        salutation = f"Mwaramutse {owner}" if owner else f"Mwaramutse ba nyiri {name}"
        
        message = f"""{salutation},

Nitegereje uburyo {name} ikora muri uyu mujyi, mbona service yanyu ya {biz_type} ni nziza. Ariko hari ikibazo nabonye gishobora gutuma muhomba abakiriya: *{problem}*.

Nk'inzobere muri **AI Systems**, nateguye uburyo bw'ibanga (AI Automation) bwabafasha gukemura iki kibazo mu masaha 24 gusa, maze mukikuba 2x mu bakiriya.

Ese nshobora kukoherereza Demo y'iminota 2 gusa nkwereke uko bikora? 

Urakoze, ni Divin."""

        # Kwerekana Message muri App
        st.subheader("📋 Copy message n'ubundi buryo:")
        st.code(message, language="text")

        # Gukora WhatsApp Link idafite error
        encoded_message = urllib.parse.quote(message)
        wa_url = f"https://wa.me/?text={encoded_message}"
        
        st.markdown(f'''
            <a href="{wa_url}" target="_blank" style="text-decoration: none;">
                <div style="background-color: #25d366; color: white; padding: 15px; text-align: center; border-radius: 10px; font-weight: bold; font-size: 20px;">
                    📲 SEND VIA WHATSAPP
                </div>
            </a>
        ''', unsafe_allow_html=True)

# --- 4. THE FREE GIFT (LOGO/MENU AI) ---
st.write("---")
st.info("💡 **Pro-Tip:** Mbere yo kumwandikira, koresha AI ukore Logo nshya cyangwa Menu nziza uyimuhere ubuntu (Free Gift) nk'icyitegererezo!")
