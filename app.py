import streamlit as st
import pandas as pd
import gspread

st.set_page_config(page_title="Asistent Concurs Feeder", layout="centered")
st.title("🏆 Asistent Concurs Method Feeder")

# Conectare nativa la Google Sheets folosind URL-ul din Secrets
@st.cache_resource
def get_gsheet_client():
    return gspread.public_spreadsheet(st.secrets["gsheets"]["spreadsheet"])

try:
    sheet = get_gsheet_client().sheet1
    raw_data = sheet.get_all_records()
    data = pd.DataFrame(raw_data)
except Exception:
    data = pd.DataFrame(columns=["Arbitru", "Sector", "Stand", "Echipă", "Pescar", "Greutate (g)", "Captură Mare (g)"])

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
        # Adaugare rand direct in Google Sheet
        rand_nou = [arbitru, sector, int(stand), echipa, pescar, int(greutate), int(captura_mare)]
        sheet.append_row(rand_nou)
        
        st.success(f"Date salvate cu succes pentru {pescar} ({echipa})!")
        st.rerun()
    else:
        st.error("Te rugăm să introduci numele pescarului!")

st.write("---")
st.subheader("📊 Registru Cântăriri (Sincronizat Live)")

if not data.empty:
    st.dataframe(data, use_container_width=True)
else:
    st.info("Nu a fost înregistrată nicio cântărire până acum.")
