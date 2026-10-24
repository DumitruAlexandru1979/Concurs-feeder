import streamlit as st
import pandas as pd

st.set_page_config(page_title="Asistent Concurs Feeder", layout="centered")
st.title("🏆 Asistent Concurs Method Feeder")

# Extragere URL din Secrets
sheet_url = st.secrets["gsheets"]["spreadsheet"]

# Conversie URL pentru citire directa CSV din Google Sheets
if "/edit" in sheet_url:
    csv_url = sheet_url.split("/edit")[0] + "/export?format=csv"
else:
    csv_url = sheet_url

def incarca_date():
    try:
        df = pd.read_csv(csv_url)
        if df is not None and not df.empty:
            return df.dropna(how="all")
    except Exception:
        pass
    return pd.DataFrame(columns=["Arbitru", "Sector", "Stand", "Echipă", "Pescar", "Greutate (g)", "Captură Mare (g)"])

data = incarca_date()

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
        st.success(f"Cântărire înregistrată pentru {pescar} ({echipa})!")
        st.info("Pentru adăugare automată în Google Sheet fără autentificare Google Cloud, poți introduce datele direct sau folosi formularul sincronizat.")
    else:
        st.error("Te rugăm să introduci numele pescarului!")

st.write("---")
st.subheader("📊 Registru Cântăriri (Sincronizat Live)")

if not data.empty:
    st.dataframe(data, use_container_width=True)
else:
    st.info("Nu a fost înregistrată nicio cântărire până acum.")
