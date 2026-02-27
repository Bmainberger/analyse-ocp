import streamlit as st
from datetime import date

# 1. Configuration de la page
st.set_page_config(page_title="OCP Patrimoine - Analyse", page_icon="🛡️", layout="wide")

st.title("🛡️ OCP Patrimoine - Bilan et Analyse")
st.markdown("---")

# 2. État Civil
st.header("1. État Civil & Situation Familiale")
col1, col2 = st.columns(2)
with col1:
    st.text_input("Nom du Client", key="nom_client")
    st.text_input("Prénom du Client", key="prenom_client")
    st.date_input("Date de naissance", value=date(1980, 1, 1), key="dnaiss_client")
with col2:
    st.selectbox("Situation Matrimoniale", ["Célibataire", "Marié(e)", "Pacsé(e)", "Divorcé(e)", "Veuf/Veuve"], key="situation")
    nb_enfants = st.number_input("Nombre d'enfants à charge", min_value=0, max_value=15, step=1, key="nb_enfants")

# 3. Patrimoine Financier (Vos 5 familles)
st.markdown("---")
st.header("6. Patrimoine Financier")

familles_actifs = {
    "Liquidités & Disponibilités": ["Compte Courant", "Livret A", "LDDS", "LEP", "Compte à terme"],
    "Épargne Logement": ["PEL", "CEL"],
    "Enveloppes de Capitalisation": ["Assurance-Vie", "Contrat de Capitalisation", "PEA", "PEA-PME", "Compte-Titres"],
    "Épargne Retraite": ["PER Individuel", "PER Collectif", "PER Assurance"],
    "Actifs Numériques": ["Crypto-actifs (Bitcoin, ETH...)", "Stablecoins"]
}

nb_fin = st.number_input("Nombre de comptes ou contrats financiers", min_value=0, step=1, key="nb_fin_total")
total_fin = 0.0

for k in range(int(nb_fin)):
    with st.expander(f"Contrat n°{k+1}", expanded=True):
        col_f1, col_f2, col_f3 = st.columns(3)
        with col_f1:
            famille_choisie = st.selectbox("Famille d'actif", list(familles_actifs.keys()), key=f"fam_f_{k}")
            st.text_input("Établissement", key=f"etab_f_{k}")
        with col_f2:
            type_precis = st.selectbox("Type de contrat", familles_actifs[famille_choisie], key=f"type_f_{k}")
            solde = st.number_input("Solde / Valeur actuelle (€)", min_value=0.0, key=f"solde_f_{k}")
            total_fin += solde
        with col_f3:
            st.selectbox("Mode de gestion", ["Gestion Libre", "Gestion Pilotée", "Gestion Sous Mandat"], key=f"gest_f_{k}")

if total_fin > 0:
    st.metric("Total Épargne Financière", f"{total_fin:,.0f} €".replace(",", " "))

st.markdown("---")
st.success("Analyse prête !")
