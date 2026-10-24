import streamlit as st

st.set_page_config(
    page_title="Asistent Concurs Feeder", 
    page_icon="🏆",
    layout="centered"
)

st.title("🏆 Asistent Concurs Method Feeder")

# Buton de refresh rapid
if st.button("🔄 Actualizează Clasamentul / Pagina"):
    st.rerun()

# Link-uri Google Form si Google Sheets
form_url = "https://docs.google.com/forms/d/e/1FAIpQLSf67fr3GOWoGQ5-XDkKc924_nhzGZU4dg3bMQivtU5L8HNNng/viewform?embedded=true"
sheet_individual_url = "https://docs.google.com/spreadsheets/d/1tnW1gonKtUY0RYD6H4wfVPitz46wDOzzbOlkNHvW0S4/htmlview?gid=1874291500"
sheet_echipe_url = "https://docs.google.com/spreadsheets/d/1tnW1gonKtUY0RYD6H4wfVPitz46wDOzzbOlkNHvW0S4/htmlview?gid=1874291500"

tab1, tab2, tab3 = st.tabs(["📝 Adaugă Cântărire", "👤 Clasament Individual", "👥 Clasament Echipe"])

with tab1:
    st.subheader("📋 Formular Introducere Date")
    st.caption("Arbitrii introduc datele cântăririi mai jos. Apăsați 'Trimite' după fiecare cântărire.")
    st.components.v1.iframe(form_url, height=800, scrolling=True)

with tab2:
    st.subheader("👤 Clasament Individual Live")
    st.caption("Se actualizează automat pe măsură ce arbitrii salvează datele.")
    st.components.v1.iframe(sheet_individual_url, height=700, scrolling=True)

with tab3:
    st.subheader("👥 Clasament Echipe Live")
    st.caption("Punctajul și greutatea totală agregate per echipă/club.")
    st.components.v1.iframe(sheet_echipe_url, height=700, scrolling=True)
