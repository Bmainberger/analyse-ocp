import streamlit as st

# Configuration de la page
st.set_page_config(page_title="Analyse OCP", layout="wide")

st.title("🛡️ Analyse OCP - Audit Patrimonial")

# INITIALISATION DES ONGLETS (C'est ce qui manquait !)
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📍 État Civil", 
    "🏢 Pierre-Papier", 
    "🏠 Immobilier Physique",
    "💰 Financier",
    "🎯 Objectifs"
])

# --- SECTION 1 : ÉTAT CIVIL ---
with tab1:
    st.header("Informations Client")
    c1, c2 = st.columns(2)
    with c1:
        st.text_input("Nom du Client", key="nom_client")
        st.number_input("Âge", min_value=0, max_value=120, key="age_client")
    with c2:
        st.selectbox("Situation Familiale", ["Célibataire", "Marié(e)", "Pacsé(e)", "Divorcé(e)"], key="sit_fam")
        st.number_input("Nombre d'enfants", min_value=0, key="nb_enfants")

# --- SECTION 2 : PIERRE-PAPIER ---
with tab2:
    st.header("Placements Collectifs (SCPI, SCI, GFV...)")
    nb_coll = st.number_input("Nombre de placements collectifs", min_value=0, step=1)
    
    for j in range(int(nb_coll)):
        with st.expander(f"Placement Collectif n°{j+1}", expanded=True):
            t_coll = st.selectbox(f"Type de support", ["SCPI", "SCI", "OPCI", "GFV", "GFI", "Club Deal"], key=f"type_c_{j}")
            
            if t_coll == "SCPI":
                st.selectbox("Sous-type SCPI", ["Rendement", "Fiscale", "Plus-value", "Européenne", "Thématique"], key=f"st_scpi_{j}")
            elif t_coll == "GFV":
                st.selectbox("Sous-type GFV", ["Viticole", "Agricole"], key=f"st_gfv_{j}")
            elif t_coll == "GFI":
                st.selectbox("Sous-type GFI", ["Forestier", "Chasse"], key=f"st_gfi_{j}")

            st.markdown("---")
            col_a, col_b = st.columns(2)
            with col_a:
                st.text_input("Nom du support", key=f"nom_c_{j}")
                st.selectbox("Mode de détention", ["Pleine Propriété", "Nue-Propriété", "Usufruit", "Via Assurance-Vie", "Via PER"], key=f"det_c_{j}")
            with col_b:
                val_estim = st.number_input("Valeur actuelle estimée (€)", min_value=0, key=f"liq_c_{j}")
                rev_annuel = st.number_input("Revenus annuels nets (€)", min_value=0, key=f"rev_c_{j}")
                if val_estim > 0:
                    st.info(f"📈 Rendement : {(rev_annuel / val_estim) * 100:.2f} %")

# --- SECTIONS VIDES POUR EVITER LES ERREURS ---
with tab3: st.write("En construction...")
with tab4: st.write("En construction...")
with tab5: st.write("En construction...")
