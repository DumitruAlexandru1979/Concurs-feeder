import streamlit as st
import pandas as pd

st.set_page_config(page_title="Concurs Feeder Live", page_icon="🏆", layout="centered")

st.title("🏆 Concurs Method Feeder")

# Inițializare bază de date în memorie
if "weigh_data" not in st.session_state:
    st.session_state.weigh_data = []

# Adăugat Tab-ul 4: Modifică / Șterge
tab1, tab2, tab3, tab4 = st.tabs([
    "➕ Adaugă Cântărire", 
    "👤 Clasament Individual", 
    "👥 Clasament Echipe",
    "✏️ Modifică / Șterge"
])

# TAB 1: FORMULAR INTRODUCERE
with tab1:
    st.subheader("📋 Introducere Cântărire")
    
    with st.form("form_cantarire", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            sector = st.selectbox("Sector", ["Sector A", "Sector B", "Sector C", "Sector D"])
            stand = st.number_input("Număr Stand", min_value=1, max_value=100, step=1)
        with col2:
            angler = st.text_input("Nume Pescar")
            team = st.text_input("Nume Echipă / Club")
            
        weight = st.number_input("Greutate (kg)", min_value=0.0, step=0.05, format="%.2f")
        cmmc = st.number_input("CMMC / Captură Mare (kg)", min_value=0.0, step=0.05, format="%.2f")
        
        submitted = st.form_submit_button("💾 Salvează Cântărirea", use_container_width=True)
        
        if submitted:
            if angler.strip() == "":
                st.error("Te rugăm să introduci numele pescarului!")
            elif weight <= 0:
                st.error("Introdu o greutate mai mare de 0 kg!")
            else:
                st.session_state.weigh_data.append({
                    "Sector": sector,
                    "Stand": stand,
                    "Pescar": angler.strip(),
                    "Echipă": team.strip() if team.strip() else "Individual",
                    "Greutate": weight,
                    "CMMC": cmmc
                })
                st.success(f"✅ Cântărire salvată pentru {angler} ({weight} kg)!")
                st.rerun()

# Convertim datele în DataFrame
df = pd.DataFrame(st.session_state.weigh_data)

# TAB 2: CLASAMENT INDIVIDUAL
with tab2:
    st.subheader("👤 Clasament Individual Live")
    if not df.empty:
        ind_df = df.groupby(["Pescar", "Echipă", "Sector"]).agg(
            Total_Kg=("Greutate", "sum"),
            CMMC_Max=("CMMC", "max")
        ).reset_index()
        
        ind_df = ind_df.sort_values(by="Total_Kg", ascending=False).reset_index(drop=True)
        ind_df.index += 1
        ind_df.index.name = "Loc"
        
        st.dataframe(ind_df, use_container_width=True)
    else:
        st.info("Nu există nicio cântărire înregistrată încă.")

# TAB 3: CLASAMENT ECHIPE
with tab3:
    st.subheader("👥 Clasament Echipe Live")
    if not df.empty:
        team_df = df.groupby("Echipă").agg(
            Total_Kg=("Greutate", "sum"),
            CMMC_Max=("CMMC", "max"),
            Nr_Cantariri=("Greutate", "count")
        ).reset_index()
        
        team_df = team_df.sort_values(by="Total_Kg", ascending=False).reset_index(drop=True)
        team_df.index += 1
        team_df.index.name = "Loc"
        
        st.dataframe(team_df, use_container_width=True)
    else:
        st.info("Nu există date pentru clasamentul pe echipe.")

# TAB 4: MODIFICĂ SAU ȘTERGE DATE GREȘITE
with tab4:
    st.subheader("✏️ Editare Cântăriri Înregistrate")
    if not df.empty:
        st.caption("Modifică valorile direct în tabel sau selectează rânduri și apasă 'Delete' pe tastatură pentru a le șterge.")
        
        # Tabelul interactiv de editare
        edited_df = st.data_editor(
            df, 
            num_rows="dynamic", 
            use_container_width=True,
            key="editor_cantariri"
        )
        
        # Buton pentru salvarea modificărilor în memorie
        if st.button("💾 Salvează Modificările Corectate", type="primary", use_container_width=True):
            st.session_state.weigh_data = edited_df.to_dict(orient="records")
            st.success("✅ Datele au fost actualizate cu succes!")
            st.rerun()
    else:
        st.info("Nu există cântăriri de modificat.")

# OPȚIUNI SALVARE ȘI RESETARE CONCURS JOS
st.divider()

if not df.empty:
    csv_data = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Descarcă Istoric Concurs (CSV / Excel)",
        data=csv_data,
        file_name="rezultate_concurs.csv",
        mime="text/csv",
        use_container_width=True
    )

if st.button("🗑️ Resetare Concurs (Șterge Datele)", type="secondary", use_container_width=True):
    st.session_state.weigh_data = []
    st.rerun()
