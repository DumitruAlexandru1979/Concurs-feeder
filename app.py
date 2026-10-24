import streamlit as st

st.set_page_config(page_title="Asistent Concurs Feeder", layout="centered")
st.title("🏆 Asistent Concurs Method Feeder")

# Link-uri Google Form si Google Sheets pentru fiecare foaie
form_url = "https://docs.google.com/forms/d/e/1FAIpQLSf67fr3GOWoGQ5-XDkKc924_nhzGZU4dg3bMQivtU5L8HNNng/viewform?embedded=true"

# Link-uri catre foile individuale si echipe
sheet_individual_url = "https://docs.google.com/spreadsheets/d/1tnW1gonKtUY0RYD6H4wfVPitz46wDOzzbOlkNHvW0S4/htmlview?gid=1874291500"
sheet_echipe_url = "https://docs.google.com/spreadsheets/d/1tnW1gonKtUY0RYD6H4wfVPitz46wDOzzbOlkNHvW0S4/htmlview?gid=1874291500"

tab1, tab2, tab3 = st.tabs(["📝 Adaugă Cântărire", "👤 Clasament Individual", "👥 Clasament Echipe"])

with tab1:
    st.subheader("📋 Formular Introducere Date")
    st.components.v1.iframe(form_url, height=850, scrolling=True)

with tab2:
    st.subheader("👤 Clasament Individual Live")
    st.components.v1.iframe(sheet_individual_url, height=700, scrolling=True)

with tab3:
    st.subheader("👥 Clasament Echipe Live")
    st.components.v1.iframe(sheet_echipe_url, height=700, scrolling=True)
