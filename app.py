import streamlit as st
import pandas as pd

st.set_page_config(page_title="Asistent Concurs Feeder", layout="centered")
st.title("🏆 Asistent Concurs Method Feeder")

if 'cantariri' not in st.session_state:
    st.session_state['cantariri'] = []

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
        st.session_state['cantariri'].append({
            "Arbitru": arbitru,
            "Sector": sector,
            "Stand": stand,
            "Echipă": echipa,
            "Pescar": pescar,
            "Greutate (g)": greutate,
            "Captură Mare (g)": captura_mare
        })
        st.success(f"Date salvate cu succes pentru {pescar} ({echipa})!")
    else:
        st.error("Te rugăm să introduci numele pescarului!")

st.write("---")
st.subheader("📊 Registru Cântăriri")

if st.session_state['cantariri']:
    df = pd.DataFrame(st.session_state['cantariri'])
    st.dataframe(df, use_container_width=True)
else:
    st.info("Nu a fost înregistrată nicio cântărire până acum.")
