import streamlit as st
import pandas as pd

st.set_page_config(page_title="Asistent Concurs Feeder", layout="centered")
st.title("🏆 Asistent Concurs Method Feeder")

# Inserăm Google Sheet-ul tău direct integrat în aplicație pentru vizualizare live
sheet_url = "https://docs.google.com/spreadsheets/d/1tnW1gonKtUY0RYD6H4wfVPitz46wDOzzbOlkNHvW0S4/edit?usp=sharing"
embed_url = sheet_url.replace("/edit?usp=sharing", "/preview")

st.sidebar.header("📋 Panou Arbitru")
arbitru = st.sidebar.text_input("Nume Arbitru", "Arbitru 1")
sector = st.sidebar.selectbox("Sector", ["Sector A", "Sector B", "Sector C", "Sector D"])

tab1, tab2 = st.tabs(["📝 Introducere Cântărire", "📊 Tabel Live (Google Sheets)"])

with tab1:
    st.header(f"Cântărire - {sector}")
    
    with st.form("form_cantarire", clear_on_submit=True):
        echipa = st.text_input("Nume Echipă / Club")
        pescar = st.text_input("Nume Pescar")
        stand = st.number_input("Număr Stand", min_value=1, max_value=100, step=1)
        greutate = st.number_input("Greutate Totală (grame)", min_value=0, step=10)
        captura_mare = st.number_input("Cea mai mare captură (grame)", min_value=0, step=10)
        
        salveaza = st.form_submit_button("💾 Înregistrează Cântărirea")

    if salveaza:
        if pescar.strip() != "":
            # Se salvează în memoria locală a sesiunii pentru verificare rapidă
            if "cantariri" not in st.session_state:
                st.session_state.cantariri = []
            
            st.session_state.cantariri.append({
                "Arbitru": arbitru,
                "Sector": sector,
                "Stand": stand,
                "Echipă": echipa,
                "Pescar": pescar,
                "Greutate (g)": greutate,
                "Captură Mare (g)": captura_mare
            })
            st.success(f"Cântărire înregistrată local pentru {pescar}!")
        else:
            st.error("Te rugăm să introduci numele pescarului!")

    if "cantariri" in st.session_state and st.session_state.cantariri:
        st.subheader("Cântăriri adăugate pe acest telefon:")
        st.dataframe(pd.DataFrame(st.session_state.cantariri), use_container_width=True)

with tab2:
    st.subheader("📊 Tabel Centralizat Live")
    st.components.v1.iframe(embed_url, height=600, scrolling=True)
