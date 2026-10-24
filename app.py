import streamlit as st
from datetime import datetime

st.set_page_config(
    page_title="Asistent Concurs Feeder", 
    page_icon="🏆",
    layout="centered"
)

st.title("🏆 Asistent Concurs Method Feeder")

# Bara superioara de status si refresh
col1, col2 = st.columns([2, 1])
with col1:
    st.caption(f"🕒 Ultima verificare: **{datetime.now().strftime('%H:%M:%S')}**")
with col2:
    if st.button("🔄 Actualizează", use_container_width=True):
        st.rerun()

# Link-uri Google Form si Google Sheets direct catre Clasament General (gid=269019846)
form_url = "https://docs.google.com/forms/d/e/1FAIpQLSf67fr3GOWoGQ5-XDkKc924_nhzGZU4dg3bMQivtU5L8HNNng/viewform?embedded=true"
sheet_clasament_url = "https://docs.google.com/spreadsheets/d/1tnW1gonKtUY0RYD6H4wfVPitz46wDOzzbOlkNHvW0S4/htmlview?gid=269019846"

tab1, tab2, tab3 = st.tabs(["📝 Adaugă Cântărire", "👤 Clasament Individual", "👥 Clasament Echipe"])

with tab1:
    st.subheader("📋 Formular Introducere Date")
    st.components.v1.iframe(form_url, height=800, scrolling=True)

with tab2:
    st.subheader("👤 Clasament Individual Live")
    st.caption("Centralizat și ordonat automat după totalul de kilograme.")
    st.components.v1.iframe(sheet_clasament_url, height=700, scrolling=True)

with tab3:
    st.subheader("👥 Clasament Echipe Live")
    st.caption("Punctaj și greutate totală însumate per echipă.")
    st.components.v1.iframe(sheet_clasament_url, height=700, scrolling=True)
