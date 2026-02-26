import streamlit as st
from datetime import date

# Configuration de la page
st.set_page_config(page_title="OCP Patrimoine - Analyse", page_icon="🛡️", layout="wide")

# Titre principal
st.title("🛡️ OCP Patrimoine - Bilan et Analyse")
st.markdown("---")

# --- SECTION 1 : ÉTAT CIVIL ---
st.header("1. État Civil & Situation Familiale")
col1, col2 = st.columns(2)
with col1:
    st.subheader("Informations Personnelles")
    nom_client = st.text_input("Nom du Client")
    prenom_client = st.text_input("Prénom du Client")
    date_naissance = st.date_input("Date de naissance", value=date(1980, 1, 1))
with col2:
    st.subheader("Situation Familiale")
    situation = st.selectbox("Situation Matrimoniale", ["Célibataire", "Marié(e)", "Pacsé(e)", "Divorcé(e)", "Veuf/Veuve"])
    nb_enfants = st.number_input("Nombre d'enfants à charge", min_value=0, max_value=15, step=1)
    if nb_enfants > 0:
        cols_ages = st.columns(nb_enfants)
        for i in range(nb_enfants):
            with cols_ages[i]:
                st.number_input(f"Âge Enfant {i+1}", min_value=0, max_value=30, key=f"age_{i}")

st.markdown("---")

# --- SECTION 2 : ADRESSE & PRO ---
st.header("2. Coordonnées et Situation Professionnelle")
col3, col4 = st.columns(2)
with col3:
    st.subheader("📍 Adresse")
    adresse = st.text_input("Adresse complète")
    residence_statut = st.radio("Statut résidence", ["Propriétaire", "Locataire", "Logé par l'employeur"])
with col4:
    st.subheader("💼 Situation Professionnelle")
    statut_pro = st.selectbox("Statut professionnel", ["Salarié", "TNS", "Fonctionnaire", "Retraité"])
    revenu_annuel = st.number_input("Revenu Annuel Net (€)", min_value=0, step=1000)

st.markdown("---")

# --- SECTION 3 : PATRIMOINE IMMOBILIER (PHYSIQUE) ---
st.header("3. Patrimoine Immobilier (Physique)")
nb_biens = st.number_input("Nombre de biens immobiliers", min_value=0, max_value=10, step=1)
for i in range(nb_biens):
    with st.expander(f"Bien Immobilier n°{i+1}", expanded=False):
        c1, c2 = st.columns(2)
        with c1:
            st.selectbox(f"Type de bien {i+1}", ["Résidence Principale", "Résidence Secondaire", "Locatif"], key=f"type_{i}")
            st.number_input(f"Valeur vénale (€) {i+1}", min_value=0, key=f"val_i_{i}")
        with c2:
            st.radio(f"Crédit en cours ? {i+1}", ["Non", "Oui"], key=f"cred_i_{i}")

st.markdown("---")

# --- SECTION 4 : IMMOBILIER COLLECTIF (PIERRE-PAPIER) ---
st.header("4. Patrimoine Immobilier Collectif")
st.info("SCPI, SCI, OPCI, GFV, GFI, Club Deal...")

nb_coll = st.number_input("Nombre de placements collectifs", min_value=0, max_value=20, step=1)

for j in range(nb_coll):
    with st.expander(f"Placement Collectif n°{j+1}", expanded=True):
        t1, t2, t3 = st.columns(3)
        
        with t1:
            type_coll = st.selectbox(
                f"Type de placement {j+1}", 
                ["SCPI", "SCI", "OPCI", "GFV (Viticole)", "GFI/GFF (Forêt)", "Club Deal", "Crowdfunding"],
                key=f"type_c_{j}"
            )
            nom_support = st.text_input(f"Nom du support / Société de gestion", key=f"nom_c_{j}")
            
        with t2:
            mode_detention = st.selectbox(
                f"Mode de détention {j+1}",
                ["Pleine Propriété", "Nue-Propriété", "Usufruit", "Via Assurance-Vie / PER"],
                key=f"detent_c_{j}"
            )
            valeur_actuelle = st.number_input(f"Valeur actuelle (€) {j+1}", min_value=0, key=f"val_c_{j}")

        with t3:
            revenus_c = st.number_input(f"Revenus annuels perçus (€) {j+1}", min_value=0, key=f"rev_c_{j}")
            # Logique spécifique selon le type
            if type_coll == "SCPI":
                nb_parts = st.number_input(f"Nombre de parts", min_value=0, key=f"parts_c_{j}")
            elif type_coll in ["GFI/GFF (Forêt)", "GFV (Viticole)"]:
                st.write("🌿 *Avantage fiscal forestier/agricole applicable*")

st.markdown("---")
st.success("Sections 1 à 4 opérationnelles. En attente du Patrimoine Financier (Section 5).")
