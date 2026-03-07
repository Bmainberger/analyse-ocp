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

# 2. INITIALISATION DES VARIABLES
total_brut_immo = 0.0
total_brut_fin = 0.0
total_passif = 0.0
mensualites_totales = 0.0
rev_annuel = 0.0

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

# 4. CONTENU PRINCIPAL
st.title("Votre stratégie patrimoniale commence ici.")
st.markdown("---")

# --- SECTION 1 À 3 : ÉTAT CIVIL & REVENUS ---
st.header("1. État Civil & Situation Familiale")
col1, col2 = st.columns(2)
with col1:
    nom_client = st.text_input("Nom du Client", key="nom_c")
    prenom_client = st.text_input("Prénom du Client", key="pre_c")
    date_naissance = st.date_input("Date de naissance", value=date(1980, 1, 1), key="dnaiss_c")
with col2:
    situation = st.selectbox("Situation Matrimoniale", ["Célibataire", "Marié(e)", "Pacsé(e)", "Divorcé(e)", "Veuf/Veuve"], key="sit_mat")
    nb_enfants = st.number_input("Nombre d'enfants à charge", min_value=0, max_value=15, step=1, key="nb_e")

st.header("2. Coordonnées")
c_coo1, c_coo2 = st.columns([2, 1])
with c_coo1: st.text_input("Adresse postale complète", key="adr_p")
with c_coo2: st.text_input("Téléphone", key="tel_p")

st.header("3. Situation Professionnelle & Revenus")
cp1, cp2, cp3 = st.columns(3)
with cp1:
    st.selectbox("Statut Professionnel", ["Salarié", "TNS / Libéral", "Dirigeant", "Fonctionnaire", "Retraité"], key="statut_pro")
with cp2:
    rev_annuel = st.number_input("Revenu net annuel (€)", min_value=0.0, key="rev_a")
with cp3:
    tmi_c = st.selectbox("Tranche Marginale d'Imposition (TMI)", ["0%", "11%", "30%", "41%", "45%"], key="tmi_c")

# --- SECTION 4 & 5 : IMMOBILIER (COMPLET) ---
st.header("4 & 5. Patrimoine Immobilier")
tab_im1, tab_im2 = st.tabs(["🏠 Immobilier Physique", "🏢 Pierre-Papier"])
with tab_im1:
    nb_biens = st.number_input("Nombre de biens immobiliers physiques", min_value=0, key="nb_p_p")
    for i in range(int(nb_biens)):
        with st.expander(f"Bien n°{i+1}", expanded=True):
            ci1, ci2 = st.columns(2)
            with ci1:
                st.selectbox(f"Type {i}", ["Résidence Principale", "Investissement", "Secondaire"], key=f"type_i_{i}")
                val_i = st.number_input(f"Valeur vénale (€) {i}", min_value=0.0, key=f"val_i_{i}")
                total_brut_immo += val_i
            with ci2:
                st.selectbox(f"Régime {i}", ["Nu", "LMNP", "Pinel"], key=f"fisc_i_{i}")
with tab_im2:
    nb_coll = st.number_input("Nombre de placements collectifs", min_value=0, key="nb_p_c")
    for j in range(int(nb_coll)):
        with st.expander(f"SCPI/SCI n°{j+1}", expanded=True):
            st.text_input(f"Nom du support {j}", key=f"nom_c_{j}")
            px_p = st.number_input(f"Prix de part (€) {j}", min_value=0.0, key=f"px_c_{j}")
            nb_p = st.number_input(f"Nombre de parts {j}", min_value=0.0, key=f"nb_c_{j}")
            total_brut_immo += (px_p * nb_p)

# --- SECTION 6 : FINANCIER (COMPLET) ---
st.header("6. Patrimoine Financier")
nb_fin = st.number_input("Nombre de contrats financiers", min_value=0, key="nb_f_f")
for k in range(int(nb_fin)):
    with st.expander(f"Contrat n°{k+1}"):
        f1, f2 = st.columns(2)
        with f1:
            st.selectbox(f"Type {k}", ["Assurance-Vie", "PER", "PEA", "Livret"], key=f"typ_f_{k}")
        with f2:
            m_f = st.number_input(f"Solde (€) {k}", min_value=0.0, key=f"m_f_{k}")
            total_brut_fin += m_f

# --- SECTION 7 & 8 : PRÉVOYANCE & SANTÉ ---
st.header("7. Prévoyance & Protection")
st.number_input("Nombre de contrats de prévoyance", min_value=0, key="nb_p_v")

st.header("8. Santé / Mutuelle")
st.text_input("Assureur Santé", key="s_org")

# --- SECTION 9 : PASSIF ---
st.header("9. Passif & Endettement")
nb_pret = st.number_input("Nombre de crédits immobiliers", min_value=0, key="nb_p_immo")
for i in range(int(nb_pret)):
    with st.expander(f"Crédit Immo n°{i+1}"):
        crdu = st.number_input(f"Restant Dû (€) {i}", min_value=0.0, key=f"crdu_p_{i}")
        total_passif += crdu
        mensualites_totales += st.number_input(f"Mensualité (€) {i}", min_value=0.0, key=f"mens_p_{i}")

# --- SECTION 10 & 11 : COMMENTAIRES ET OBJECTIFS ---
st.header("📝 10. Commentaires & Préconisations")
if st.session_state['is_expert']:
    st.text_area("Note de Synthèse de l'Expert", key="syn_expert")
else:
    st.text_area("Vos précisions", key="com_client")

st.header("🎯 11. Objectifs & Priorités")
st.multiselect("Objectifs ?", ["Retraite", "Fiscalité", "Transmission"], key="obj_multi")

# --- ANALYSE STRATÉGIQUE (ONGLETS AU CENTRE) ---
if st.session_state['is_expert']:
    st.markdown("---")
    st.header("📊 ANALYSE STRATÉGIQUE BIG EXPERT")
    
    pat_brut = total_brut_immo + total_brut_fin
    pat_net = pat_brut - total_passif
    
    met1, met2, met3 = st.columns(3)
    met1.metric("Patrimoine Net", f"{pat_net:,.0f} €")
    met2.metric("Revenu Mensuel", f"{(rev_annuel/12):,.0f} €")
    ratio = (total_passif/pat_brut*100) if pat_brut > 0 else 0
    met3.metric("Endettement", f"{ratio:.1f}%")

    diag_tabs = st.tabs(["Structure", "Fiscalité", "Prévoyance", "Retraite"])
    
    with diag_tabs[0]:
        st.write("**Analyse de la structure**")
        if total_brut_fin < (rev_annuel / 2):
            st.error("🚨 Liquidité de précaution insuffisante.")
        else:
            st.success("✅ Épargne de précaution OK.")
            
    with diag_tabs[1]:
        st.write("**Analyse Fiscale**")
        st.info(f"TMI actuelle : {tmi_c}")
        if tmi_c in ["30%", "41%", "45%"]:
            st.warning("Optimisation fiscale recommandée.")

    with diag_tabs[2]:
        st.write("**Analyse Prévoyance**")
        st.write("Protection familiale à auditer.")

    with diag_tabs[3]:
        st.write("**Analyse Retraite**")
        gap = (rev_annuel / 12) * 0.45
        st.info(f"Gap Retraite estimé : -{gap:,.0f} € / mois")

    if st.button("📄 GÉNÉRER LE BILAN PDF"):
        st.success("PDF Généré (Simulation)")

# --- BOUTON FINAL ---
if not st.session_state['is_expert']:
    st.markdown("---")
    if st.button("🚀 TRANSMETTRE MON ÉTUDE"):
        st.balloons()
