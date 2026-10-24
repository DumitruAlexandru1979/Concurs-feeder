import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="Asistent Concurs Feeder", layout="centered")
st.title("🏆 Asistent Concurs Method Feeder")

# Conexiune la Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

st.sidebar.header("📋 Panou Arbitru")
arbitru = st.sidebar.text_input("Nume Arbitru", "Arbitru 1")
sector = st.sidebar.selectbox("Sector", ["Sector A", "Sector B", "Sector C", "Sector D"])

st.header(f"Cântărire - {sector}")

with st.form("form_cantarire", clear_on_submit=True):
    echipa = st.text_input("Nume Echipă / Club")
    pescar = st.text_input("Nume Pescar")
    stand = st.number_input("Număr Stand", min_value=1, max_value=100, step=1)
    greutate = st.number_input("Greutate Totală (grame)", min_value=0, step=10)
    captura_mare = st.number_input("Cea mai mare captură (grame)", min_value=0, step=10)
    
    salveaza = st.form_submit_button("💾 Salvează Datele")

if salveaza:
    if pescar.strip() != "":
        try:
            # Citim datele existente din Google Sheets
            existing_data = conn.read(ttl=0)
            existing_data = existing_data.dropna(how="all")
        except Exception:
            existing_data = pd.DataFrame()

        new_entry = pd.DataFrame([{
            "Arbitru": arbitru,
            "Sector": sector,
            "Stand": stand,
            "Echipă": echipa,
            "Pescar": pescar,
            "Greutate (g)": greutate,
            "Captură Mare (g)": captura_mare
        }])

        updated_df = pd.concat([existing_data, new_entry], ignore_index=True)
        
        # Salvam inapoi in Google Sheets
        conn.update(data=updated_df)
        st.success(f"Date salvate cu succes în Google Sheets pentru {pescar} ({echipa})!")
        st.cache_data.clear()
    else:
        st.error("Te rugăm să introduci numele pescarului!")

st.write("---")
st.subheader("📊 Registru Cântăriri (Live din Google Sheets)")

try:
    df_live = conn.read(ttl=0).dropna(how="all")
    if not df_live.empty:
        st.dataframe(df_live, use_container_width=True)
    else:
        st.info("Nu a fost înregistrată nicio cântărire până acum.")
except Exception:
    st.info("Tabelul este gol sau se încarcă datele...")
