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
    nom_client = st.text_input("Nom du Client")
    prenom_client = st.text_input("Prénom du Client")
    date_naissance = st.date_input("Date de naissance", value=date(1980, 1, 1))
with col2:
    situation = st.selectbox("Situation Matrimoniale", ["Célibataire", "Marié(e)", "Pacsé(e)", "Divorcé(e)", "Veuf/Veuve"])
    nb_enfants = st.number_input("Nombre d'enfants à charge", min_value=0, max_value=15, step=1)

st.markdown("---")

# --- SECTION 2 : ADRESSE & PRO ---
st.header("2. Coordonnées et Situation Professionnelle")
col3, col4 = st.columns(2)
with col3:
    adresse = st.text_input("Adresse complète")
    residence_statut = st.radio("Statut résidence", ["Propriétaire", "Locataire", "Logé par l'employeur"])
with col4:
    statut_pro = st.selectbox("Statut professionnel", ["Salarié", "TNS", "Fonctionnaire", "Retraité"])
    revenu_annuel = st.number_input("Revenu Annuel Net (€)", min_value=0, step=1000)

st.markdown("---")

# --- SECTION 3 & 4 : IMMOBILIER ---
st.header("3 & 4. Patrimoine Immobilier (Physique & Collectif)")
tab1, tab2 = st.tabs(["🏠 Immobilier Physique", "🏢 Pierre-Papier (SCPI...)"])
with tab1:
    nb_biens = st.number_input("Nombre de biens immobiliers", min_value=0)
    for i in range(nb_biens):
        with st.expander(f"Bien n°{i+1}"):
            st.selectbox(f"Type", ["Résidence Principale", "Résidence Secondaire", "Locatif"], key=f"type_i_{i}")
            st.number_input(f"Valeur vénale (€)", min_value=0, key=f"val_i_{i}")
with tab2:
    nb_coll = st.number_input("Nombre de placements collectifs", min_value=0)
    for j in range(nb_coll):
        with st.expander(f"Placement n°{j+1}"):
            st.selectbox(f"Type", ["SCPI", "SCI", "OPCI", "GFV", "GFI"], key=f"type_c_{j}")
            st.number_input(f"Valeur actuelle (€)", min_value=0, key=f"val_c_{j}")

st.markdown("---")

# --- SECTION 5 : PATRIMOINE FINANCIER ---
st.header("5. Patrimoine Financier")
nb_fin = st.number_input("Nombre de comptes/contrats financiers", min_value=0)
total_fin = 0.0
for k in range(nb_fin):
    with st.expander(f"Contrat n°{k+1}"):
        c_fin1, c_fin2 = st.columns(2)
        with c_fin1:
            st.selectbox("Support", ["Livret", "Assurance-Vie", "PEA", "PER", "Compte-Titres", "Crypto"], key=f"typ_f_{k}")
        with c_fin2:
            m_f = st.number_input("Montant (€)", min_value=0.0, key=f"m_f_{k}")
            total_fin += m_f
if total_fin > 0:
    st.metric("Total Épargne Financière", f"{total_fin:,.0f} €".replace(",", " "))

st.markdown("---")

# --- SECTION 6 : PRÉVOYANCE (VERSION EXPERTE) ---
st.header("6. Prévoyance & Protection")
nb_prev = st.number_input("Nombre de contrats de prévoyance", min_value=0, step=1)
for p in range(nb_prev):
    with st.expander(f"Contrat de Prévoyance n°{p+1}", expanded=False):
        p1, p2 = st.columns(2)
        with p1:
            t_prev = st.selectbox("Type de garantie", 
                ["Garantie Décès", "Invalidité / Incapacité", "Arrêt de travail (IJ)", "Dépendance", "GAV", "Assurance Emprunteur"], 
                key=f"type_p_{p}")
            st.text_input("Assureur", key=f"ass_p_{p}")
            st.text_input("Bénéficiaires", key=f"ben_p_{p}")
        with p2:
            st.number_input("Capital ou Rente garanti (€)", min_value=0, key=f"cap_p_{p}")
            st.number_input("Cotisation Annuelle (€)", min_value=0, key=f"cot_p_{p}")
            st.selectbox("Statut du contrat", ["Actif", "Résilié", "Suspendu"], key=f"stat_p_{p}")

        # Détails spécifiques selon le type
        st.markdown("**Détails techniques :**")
        d1, d2 = st.columns(2)
        if t_prev == "Arrêt de travail (IJ)":
            with d1: st.selectbox("Franchise", ["7j", "15j", "30j", "90j"], key=f"fran_p_{p}")
            with d2: st.number_input("Durée max indemnisation (jours)", value=1095, key=f"dur_p_{p}")
        elif t_prev == "Invalidité / Incapacité":
            with d1: st.selectbox("Barème", ["Professionnel", "Sécurité Sociale", "Croisé"], key=f"bar_p_{p}")
            with d2: st.number_input("Taux de déclenchement (%)", value=33, key=f"taux_p_{p}")
        elif t_prev == "Assurance Emprunteur":
            with d1: st.number_input("Quotité (%)", value=100, key=f"quo_p_{p}")
            with d2: st.multiselect("Garanties", ["Décès", "PTIA", "IPT", "ITT", "Perte Emploi"], key=f"gar_p_{p}")

st.markdown("---")

# --- SECTION 7 : SANTÉ (VERSION EXPERTE) ---
st.header("7. Santé / Mutuelle")
col_s1, col_s2 = st.columns(2)
with col_s1:
    st.subheader("Informations Générales")
    st.text_input("Assureur Santé")
    st.selectbox("Type de contrat", ["Individuel", "Collectif Entreprise", "Senior", "Madelin (TNS)"])
    st.number_input("Cotisation Mensuelle (€)", min_value=0)
with col_s2:
    st.subheader("Niveaux de Remboursement (%)")
    st.number_input("Consultations / Spécialistes", value=100, step=50)
    st.number_input("Optique / Dentaire", value=200, step=50)
    st.number_input("Hospitalisation", value=100, step=50)

st.markdown("---")
st.success("Sections 1 à 7 (Expert) opérationnelles ! On continue avec les Objectifs ?")
