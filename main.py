import streamlit as st
from datetime import date

# Configuration de la page pour un affichage large et professionnel
st.set_page_config(page_title="OCP Patrimoine - Analyse", page_icon="🛡️", layout="wide")

# Titre principal avec le logo bouclier
st.title("🛡️ OCP Patrimoine - Bilan et Analyse")
st.markdown("---")

# --- SECTION 1 : ÉTAT CIVIL & IDENTITÉ ---
st.header("1. État Civil & Situation Familiale")

# Création de deux colonnes pour que le formulaire soit élégant
col1, col2 = st.columns(2)

with col1:
    st.subheader("Informations Personnelles")
    nom_client = st.text_input("Nom du Client")
    prenom_client = st.text_input("Prénom du Client")
    date_naissance = st.date_input(
        "Date de naissance", 
        value=date(1980, 1, 1),
        help="Cette donnée est essentielle pour calculer l'âge et les projections de retraite."
    )
    profession = st.text_input("Profession / Secteur d'activité")
    revenu_annuel = st.number_input("Revenu Annuel Net (€)", min_value=0, step=1000)

with col2:
    st.subheader("Situation Familiale")
    situation_matrimoniale = st.selectbox(
        "Situation Matrimoniale",
        ["Célibataire", "Marié(e)", "Pacsé(e)", "Divorcé(e)", "Veuf/Veuve"]
    )
    
    # Le champ "Régime" ne s'affiche que si le client est marié ou pacsé
    if situation_matrimoniale in ["Marié(e)", "Pacsé(e)"]:
        regime_matrimonial = st.selectbox(
            "Régime Matrimonial",
            ["Communauté réduite aux acquêts", "Séparation de biens", "Participation aux acquêts", "Communauté universelle"]
        )
    
    enfants_charge = st.number_input("Nombre d'enfants à charge", min_value=0, max_value=20, step=1)
    
    objectifs = st.multiselect(
        "Objectifs prioritaires du client",
        ["Préparer la retraite", "Réduire les impôts", "Transmettre un patrimoine", "Protéger le conjoint", "Créer des revenus"]
    )

# Barre de séparation
st.markdown("---")

# Bouton de validation visuel
if st.button("Valider la saisie de l'État Civil"):
    if nom_client and prenom_client:
        st.success(f"✅ Section validée pour {prenom_client} {nom_client}.")
    else:
        st.warning("Veuillez au moins saisir le nom et le prénom du client.")

# Note d'information pour la suite
st.info("💡 Note : Les sections suivantes (Patrimoine Immobilier, Placements, Passif) seront ajoutées lors de notre prochaine étape.")
