import streamlit as st
from datetime import date

# 1. CONFIGURATION
st.set_page_config(page_title="OCP Patrimoine - Diagnostic", layout="wide")

# 2. LOGIQUE D'ACCÈS (BARRE DE GAUCHE)
if 'is_expert' not in st.session_state:
    st.session_state['is_expert'] = False

with st.sidebar:
    st.title("🔐 Accès OCP")
    code_saisi = st.text_input("Code Expert (Optionnel)", type="password", key="auth_expert_unique")
    if code_saisi == "ADMINOCP":
        st.session_state['is_expert'] = True
        st.success("👨‍💼 MODE EXPERT ACTIVÉ")
    else:
        st.session_state['is_expert'] = False
        st.caption("Visiteur : Remplissez le formulaire ci-contre.")

# 3. TITRE PRINCIPAL
st.title("🏢 OCP Patrimoine : Votre Diagnostic en ligne")
st.markdown("---")

# 4. INITIALISATION DES VARIABLES DE CALCUL
total_brut_immo = 0.0
total_brut_fin = 0.0
total_passif = 0.0
mensualites_totales = 0.0
reste_vivre_brut = 0.0

# --- SECTION 1 : ÉTAT CIVIL & FAMILLE ---
st.header("1. État Civil & Situation Familiale")
col1, col2 = st.columns(2)
with col1:
    st.subheader("Le Client")
    nom_client = st.text_input("Nom du Client", key="nom_c")
    prenom_client = st.text_input("Prénom du Client", key="pre_c")
    date_naissance = st.date_input("Date de naissance", value=date(1980, 1, 1), key="dnaiss_c")
    lieu_naissance = st.text_input("Lieu de naissance", key="lieu_c")
    nationalite = st.text_input("Nationalité", key="nat_c") 

with col2:
    st.subheader("Situation")
    situation = st.selectbox("Situation Matrimoniale", ["Célibataire", "Marié(e)", "Pacsé(e)", "Divorcé(e)", "Veuf/Veuve"], key="sit_mat")
    nb_enfants = st.number_input("Nombre d'enfants à charge", min_value=0, max_value=15, step=1, key="nb_e")

if situation in ["Marié(e)", "Pacsé(e)"]:
    st.markdown("---")
    st.subheader("Informations du Conjoint")
    c_col1, c_col2 = st.columns(2)
    with c_col1:
        nom_conj = st.text_input("Nom du Conjoint", key="nom_conj")
        dnaiss_conj = st.date_input("Date de naissance conjoint", value=date(1980, 1, 1), key="dnaiss_conj")
    with c_col2:
        pre_conj = st.text_input("Prénom du Conjoint", key="pre_conj")

if nb_enfants > 0:
    st.write("📅 **Détail des enfants :**")
    c_enf = st.columns(3)
    for i in range(int(nb_enfants)):
        with c_enf[i % 3]:
            st.date_input(f"Date de naissance Enfant n°{i+1}", value=date(2010, 1, 1), key=f"dnaiss_enf_{i}")

st.markdown("---")

# --- SECTION 2 : COORDONNÉES ---
st.header("2. Coordonnées")
c_coo1, c_coo2, c_coo3 = st.columns([2, 1, 1])
with c_coo1:
    st.text_input("Adresse postale complète", key="adr_p")
with c_coo2:
    st.text_input("Téléphone", key="tel_p")
with c_coo3:
    st.text_input("Email", key="mail_p")

st.markdown("---")

# --- SECTION 3 : PROFESSION & REVENUS ---
st.header("3. Situation Professionnelle & Revenus")
cp1, cp2, cp3 = st.columns(3)
with cp1:
    st.selectbox("Statut Professionnel", ["Salarié", "TNS / Libéral", "Dirigeant", "Fonctionnaire", "Retraité", "Sans activité"], key="statut_pro")
    st.text_input("Profession / Intitulé du poste", key="poste_pro")
with cp2:
    rev_annuel = st.number_input("Revenu net annuel (€)", min_value=0.0, key="rev_a")
    rev_foncier = st.number_input("Autres revenus (Foncier, etc.) (€)", min_value=0.0, key="rev_f")
with cp3:
    tmi_c = st.selectbox("Tranche Marginale d'Imposition (TMI)", ["0%", "11%", "30%", "41%", "45%"], key="tmi_c")
    st.number_input("Âge de départ à la retraite prévu", min_value=50, max_value=80, value=64, key="age_ret")

st.subheader("📊 3. bis Budget & Capacité d'Épargne")
b_col1, b_col2 = st.columns(2)
with b_col1:
    vie_courante = st.number_input("Train de vie mensuel (€)", min_value=0.0, key="budget_vie")
    loyer_mens = st.number_input("Loyer ou Charges (€)", min_value=0.0, key="budget_loyer")
with b_col2:
    impots_mens = st.number_input("Impôts mensuels (€)", min_value=0.0, key="budget_impot")
    rev_mensuel_estim = (rev_annuel + rev_foncier) / 12
    reste_vivre_brut = rev_mensuel_estim - (vie_courante + loyer_mens + impots_mens)
    st.info(f"Revenus mensuels estimés : {rev_mensuel_estim:,.0f} €")

st.markdown("---")

# --- SECTION 4 & 5 : PATRIMOINE IMMOBILIER ---
st.header("4 & 5. Patrimoine Immobilier")
tab1, tab2 = st.tabs(["🏠 Immobilier Physique", "🏢 Pierre-Papier"])
with tab1:
    nb_biens = st.number_input("Nombre de biens immobiliers physiques", min_value=0, key="nb_p_p")
    for i in range(int(nb_biens)):
        with st.expander(f"Bien n°{i+1}", expanded=True):
            val_i = st.number_input(f"Valeur vénale (€) {i}", min_value=0.0, key=f"val_i_{i}")
            total_brut_immo += val_i
with tab2:
    nb_coll = st.number_input("Nombre de placements collectifs", min_value=0, key="nb_p_c")
    for j in range(int(nb_coll)):
        with st.expander(f"Placement Collectif n°{j+1}", expanded=True):
            px_p = st.number_input(f"Prix de part (€) {j}", min_value=0.0, key=f"px_c_{j}")
            nb_p = st.number_input(f"Nombre de parts {j}", min_value=0.0, key=f"nb_c_{j}")
            total_brut_immo += (px_p * nb_p)

st.markdown("---")

# --- SECTION 6 : PATRIMOINE FINANCIER ---
st.header("6. Patrimoine Financier")
nb_fin = st.number_input("Nombre de comptes/contrats financiers", min_value=0, key="nb_f_f")
for k in range(int(nb_fin)):
    with st.expander(f"Contrat n°{k+1}"):
        m_f = st.number_input(f"Solde (€) {k}", min_value=0.0, key=f"m_f_{k}")
        total_brut_fin += m_f

st.markdown("---")

# --- SECTION 7 & 8 : PRÉVOYANCE & SANTÉ ---
st.header("7 & 8. Protection & Santé")
st.number_input("Nombre de contrats de prévoyance", min_value=0, key="nb_p_v")
st.text_input("Assureur Santé", key="s_org")

st.markdown("---")

# --- SECTION 9 : PASSIF ---
st.header("9. Passif & Endettement")
nb_pret_immo = st.number_input("Nombre de crédits immobiliers", min_value=0, key="nb_p_immo")
for i in range(int(nb_pret_immo)):
    crdu = st.number_input(f"Restant Dû (€) {i}", min_value=0.0, key=f"crdu_p_{i}")
    total_passif += crdu
    mensualites_totales += st.number_input(f"Mensualité (€) {i}", min_value=0.0, key=f"mens_p_{i}")

st.markdown("---")

# --- SECTION 11 : OBJECTIFS ---
st.header("🎯 11. Objectifs & Priorités")
profil_r = st.select_slider("Profil de risque", options=["Prudent", "Équilibré", "Dynamique", "Offensif"], key="profil_r")
horizon = st.select_slider("Horizon", options=["Court terme", "Moyen terme", "Long terme", "Transmission"], key="horizon_p")

# --- LOGIQUE EXPERT (SYNTHÈSE) ---
pat_brut = total_brut_immo + total_brut_fin
pat_net = pat_brut - total_passif
capa_epargne = reste_vivre_brut - mensualites_totales

if st.session_state.get('is_expert', False):
    st.sidebar.markdown("---")
    st.sidebar.title("📊 Synthèse Expert")
    st.sidebar.metric("PATRIMOINE NET", f"{pat_net:,.0f} €".replace(",", " "))
    st.sidebar.metric("ÉPARGNE MENSUELLE", f"{capa_epargne:,.0f} €")
    
    if st.button("🚀 GÉNÉRER LE BILAN EXPERT"):
        st.balloons()
        st.header("📋 Diagnostic Patrimonial OCP")
        col_an1, col_an2 = st.columns(2)
        with col_an1:
            st.metric("Patrimoine Brut", f"{pat_brut:,.0f} €")
        with col_an2:
            st.metric("Poids de l'Immobilier", f"{(total_brut_immo/pat_brut*100 if pat_brut>0 else 0):.1f}%")

# --- BOUTON FINAL CLIENT ---
if not st.session_state.get('is_expert', False):
    st.markdown("---")
    if st.button("📤 ENVOYER MON DOSSIER"):
        st.balloons()
        st.success("Vos informations ont été transmises avec succès.")
