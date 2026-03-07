import streamlit as st
from datetime import date
from fpdf import FPDF

# 1. CONFIGURATION ET STYLE
st.set_page_config(page_title="OCP Patrimoine", page_icon="🛡️", layout="wide")

st.markdown("""
    <style>
    div.stButton > button:first-child {
        background-color: #1d2e4d;
        color: white;
        font-size: 20px;
        font-weight: bold;
        width: 100%;
        border-radius: 5px;
        border: none;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. INITIALISATION DES COMPTEURS
total_brut_immo = 0.0
total_brut_fin = 0.0
total_passif = 0.0
mensualites_totales = 0.0
rev_annuel = 0.0
rev_foncier = 0.0

# 3. ACCÈS EXPERT
if 'is_expert' not in st.session_state:
    st.session_state['is_expert'] = False

with st.sidebar:
    st.title("🔐 Espace Expert")
    code_admin = st.text_input("Code confidentiel", type="password")
    if code_admin == "ADMINOCP":
        st.session_state['is_expert'] = True
        st.success("Mode Expert Activé")
    else:
        st.session_state['is_expert'] = False

# 4. LANDING PAGE
st.title("Votre stratégie patrimoniale commence ici.")
col_b1, col_b2, col_b3 = st.columns(3)
with col_b1: st.info("🔭 **Vision 360°**\n\nRegroupez tout votre patrimoine.")
with col_b2: st.info("📈 **Optimisation**\n\nRéduisez vos impôts.")
with col_b3: st.info("🛡️ **Sérénité**\n\nDiagnostic par un expert.")

st.markdown("---")

# --- SECTION 1 À 11 (VOS MODULES INTACTS) ---

# 1. ÉTAT CIVIL
st.header("1. État Civil & Situation Familiale")
col1, col2 = st.columns(2)
with col1:
    nom_client = st.text_input("Nom du Client", key="nom_c")
    prenom_client = st.text_input("Prénom du Client", key="pre_c")
    date_naissance = st.date_input("Date de naissance", value=date(1980, 1, 1), key="dnaiss_c")
with col2:
    situation = st.selectbox("Situation Matrimoniale", ["Célibataire", "Marié(e)", "Pacsé(e)", "Divorcé(e)", "Veuf/Veuve"], key="sit_mat")
    nb_enfants = st.number_input("Nombre d'enfants à charge", min_value=0, max_value=15, step=1, key="nb_e")

# 2. COORDONNÉES
st.header("2. Coordonnées")
c_coo1, c_coo2 = st.columns([2, 1])
with c_coo1: st.text_input("Adresse postale complète", key="adr_p")
with c_coo2: st.text_input("Téléphone", key="tel_p")

# 3. REVENUS
st.header("3. Situation Professionnelle & Revenus")
cp1, cp2, cp3 = st.columns(3)
with cp1: st.selectbox("Statut", ["Salarié", "TNS", "Dirigeant", "Retraité"], key="statut_pro")
with cp2: rev_annuel = st.number_input("Revenu net annuel (€)", min_value=0.0, key="rev_a")
with cp3: tmi_c = st.selectbox("TMI", ["0%", "11%", "30%", "41%", "45%"], key="tmi_c")

# 4 & 5. IMMOBILIER (COMPLET)
st.header("4 & 5. Patrimoine Immobilier")
tab1, tab2 = st.tabs(["🏠 Immobilier Physique", "🏢 Pierre-Papier"])
with tab1:
    nb_biens = st.number_input("Nombre de biens", min_value=0, key="nb_p_p")
    for i in range(int(nb_biens)):
        with st.expander(f"Bien n°{i+1}"):
            val_i = st.number_input(f"Valeur (€) {i}", key=f"val_i_{i}")
            total_brut_immo += val_i
with tab2:
    nb_coll = st.number_input("Nombre de placements collectifs", min_value=0, key="nb_p_c")
    for j in range(int(nb_coll)):
        with st.expander(f"Placement n°{j+1}"):
            t_coll = st.selectbox(f"Type {j}", ["SCPI", "SCI", "OPCI", "GFV"], key=f"type_c_{j}")
            px_p = st.number_input(f"Prix part {j}", key=f"px_c_{j}")
            nb_p = st.number_input(f"Nombre parts {j}", key=f"nb_c_{j}")
            total_brut_immo += (px_p * nb_p)

# 6. FINANCIER
st.header("6. Patrimoine Financier")
nb_fin = st.number_input("Nombre de contrats financiers", min_value=0, key="nb_f_f")
for k in range(int(nb_fin)):
    with st.expander(f"Contrat n°{k+1}"):
        m_f = st.number_input(f"Solde (€) {k}", key=f"m_f_{k}")
        total_brut_fin += m_f

# 7 & 8. PRÉVOYANCE & SANTÉ
st.header("7 & 8. Protection & Santé")
st.number_input("Contrats de prévoyance", min_value=0, key="nb_p_v")
st.text_input("Assureur Santé", key="s_org")

# 9. PASSIF
st.header("9. Passif & Endettement")
nb_pret_immo = st.number_input("Nombre de crédits", min_value=0, key="nb_p_immo")
for i in range(int(nb_pret_immo)):
    with st.expander(f"Crédit n°{i+1}"):
        crdu = st.number_input(f"Restant Dû (€) {i}", key=f"crdu_p_{i}")
        total_passif += crdu
        mensualites_totales += st.number_input(f"Mensualité (€) {i}", key=f"mens_p_{i}")

# 10. COMMENTAIRES
st.header("10. Commentaires")
st.text_area("Notes", key="com_client")
if st.session_state['is_expert']:
    synthese_expert = st.text_area("Note de Synthèse (Expert)", key="syn_expert")

# 11. OBJECTIFS
st.header("11. Objectifs")
st.multiselect("Priorités", ["Retraite", "Fiscalité", "Transmission"], key="obj_multi")

# --- PARTIE 1 : LA SIDEBAR (POUR L'EXPERT) ---
if st.session_state['is_expert']:
    with st.sidebar:
        st.markdown("---")
        st.subheader("📊 Pilotage Expert")
        pat_brut = total_brut_immo + total_brut_fin
        pat_net = pat_brut - total_passif
        st.metric("Patrimoine Net", f"{pat_net:,.0f} €")
        
        # Alertes rapides
        if total_brut_fin < (rev_annuel / 2): st.error("🚨 Liquidité Faible")
        else: st.success("✅ Liquidité OK")

# --- PARTIE 2 : LA NOUVELLE SYNTHÈSE CENTRALE (POUR LE CLIENT) ---
if st.session_state['is_expert']:
    st.markdown("---")
    st.header("📊 BILAN PATRIMONIAL - ANALYSE STRATÉGIQUE")
    
    # Calculs pour l'affichage central
    pat_brut = total_brut_immo + total_brut_fin
    pat_net = pat_brut - total_passif
    ratio_dette = (total_passif / pat_brut * 100) if pat_brut > 0 else 0
    
    # KPIs en grand au centre
    kpi1, kpi2, kpi3 = st.columns(3)
    kpi1.metric("VALEUR NETTE DU PATRIMOINE", f"{pat_net:,.0f} €")
    kpi2.metric("REVENUS MENSUELS", f"{(rev_annuel/12):,.0f} €")
    kpi3.metric("RATIO D'ENDETTEMENT", f"{ratio_dette:.1f} %")

    # Les 4 Piliers d'hier réintégrés ici au centre
    st.subheader("🎯 Diagnostic des 4 Piliers")
    tab_diag1, tab_diag2, tab_diag3, tab_diag4 = st.tabs(["Structure", "Fiscalité", "Prévoyance", "Retraite"])
    
    with tab_diag1:
        st.markdown("### 🏦 Structure & Liquidité")
        if total_brut_fin < (rev_annuel / 2):
            st.warning("Votre épargne disponible est inférieure à 6 mois de revenus. Il est conseillé de renforcer votre poche de liquidité.")
        else:
            st.success("Votre structure de patrimoine présente une excellente liquidité de précaution.")

    with tab_diag2:
        st.markdown("### ⚖️ Optimisation Fiscale")
        st.write(f"Votre TMI est de **{tmi_c}**.")
        if tmi_c in ["30%", "41%", "45%"]:
            st.info("Des leviers de défiscalisation (PER, SCPI Fiscales, Girardin) sont recommandés pour réduire votre pression fiscale.")
        else:
            st.write("La pression fiscale est modérée sur vos revenus actuels.")

    with tab_diag3:
        st.markdown("### 🛡️ Prévoyance & Protection")
        besoin_dc = rev_annuel * 3
        st.write(f"Pour maintenir le niveau de vie de votre famille, un capital décès minimum de **{besoin_dc:,.0f} €** est préconisé.")

    with tab_diag4:
        st.markdown("### 📉 Préparation Retraite")
        gap = (rev_annuel / 12) * 0.45
        st.warning(f"Le manque à gagner estimé à la retraite est de **{gap:,.0f} € par mois**. Une stratégie de revenus complémentaires est à prévoir.")

    # Bouton PDF central
    if st.button("📄 GÉNÉRER LE BILAN PDF POUR LE CLIENT"):
        st.balloons()
        st.success("PDF en cours de préparation...")

# --- SECTION FINALE (ENVOI) ---
if not st.session_state['is_expert']:
    st.markdown("---")
    st.markdown('<button style="background-color: #1d2e4d; color: white; padding: 20px; font-size: 18px; border-radius: 8px; width: 100%; border: none; font-weight: bold;">🚀 TRANSMETTRE MON ÉTUDE</button>', unsafe_allow_html=True)
