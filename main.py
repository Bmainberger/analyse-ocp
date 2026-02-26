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
    profession = st.text_input("Profession")
    revenu_annuel = st.number_input("Revenu Annuel Net (€)", min_value=0, step=1000)

with col2:
    st.subheader("Situation Familiale")
    situation = st.selectbox("Situation Matrimoniale", ["Célibataire", "Marié(e)", "Pacsé(e)", "Divorcé(e)", "Veuf/Veuve"])
    
    # Dynamique : Nombre d'enfants et leurs âges
    nb_enfants = st.number_input("Nombre d'enfants à charge", min_value=0, max_value=15, step=1)
    
    if nb_enfants > 0:
        st.write("Âge des enfants :")
        cols_ages = st.columns(nb_enfants)
        for i in range(nb_enfants):
            with cols_ages[i]:
                st.number_input(f"Enfant {i+1}", min_value=0, max_value=30, key=f"age_{i}")

st.markdown("---")
st.info("💡 Prochaine étape : Patrimoine Immobilier. Envoie-moi tes éléments Copilot !")
