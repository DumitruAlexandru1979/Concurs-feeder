import streamlit as st
import pandas as pd

# Titlu aplicatie
st.set_page_config(page_title="Asistent Concurs Feeder", layout="centered")
st.title("🏆 Concurs Feeder - Introducere Date")

# Initializare baza de date locala in sesiune
if 'cantariri' not in st.session_state:
    st.session_state['cantariri'] = []

st.sidebar.header("📋 Panou Arbitru")
arbitru = st.sidebar.text_input("Nume Arbitru", "Arbitru 1")
sector = st.sidebar.selectbox("Sector", ["Sector A", "Sector B", "Sector C", "Sector D"])

st.header(f"Cântărire - {sector}")

with st.form("form_cantarire", clear_on_submit=True):
    stand = st.number_input("Număr Stand / Pescar", min_value=1, max_value=100, step=1)
    nume_pescar = st.text_input("Nume Pescar")
    greutate = st.number_input("Greutate (grame)", min_value=0, step=50)
    peste_mare = st.number_input("Cel mai mare pește (grame - opțional)", min_value=0, step=50)
    
    salveaza = st.form_submit_button("💾 Salvează Cântărirea")

if salveaza:
    if nume_pescar.strip() != "":
        st.session_state['cantariri'].append({
            "Arbitru": arbitru,
            "Sector": sector,
            "Stand": stand,
            "Pescar": nume_pescar,
            "Greutate (g)": greutate,
            "Pește Mare (g)": peste_mare
        })
        st.success(f"Cântărire salvată pentru {nume_pescar} (Stand {stand})!")
    else:
        st.error("Te rugăm să introduci numele pescarului!")

# Afisare Clasament / Date introduse
st.write("---")
st.subheader("📊 Date Introduse")

if st.session_state['cantariri']:
    df = pd.DataFrame(st.session_state['cantariri'])
    st.dataframe(df, use_container_width=True)
else:
    st.info("Nu a fost introdusă nicio cântărire încă.")
