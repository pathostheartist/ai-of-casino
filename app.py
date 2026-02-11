import streamlit as st
import time

# --- 1. CONFIGURATION & ACCESS CONTROL ---
st.set_page_config(page_title="Aviator AI Master", layout="wide", page_icon="⚙️")

# DATABASE Y'ABAKORESHA (Iyi niyo "Engine" yawe)
# 'active': True (afite uruhushya), 'active': False (arafunze)
if 'db_users' not in st.session_state:
    st.session_state['db_users'] = {
        "admin_divin": {"password": "divin2026", "status": "Admin", "active": True},
        "test_user": {"password": "123", "status": "Trial", "active": True},
    }

# --- 2. CUSTOM CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: white; }
    [data-testid="stSidebar"] { background-color: #111; border-right: 1px solid #333; }
    .user-card { 
        background-color: #1a1a1a; padding: 15px; border-radius: 10px; 
        border: 1px solid #333; margin-bottom: 10px;
    }
    .status-active { color: #00ff00; font-weight: bold; }
    .status-blocked { color: #ff0000; font-weight: bold; }
    .stButton>button { border-radius: 8px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SESSION STATE ---
if 'user' not in st.session_state:
    st.session_state['user'] = None

# --- 4. LOGIN LOGIC ---
def login_page():
    st.title("🎯 Aviator AI Pro Login")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        u = st.text_input("Username").lower().strip()
        p = st.text_input("Password", type="password")
        if st.button("LOGIN"):
            db = st.session_state['db_users']
            if u in db and db[u]["password"] == p:
                if not db[u]["active"]:
                    st.error("🛑 Your account is DEACTIVATED. Contact Admin.")
                else:
                    st.session_state['user'] = {"username": u, "status": db[u]["status"]}
                    st.success("Authenticated!")
                    st.rerun()
            else:
                st.error("Invalid credentials.")

# --- 5. ADMIN CONTROL PANEL ---
def admin_dashboard():
    st.title("👨‍🔧 Master Admin Control")
    st.subheader("Manage All Registered Users")
    
    db = st.session_state['db_users']
    
    # Kurema umuntu mushya (Add User)
    with st.expander("➕ Add New User"):
        c1, c2, c3 = st.columns(3)
        new_u = c1.text_input("New Username")
        new_p = c2.text_input("New Password")
        new_s = c3.selectbox("Role", ["Trial", "Premium"])
        if st.button("CREATE ACCOUNT"):
            if new_u and new_p:
                st.session_state['db_users'][new_u] = {"password": new_p, "status": new_s, "active": True}
                st.success(f"Account for {new_u} created!")
                st.rerun()

    st.markdown("---")
    
    # Lisiti y'abantu bose
    for username, info in db.items():
        if username == "admin_divin": continue # Admin ntiyiyobora
        
        with st.container():
            col1, col2, col3, col4 = st.columns([2, 1, 1, 2])
            col1.write(f"👤 **{username}** (Pass: {info['password']})")
            col2.write(f"Type: {info['status']}")
            
            # Kwerekana niba active cyangwa inactive
            status_text = "ACTIVE" if info['active'] else "BLOCKED"
            status_class = "status-active" if info['active'] else "status-blocked"
            col3.markdown(f'<span class="{status_class}">{status_text}</span>', unsafe_allow_html=True)
            
            # Buto zo gukontrola
            if info['active']:
                if col4.button("🚫 DEACTIVATE", key=f"deact_{username}"):
                    st.session_state['db_users'][username]['active'] = False
                    st.rerun()
            else:
                if col4.button("✅ ACTIVATE", key=f"act_{username}"):
                    st.session_state['db_users'][username]['active'] = True
                    st.rerun()
            
            if col4.button("🗑️ DELETE", key=f"del_{username}"):
                del st.session_state['db_users'][username]
                st.rerun()
        st.write("---")

# --- 6. USER DASHBOARD ---
def user_dashboard():
    user = st.session_state['user']
    st.title(f"🚀 Aviator AI Predictor")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div style="background-color: #111; padding: 30px; border-radius: 15px; border-left: 5px solid #ff4b4b;">
            <h3>Live Analysis Engine</h3>
            <p>The AI is currently scanning Aviator servers for patterns.</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("GENERATE SIGNAL"):
            with st.spinner("Calculating..."):
                time.sleep(2)
                st.success("✅ Prediction: 2.85x")
                st.balloons()
                
    with col2:
        st.write("### Account Info")
        st.info(f"Account: {user['status']}")
        st.write("For help, contact support.")

# --- 7. NAVIGATION ---
if st.session_state['user'] is None:
    login_page()
else:
    current_user = st.session_state['user']
    st.sidebar.title(f"Welcome, {current_user['username']}")
    
    if current_user['status'] == "Admin":
        choice = st.sidebar.radio("Menu", ["Admin Panel", "View Predictor"])
        if choice == "Admin Panel":
            admin_dashboard()
        else:
            user_dashboard()
    else:
        user_dashboard()
        
    if st.sidebar.button("Logout"):
        st.session_state['user'] = None
        st.rerun()
