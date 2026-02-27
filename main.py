import streamlit as st

st.set_page_config(page_title="Analyse OCP", layout="wide")

st.title("🛡️ Analyse OCP - Audit Patrimonial")

# Création des onglets
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📍 État Civil", 
    "🏢 Pierre-Papier", 
    "🏠 Immobilier Physique",
    "💰 Financier",
    "🎯 Objectifs"
])

# --- SECTION 1 : ÉTAT CIVIL (RESTAURÉE) ---
with tab1:
    st.header("Informations Personnelles")
    c1, c2 = st.columns(2)
    with c1:
        st.text_input("Nom du Client", key="nom_c")
        st.text_input("Prénom", key="prenom_c")
        st.date_input("Date de naissance", key="dnais_c")
        st.text_input("Lieu de naissance", key="lieu_c")
        st.text_input("Nationalité", key="nat_c")
    with c2:
        situation = st.selectbox("Situation Familiale", ["Célibataire", "Marié(e)", "Pacsé(e)", "Divorcé(e)", "Veuf(ve)"], key="sit_fam")
        if situation in ["Marié(e)", "Pacsé(e)"]:
            st.selectbox("Régime matrimonial", ["Communauté réduite aux acquêts", "Séparation de biens", "Participation aux acquêts", "Communauté universelle"], key="regime")
            st.subheader("Informations Conjoint")
            st.text_input("Nom du Conjoint", key="nom_conj")
            st.date_input("Date de naissance conjoint", key="dnais_conj")

    st.divider()
    st.subheader("Enfants")
    nb_enfants = st.number_input("Nombre d'enfants", min_value=0, step=1)
    for i in range(int(nb_enfants)):
        col_e1, col_e2 = st.columns(2)
        with col_e1:
            st.text_input(f"Prénom Enfant {i+1}", key=f"enf_prenom_{i}")
        with col_e2:
            st.date_input(f"Date de naissance Enfant {i+1}", key=f"enf_dnais_{i}")

    st.divider()
    st.subheader("Revenus & Fiscalité")
    c3, c4 = st.columns(2)
    with c3:
        st.number_input("Revenus professionnels annuels (€)", min_value=0, key="rev_pro")
    with c4:
        st.selectbox("Tranche Marginale d'Imposition (TMI)", ["0%", "11%", "30%", "41%", "45%"], key="tmi")

# --- SECTION 2 : PIERRE-PAPIER (MISE À JOUR) ---
with tab2:
    st.header("Placements Collectifs")
    nb_coll = st.number_input("Nombre de placements collectifs", min_value=0, step=1)
    
    for j in range(int(nb_coll)):
        with st.expander(f"Placement n°{j+1}", expanded=True):
            t_coll = st.selectbox("Type de support", ["SCPI", "SCI", "OPCI", "GFV", "GFI", "Club Deal"], key=f"type_c_{j}")
            
            # Sous-types dynamiques
            if t_coll == "SCPI":
                st.selectbox("Sous-type SCPI", ["Rendement", "Fiscale", "Plus-value", "Européenne", "Thématique"], key=f"st_scpi_{j}")
            elif t_coll == "GFV":
                st.selectbox("Sous-type GFV", ["Viticole", "Agricole"], key=f"st_gfv_{j}")
            elif t_coll == "GFI":
                st.selectbox("Sous-type GFI", ["Forestier", "Chasse"], key=f"st_gfi_{j}")
            elif t_coll == "SCI":
                st.selectbox("Sous-type SCI", ["Patrimoniale", "Fiscale", "Variable", "Fixe"], key=f"st_sci_{j}")

            st.markdown("---")
            col_a, col_b = st.columns(2)
            with col_a:
                st.text_input("Nom du support", key=f"nom_c_{j}")
                st.selectbox("Mode de détention", ["Pleine Propriété", "Nue-Propriété", "Usufruit", "Via Assurance-Vie", "Via PER"], key=f"det_c_{j}")
            with col_b:
                val_estim = st.number_input("Valeur estimée (€)", min_value=0, key=f"liq_c_{j}")
                rev_annuel = st.number_input("Revenus annuels nets (€)", min_value=0, key=f"rev_c_{j}")
                if val_estim > 0:
                    st.info(f"📈 Rendement : {(rev_annuel / val_estim) * 100:.2f} %")

# --- SECTION 3 : IMMOBILIER PHYSIQUE (RESTAURÉE) ---
with tab3:
    st.header("Patrimoine Immobilier")
    st.write("Détaillez ici vos résidences et investissements locatifs.")
    # On garde la structure pour que tu puisses la remplir
    nb_immo = st.number_input("Nombre de biens immobiliers", min_value=0, step=1)

# --- SECTION 4 : FINANCIER (RESTAURÉE) ---
with tab4:
    st.header("Actifs Financiers")
    st.write("Comptes bancaires, Assurance-vie, PEA...")
    # On garde la structure

# --- SECTION 5 : OBJECTIFS (RESTAURÉE) ---
with tab5:
    st.header("Objectifs Patrimoniaux")
    st.checkbox("Préparer la retraite")
    st.checkbox("Optimiser la fiscalité")
    st.checkbox("Transmettre un patrimoine")
    st.checkbox("Protéger le conjoint")
