import streamlit as st

st.set_page_config(page_title="Asistent Concurs Feeder", layout="centered")
st.title("🏆 Asistent Concurs Method Feeder")

# Link-uri Google Form si Google Sheet (specificat pe tab-ul cu raspunsuri)
form_url = "https://docs.google.com/forms/d/e/1FAIpQLSf67fr3GOWoGQ5-XDkKc924_nhzGZU4dg3bMQivtU5L8HNNng/viewform?embedded=true"
sheet_url = "https://docs.google.com/spreadsheets/d/1tnW1gonKtUY0RYD6H4wfVPitz46wDOzzbOlkNHvW0S4/htmlview?gid=2000651327"

tab1, tab2 = st.tabs(["📝 Introducere Cântărire", "📊 Tabel Live (Google Sheets)"])

with tab1:
    st.subheader("📋 Formular Introducere Date")
    st.components.v1.iframe(form_url, height=850, scrolling=True)

with tab2:
    st.subheader("📊 Registru Cântăriri (Sincronizat Live)")
    st.components.v1.iframe(sheet_url, height=700, scrolling=True)
