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

# --- SECTION 4 : IMMOBILIER COLLECTIF ---
st.header("4. Patrimoine Immobilier Collectif")
nb_coll = st.number_input("Nombre de placements collectifs (SCPI, GFI...)", min_value=0, max_value=20, step=1)
for j in range(nb_coll):
    with st.expander(f"Placement Collectif n°{j+1}", expanded=False):
        t1, t2 = st.columns(2)
        with t1:
            st.selectbox(f"Type {j+1}", ["SCPI", "SCI", "OPCI", "GFV", "GFI", "Club Deal"], key=f"type_c_{j}")
            st.text_input(f"Nom du support", key=f"nom_c_{j}")
        with t2:
            st.number_input(f"Valeur actuelle (€)", min_value=0, key=f"val_c_{j}")

st.markdown("---")

# --- SECTION 5 : PATRIMOINE FINANCIER ---
st.header("5. Patrimoine Financier")
st.info("Saisissez ici vos comptes bancaires, livrets, contrats d'assurance-vie, PEA, etc.")

nb_fin = st.number_input("Nombre de comptes ou contrats financiers", min_value=0, max_value=30, step=1)

total_financier = 0.0

for k in range(nb_fin):
    with st.expander(f"Contrat / Compte n°{k+1}", expanded=True):
        f1, f2, f3 = st.columns(3)
        with f1:
            type_f = st.selectbox(
                f"Type de placement {k+1}", 
                ["Livret (A, LDDS, PEL)", "Assurance-Vie", "PER", "PEA / PEA-PME", "Compte-Titres", "Crypto-actifs", "Compte Courant"],
                key=f"type_f_{k}"
            )
            etablissement = st.text_input(f"Établissement (Banque/Assureur)", key=f"etab_f_{k}")
        with f2:
            montant = st.number_input(f"Solde / Valeur actuelle (€)", min_value=0.0, step=100.0, key=f"val_f_{k}")
            total_financier += montant
            titulaire = st.selectbox(f"Titulaire", ["Client", "Conjoint", "Joint"], key=f"tit_f_{k}")
        with f3:
            performance = st.number_input(f"Rendement estimé (%)", min_value=0.0, max_value=20.0, step=0.1, key=f"perf_f_{k}")
            date_ouv = st.text_input(f"Date d'ouverture (MM/AAAA)", key=f"date_f_{k}")

# Affichage du total financier dynamique
if total_financier > 0:
    st.metric(label="Total Patrimoine Financier Saisi", value=f"{total_financier:,.0f} €".replace(",", " "))

st.markdown("---")
st.success("Sections 1 à 5 validées. Prêt pour les Assurances & Prévoyance (Section 6) ?")
