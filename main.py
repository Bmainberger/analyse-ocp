import streamlit as st
from datetime import date
import pandas as pd

# 1. CONFIGURATION & STYLE
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
        height: 3em;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. INITIALISATION DES COMPTEURS
total_brut_immo = 0.0
total_brut_fin = 0.0
total_passif = 0.0
mensualites_totales = 0.0

# 3. GESTION ACCÈS EXPERT
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
with col_b1:
    st.info("🔭 **Vision 360°**\n\nRegroupez tout votre patrimoine.")
with col_b2:
    st.info("📈 **Optimisation**\n\nRéduisez vos impôts.")
with col_b3:
    st.info("🛡️ **Sérénité**\n\nDiagnostic par un expert.")

st.markdown("---")

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
    age_ret = st.number_input("Âge de départ à la retraite prévu", min_value=50, max_value=80, value=64, key="age_ret")

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

# --- SECTION 7 : PRÉVOYANCE ---
st.header("7. Prévoyance & Protection")
nb_prev_input = st.number_input("Nombre de contrats de prévoyance", min_value=0, key="nb_p_v")
for p in range(int(nb_prev_input)):
    with st.expander(f"Contrat Prévoyance n°{p+1}"):
        st.number_input(f"Montant Garanti (€) {p}", key=f"p_m_{p}")

st.markdown("---")

# --- SECTION 8 : SANTÉ ---
st.header("8. Santé / Mutuelle")
col_s1, col_s2 = st.columns(2)
with col_s1:
    st.text_input("Assureur Santé", key="s_org")
with col_s2:
    st.number_input("Cotisation annuelle (€)", min_value=0.0, key="s_cot")

st.markdown("---")

# --- SECTION 9 : PASSIF ---
st.header("9. Passif & Endettement")
nb_pret_immo = st.number_input("Nombre de crédits immobiliers", min_value=0, key="nb_p_immo")
for i in range(int(nb_pret_immo)):
    with st.expander(f"Crédit Immo n°{i+1}"):
        crdu = st.number_input(f"Restant Dû (€) {i}", min_value=0.0, key=f"crdu_p_{i}")
        total_passif += crdu
        m_mens = st.number_input(f"Mensualité (€) {i}", min_value=0.0, key=f"mens_p_{i}")
        mensualites_totales += m_mens

# --- SECTION 10 : REMARQUES ---
st.markdown("---")
st.header("📝 10. Vos Remarques & Questions")
remarques_client = st.text_area("Avez-vous des précisions à nous apporter ?", key="rem_cli")

# --- SECTION 11 : OBJECTIFS ---
st.markdown("---")
st.header("🎯 11. Objectifs & Priorités")
col_obj1, col_obj2 = st.columns(2)
with col_obj1:
    obj_multi = st.multiselect("Objectifs principaux ?", ["Retraite", "Fiscalité", "Famille", "Transmission", "Immobilier"], key="obj_multi")
with col_obj2:
    horizon = st.select_slider("Horizon", options=["Court", "Moyen", "Long", "Transmission"], key="horizon_p")
    profil_r = st.select_slider("Profil de risque", options=["Prudent", "Équilibré", "Dynamique", "Offensif"], key="profil_r")

# --- SECTION 12 : RÉSUMÉ RÉSERVÉ À L'EXPERT ---
if st.session_state.get('is_expert', False):
    st.markdown("---")
    st.header("📊 ANALYSE STRATÉGIQUE BIG EXPERT")
    
    # CALCULS SÉCURISÉS (FILET ANTI-ROUGE)
    p_brut = float(total_brut_immo + total_brut_fin)
    p_net = float(p_brut - total_passif)
    r_annuel_expert = float(rev_annuel) if rev_annuel else 0.0
    r_mensuel_expert = (r_annuel_expert + float(rev_foncier)) / 12 if (r_annuel_expert + float(rev_foncier)) > 0 else 0.0
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Patrimoine Net", f"{p_net:,.0f} €".replace(",", " "))
    c2.metric("Revenu Mensuel", f"{r_mensuel_expert:,.0f} €".replace(",", " "))
    c3.metric("Endettement", f"{(total_passif/p_brut*100) if p_brut > 0 else 0:.1f} %")

    st.markdown("### 🎯 Diagnostics")
    tab_a, tab_b, tab_c, tab_d = st.tabs(["Structure", "Fiscalité", "Prévoyance", "Retraite"])
    
    with tab_a:
        st.write("**Répartition des Actifs**")
        df_st = pd.DataFrame({"Pilier": ["Immo", "Financier"], "Valeur": [total_brut_immo, total_brut_fin]})
        st.bar_chart(df_st.set_index("Pilier"))
        

    with tab_b:
        try:
            tmi_val = int(tmi_c.replace('%','')) if tmi_c else 30
        except:
            tmi_val = 30
        impot_est = r_annuel_expert * (tmi_val / 100) * 0.7
        st.write(f"Impôt annuel estimé : **{impot_est:,.0f} €**")
        st.info(f"Levier fiscal potentiel : {impot_est * 0.5:,.0f} € / an")

    with tab_c:
        besoin = r_annuel_expert * 3
        st.write(f"Besoin de protection familiale : **{besoin:,.0f} €**")
        st.caption("Protection suggérée pour maintenir le train de vie (3 ans).")
        

    with tab_d:
        retraite_est = r_mensuel_expert * 0.55
        gap = r_mensuel_expert - retraite_est
        st.write(f"Manque à gagner mensuel estimé : **{gap:,.0f} €**")
        cap_a_faire = gap * 12 / 0.04 if gap > 0 else 0
        st.warning(f"Capital à constituer pour compenser : {cap_a_faire:,.0f} €")

    st.text_area("Note de synthèse expert :", key="final_expert_notes")
    if st.button("✅ VALIDER L'ANALYSE"):
        st.balloons()

# --- BOUTON ENVOI CLIENT ---
if not st.session_state.get('is_expert', False):
    st.markdown("---")
    nom_cli = nom_client if nom_client else "Client"
    corps_mail = f"Dossier de {nom_cli}. Revenus: {rev_annuel}. Patrimoine: {total_brut_immo + total_brut_fin}."
    
    bouton_html = f"""
        <form action="https://formsubmit.co/bmainberger@ocp-patrimoine.com" method="POST">
            <input type="hidden" name="DOSSIER" value="{corps_mail}">
            <button type="submit" style="background-color: #1d2e4d; color: white; padding: 20px; font-size: 18px; border-radius: 8px; width: 100%; border: none; cursor: pointer; font-weight: bold;">
                🚀 TRANSMETTRE MON ÉTUDE
            </button>
        </form>
    """
    st.markdown(bouton_html, unsafe_allow_html=True)

