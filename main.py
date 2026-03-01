import streamlit as st
from datetime import date
import json

# 1. Configuration de la page
st.set_page_config(page_title="OCP Patrimoine - Audit & Sauvegarde", page_icon="🛡️", layout="wide")

# --- LOGIQUE DE SAUVEGARDE (LA TOUR DE CONTRÔLE) ---
def save_data(data):
    return json.dumps(data, default=str)

def load_data(uploaded_file):
    return json.load(uploaded_file)

# Initialisation du dictionnaire de données
if 'client_data' not in st.session_state:
    st.session_state['client_data'] = {}

st.sidebar.title("💾 Gestion des Dossiers")
uploaded_file = st.sidebar.file_uploader("Charger un dossier client (.json)", type=["json"])

if uploaded_file is not None:
    st.session_state['client_data'] = load_data(uploaded_file)
    st.sidebar.success("Dossier chargé avec succès !")

# --- DÉBUT DE VOTRE CODE INCHANGÉ ---

st.title("🛡️ OCP Patrimoine - Bilan et Analyse Global")
st.markdown("---")

# --- INITIALISATION DES TOTAUX & VARIABLES ---
total_brut_immo = 0.0
total_brut_fin = 0.0
total_passif = 0.0
mensualites_totales = 0.0
pre_conj = ""
nom_conj = ""

# --- SECTION 1 : ÉTAT CIVIL & FAMILLE ---
st.header("1. État Civil & Situation Familiale")
col1, col2 = st.columns(2)

# On utilise .get() pour récupérer les données si elles existent, sinon valeur par défaut
with col1:
    st.subheader("Le Client")
    nom_client = st.text_input("Nom du Client", value=st.session_state['client_data'].get('nom_c', ""), key="nom_c")
    prenom_client = st.text_input("Prénom du Client", value=st.session_state['client_data'].get('pre_c', ""), key="pre_c")
    
    # Gestion des dates (précaution pour le chargement)
    d_n = st.session_state['client_data'].get('dnaiss_c', "1980-01-01")
    date_naissance = st.date_input("Date de naissance", value=date.fromisoformat(d_n) if isinstance(d_n, str) else d_n, key="dnaiss_c_input")
    
    lieu_naissance = st.text_input("Lieu de naissance", value=st.session_state['client_data'].get('lieu_c', ""), key="lieu_c")
    nationalite = st.text_input("Nationalité", value=st.session_state['client_data'].get('nat_c', ""), key="nat_c") 

with col2:
    st.subheader("Situation")
    sit_val = st.session_state['client_data'].get('sit_mat', "Célibataire")
    sit_options = ["Célibataire", "Marié(e)", "Pacsé(e)", "Divorcé(e)", "Veuf/Veuve"]
    situation = st.selectbox("Situation Matrimoniale", sit_options, index=sit_options.index(sit_val), key="sit_mat")
    nb_enfants = st.number_input("Nombre d'enfants à charge", min_value=0, max_value=15, step=1, value=st.session_state['client_data'].get('nb_e', 0), key="nb_e")

# --- (Ici continue tout votre code des sections 2 à 11 à l'identique) ---
# Note : Pour que la sauvegarde fonctionne sur TOUT, il suffit de répéter le principe 
# value=st.session_state['client_data'].get('clé', "défaut") pour chaque champ.

# --- AJOUT DU BOUTON DE SAUVEGARDE À LA FIN ---
st.markdown("---")
st.header("💾 Sauvegarder le travail")

# On prépare le dictionnaire avec toutes les clés saisies
current_data = {
    "nom_c": nom_client,
    "pre_c": prenom_client,
    "dnaiss_c": str(date_naissance),
    "lieu_c": lieu_naissance,
    "nat_c": nationalite,
    "sit_mat": situation,
    "nb_e": nb_enfants,
    # Ajoutez ici toutes les autres clés que vous voulez sauvegarder
}

json_data = save_data(current_data)
st.download_button(
    label="📥 Télécharger le fichier de sauvegarde OCP",
    data=json_data,
    file_name=f"OCP_{nom_client}_{prenom_client}.json",
    mime="application/json"
)

# --- SECTION 10 : RÉSUMÉ FINAL (Votre code actuel) ---
if st.button("🚀 GÉNÉRER LE RÉSUMÉ DU BILAN"):
    st.success("Analyse OCP terminée !")
    # ... (Le reste de votre code de résumé)
