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
    lieu_naissance = st.text_input("Lieu de naissance")
    nationalite = st.text_input("Nationalité", value="Française")

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
    ville = st.text_input("Ville")
    cp = st.text_input("Code Postal")
    residence_statut = st.radio("Statut résidence", ["Propriétaire", "Locataire", "Logé par l'employeur"])

with col4:
    st.subheader("💼 Situation Professionnelle")
    profession = st.text_input("Profession")
    statut_pro = st.selectbox("Statut professionnel", ["Salarié", "TNS (Indépendant)", "Fonctionnaire", "Retraité", "Sans emploi"])
    revenu_annuel = st.number_input("Revenu Annuel Net (€)", min_value=0, step=1000)

st.markdown("---")

# --- SECTION 3 : PATRIMOINE IMMOBILIER ---
st.header("3. Patrimoine Immobilier")

# Utilisation d'un expander pour chaque bien (plus propre)
nb_biens = st.number_input("Combien de biens immobiliers possédez-vous ?", min_value=0, max_value=10, step=1)

for i in range(nb_biens):
    with st.expander(f"Détails du Bien Immobilier n°{i+1}", expanded=True):
        c1, c2, c3 = st.columns(3)
        with c1:
            type_bien = st.selectbox(f"Type de bien {i+1}", ["Résidence Principale", "Résidence Secondaire", "Locatif", "Terrain", "SCPI"], key=f"type_{i}")
            valeur = st.number_input(f"Valeur vénale (€) {i+1}", min_value=0, step=10000, key=f"valeur_{i}")
        with c2:
            proprio = st.text_input(f"Propriétaire (Client, Conjoint...)", key=f"proprio_{i}")
            loyers = st.number_input(f"Revenus locatifs annuels (€)", min_value=0, step=100, key=f"loyer_{i}")
        with c3:
            credit = st.radio(f"Crédit en cours ?", ["Non", "Oui"], key=f"credit_check_{i}")
            if credit == "Oui":
                mensualite = st.number_input(f"Mensualité (€)", min_value=0, key=f"mens_{i}")
                fin_credit = st.number_input(f"Année de fin", min_value=2024, max_value=2060, key=f"fin_{i}")

st.markdown("---")
st.success("Sections 1, 2 et 3 prêtes ! On continue ?")
