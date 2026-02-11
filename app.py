import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="Aviator AI Fixer")

# --- CONNECTION ---
try:
    # Fata email robot iri gukoresha muri Secrets
    robot_email = st.secrets["connections"]["gsheets"]["client_email"]
    
    conn = st.connection("gsheets", type=GSheetsConnection)
    SHEET_URL = "https://docs.google.com/spreadsheets/d/1M2v_43rTRe-ABlg5gkU2gYoT7dxxVq4-IgqNpGCCxmI/edit#gid=0"
    
    # Gerageza gusoma amakuru
    df = conn.read(spreadsheet=SHEET_URL, worksheet=0, ttl=0)
    
    st.success("✅ CONNECTION SUCCESSFUL!")
    st.write("Abakoresha bahari:")
    st.dataframe(df)

except Exception as e:
    st.error("❌ CONNECTION FAILED")
    st.warning(f"Robot iri kugerageza kwinjira ni: {robot_email}")
    st.info("Jya muri Google Sheet, uhe iyi email uburenganzira bwa 'Editor'.")
    st.code(str(e))
