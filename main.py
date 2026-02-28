import streamlit as st
from datetime import date

st.set_page_config(page_title="OCP Patrimoine - Bilan Complet", layout="wide")
st.title("🛡️ OCP Patrimoine - Bilan Global")

# --- 1. ÉTAT CIVIL (CLIENT & CONJOINT) ---
st.header("1. État Civil & Situation Familiale")
col1, col2 = st.columns(2)
with col1:
    st.subheader("Le Client")
    st.text_input("Nom", key="nom_c")
    st.text_input("Prénom", key="prenom_c")
    st.date_input("Date de naissance", value=date(1980, 1, 1), key="dnaiss_c")
    st.text_input("Nationalité", key="nat_c")
    st.text_input("Lieu de naissance", key="lieu_c")

with col2:
    st.subheader("Situation")
    situation = st.selectbox("Situation Matrimoniale", ["Célibataire", "Marié(e)", "Pacsé(e)", "Divorcé(e)", "Veuf/Veuve"])
    nb_enfants = st.number_input("Nombre d'enfants", min_value=0, step=1)

if situation in ["Marié(e)", "Pacsé(e)"]:
    st.markdown("---")
    st.subheader("Informations du Conjoint")
    c1, c2 = st.columns(2)
    with c1:
        st.text_input("Nom du Conjoint", key="nom_conj")
        st.text_input("Prénom du Conjoint", key="pre_conj")
    with c2:
        st.date_input("Date de naissance conjoint", value=date(1980, 1, 1), key="dnaiss_conj")
        st.text_input("Nationalité Conjoint", key="nat_conj")
        st.text_input("Lieu de naissance Conjoint", key="lieu_conj")

if nb_enfants > 0:
    st.subheader("Détails des Enfants")
    cols_enf = st.columns(3)
    for i in range(int(nb_enfants)):
        cols_enf[i % 3].date_input(f"Date de naissance Enfant n°{i+1}", key=f"enf_d_{i}")

# --- 4 & 5. PATRIMOINE IMMOBILIER (2 BRANCHES) ---
st.markdown("---")
st.header("4 & 5. Patrimoine Immobilier")
col_immo1, col_immo2 = st.columns(2)
with col_immo1:
    st.subheader("🏠 Branche A : Immobilier Physique")
    nb_phys = st.number_input("Nombre de biens physiques", min_value=0, step=1, key="nb_p")
    for p in range(int(nb_phys)):
        with st.expander(f"Bien n°{p+1}"):
            st.selectbox("Usage", ["Résidence Principale", "Résidence Secondaire", "Locatif"], key=f"u_p_{p}")
            st.number_input("Valeur estimée (€)", min_value=0, key=f"v_p_{p}")
with col_immo2:
    st.subheader("📄 Branche B : Pierre Papier")
    nb_pap = st.number_input("Nombre de placements (SCPI, etc.)", min_value=0, step=1, key="nb_pap")
    for i in range(int(nb_pap)):
        with st.expander(f"Produit n°{i+1}"):
            st.selectbox("Type", ["SCPI", "OPCI", "GVF (Forêt)", "GVA (Vignes)", "SCI", "SC"], key=f"t_pap_{i}")
            st.text_input("Nom du support", key=f"n_pap_{i}")
            st.number_input("Valeur actuelle (€)", min_value=0, key=f"v_pap_{i}")

# --- 6. PATRIMOINE FINANCIER ---
st.markdown("---")
st.header("6. Patrimoine Financier")
nb_fin = st.number_input("Nombre de comptes financiers", min_value=0, step=1)
for f in range(int(nb_fin)):
    with st.expander(f"Contrat n°{f+1}"):
        st.selectbox("Catégorie", ["Liquidités", "Épargne Logement", "Assurance-Vie", "PEA", "Retraite", "Cryptos"], key=f"cat_f_{f}")
        st.number_input("Solde (€)", key=f"s_f_{f}")

# --- 7 & 8. SANTÉ & PRÉVOYANCE ---
st.markdown("---")
st.header("7 & 8. Santé & Prévoyance")
col_s1, col_s2 = st.columns(2)
with col_s1:
    st.subheader("🛡️ Santé")
    st.selectbox("Contrat", ["Individuel", "Collectif"], key="sante_type")
    st.text_input("Organisme", key="sante_org")
with col_s2:
    st.subheader("📑 Prévoyance")
    st.multiselect("Garanties", ["Décès", "Invalidité", "IJ", "Rente Éducation"], key="prev_gar")

st.success("Structure complète validée !")
