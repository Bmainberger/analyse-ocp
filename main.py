import streamlit as st
from datetime import date
import json

# 1. CONFIGURATION DE LA PAGE
st.set_page_config(page_title="OCP Patrimoine", page_icon="🛡️", layout="wide")

# Style visuel (Votre style d'origine avec le bouton vert)
st.markdown("""
    <style>
    .main { background-color: #ffffff; }
    div.stButton > button {
        background-color: #26e291; color: #1a2b49; border-radius: 8px;
        padding: 0.7em 2.5em; font-weight: bold; border: none;
    }
    .hero-title { font-size: 3rem; font-weight: 800; color: #1a2b49; }
    .benefit-card { background-color: #f8fafc; padding: 20px; border-radius: 10px; border-left: 5px solid #26e291; height: 100%; }
    </style>
    """, unsafe_allow_html=True)

# Initialisation des variables de navigation
if 'page' not in st.session_state:
    st.session_state['page'] = 'home'
if 'is_expert' not in st.session_state:
    st.session_state['is_expert'] = False

# --- LOGIQUE DE LA BARRE LATÉRALE (POUR VOUS ET LES CODES PRIVÉS) ---
with st.sidebar:
    st.title("🔐 Accès Privé")
    code_input = st.text_input("Saisissez votre code (Optionnel)", type="password")
    
    if code_input == "ADMINOCP":
        st.session_state['is_expert'] = True
        st.session_state['page'] = 'formulaire'
        st.success("👨‍💼 MODE EXPERT ACTIVÉ")
    elif code_input == "OCP2026":
        st.session_state['is_expert'] = False
        st.session_state['page'] = 'formulaire'
        st.info("✅ ACCÈS CLIENT RECONNU")

# --- PAGE D'ACCUEIL (POUR LES PROSPECTS DU WEB - SANS CODE) ---
if st.session_state['page'] == 'home':
    st.markdown('<h1 class="hero-title">Votre stratégie patrimoniale commence ici.</h1>', unsafe_allow_html=True)
    
    # Présentation Pro type Harvest
    col_b1, col_b2, col_b3 = st.columns(3)
    with col_b1:
        st.markdown('<div class="benefit-card"><h3>🔭 Vision 360°</h3><p>Regroupez immo, placements et dettes sur une seule interface.</p></div>', unsafe_allow_html=True)
    with col_b2:
        st.markdown('<div class="benefit-card"><h3>📈 Optimisation</h3><p>Réduisez vos impôts et préparez votre transmission.</p></div>', unsafe_allow_html=True)
    with col_b3:
        st.markdown('<div class="benefit-card"><h3>🛡️ Sérénité</h3><p>Un diagnostic clair réalisé par un expert OCP.</p></div>', unsafe_allow_html=True)
    
    st.write("")
    if st.button("DÉMARRER MON ANALYSE"):
        st.session_state['page'] = 'formulaire'
        st.rerun()
    st.stop()

# --- SI ON EST SUR LE FORMULAIRE (VOTRE CODE COMPLET) ---

# Variables de calcul (Initialisées ici pour ne pas planter)
total_brut_immo = 0.0
total_brut_fin = 0.0
total_passif = 0.0
mensualites_totales = 0.0

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
        st.text_input("Lieu de naissance conjoint", key="lieu_conj")
    with c_col2:
        pre_conj = st.text_input("Prénom du Conjoint", key="pre_conj")
        st.text_input("Nationalité Conjoint", key="nat_conj")

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
with c_coo1: st.text_input("Adresse postale complète", key="adr_p")
with c_coo2: st.text_input("Téléphone", key="tel_p")
with c_coo3: st.text_input("Email", key="mail_p")

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
    loyer_mens = st.number_input("Loyer ou Charges de copropriété (€)", min_value=0.0, key="budget_loyer")
with b_col2:
    impots_mens = st.number_input("Impôts mensuels (€)", min_value=0.0, key="budget_impot")
    rev_mens_estim = (rev_annuel + rev_foncier) / 12
    reste_vivre_brut = rev_mens_estim - (vie_courante + loyer_mens + impots_mens)
    st.info(f"Revenus mensuels estimés : {rev_mens_estim:,.0f} €")

st.markdown("---")

# --- SECTION 4 & 5 : PATRIMOINE IMMOBILIER ---
st.header("4 & 5. Patrimoine Immobilier")
tab1, tab2 = st.tabs(["🏠 Immobilier Physique", "🏢 Pierre-Papier (SCPI, SCI, GFV...)"])
with tab1:
    nb_biens = st.number_input("Nombre de biens immobiliers physiques", min_value=0, key="nb_p_p")
    for i in range(int(nb_biens)):
        with st.expander(f"Bien n°{i+1}", expanded=True):
            c1, c2 = st.columns(2)
            with c1:
                st.selectbox(f"Type {i}", ["Résidence Principale", "Résidence Secondaire", "Appartement", "Maison", "Parking"], key=f"type_i_{i}")
                val_i = st.number_input(f"Valeur vénale (€) {i}", min_value=0.0, key=f"val_i_{i}")
                total_brut_immo += val_i
            with c2:
                st.selectbox(f"Régime {i}", ["Droit Commun", "LMNP", "LMP", "Pinel"], key=f"fisc_i_{i}")
                st.radio(f"Crédit en cours ? {i}", ["Non", "Oui"], key=f"cred_i_{i}")

with tab2:
    nb_coll = st.number_input("Nombre de placements collectifs", min_value=0, key="nb_p_c")
    for j in range(int(nb_coll)):
        with st.expander(f"Placement n°{j+1}", expanded=True):
            t_coll = st.selectbox(f"Type {j}", ["SCPI", "SCI", "GFV / GFI"], key=f"type_c_{j}")
            c1, c2, c3 = st.columns(3)
            with c1:
                st.text_input(f"Nom support {j}", key=f"nom_c_{j}")
                st.selectbox(f"Détention {j}", ["Pleine Propriété", "Nue-Propriété", "AV"], key=f"det_c_{j}")
            with c2:
                px_p = st.number_input(f"Prix part (€) {j}", min_value=0.0, key=f"px_c_{j}")
                nb_p = st.number_input(f"Nombre parts {j}", min_value=0.0, key=f"nb_c_{j}")
                val_liq = px_p * nb_p
                total_brut_immo += val_liq
            with c3:
                if t_coll == "SCPI": st.number_input(f"TOF (%) {j}", key=f"tof_c_{j}")
                elif t_coll == "GFV / GFI": st.text_input(f"Surface {j}", key=f"surf_c_{j}")

st.markdown("---")

# --- SECTION 6 : PATRIMOINE FINANCIER ---
st.header("6. Patrimoine Financier")
nb_fin = st.number_input("Nombre de contrats financiers", min_value=0, key="nb_f_f")
for k in range(int(nb_fin)):
    with st.expander(f"Contrat n°{k+1}"):
        f1, f2, f3 = st.columns(3)
        with f1:
            st.selectbox(f"Type {k}", ["Livret", "Assurance-Vie", "PER", "PEA"], key=f"typ_f_{k}")
            st.text_input(f"Établissement {k}", key=f"banque_f_{k}")
        with f2:
            m_f = st.number_input(f"Solde (€) {k}", key=f"m_f_{k}")
            total_brut_fin += m_f
            st.date_input(f"Date adhésion {k}", key=f"date_f_{k}")
        with f3: st.selectbox(f"Support {k}", ["Mono", "Multi", "Pilotée"], key=f"gest_f_{k}")

st.markdown("---")

# --- SECTION 7 : PRÉVOYANCE ---
st.header("7. Prévoyance & Protection")
nb_prev = st.number_input("Nombre de contrats de prévoyance", min_value=0, key="nb_p_v")
for p in range(int(nb_prev)):
    with st.expander(f"Contrat Prévoyance n°{p+1}"):
        p1, p2, p3 = st.columns(3)
        with p1: type_p = st.selectbox(f"Garantie {p}", ["Décès", "Rente", "IJ", "Invalidité", "Emprunteur"], key=f"p_t_{p}")
        with p2:
            st.number_input(f"Montant (€) {p}", key=f"p_m_{p}")
            if type_p == "Emprunteur": st.number_input(f"Quotité (%) {p}", key=f"p_q_{p}")
        with p3: st.text_input(f"Bénéficiaires {p}", key=f"p_b_{p}")

st.markdown("---")

# --- SECTION 8 : SANTÉ ---
st.header("8. Santé / Mutuelle")
s1, s2, s3 = st.columns(3)
with s1:
    st.text_input("Assureur Santé", key="s_org")
    st.selectbox("Type", ["Individuel", "Collectif", "Madelin"], key="s_typ")
with s2:
    st.number_input("Cotisation (€)", key="s_cot")
    st.select_slider("Couverture", options=["100%", "200%", "300%", "Frais réels"], key="s_niv")
with s3:
    st.multiselect("Couverture", ["Client", "Conjoint", "Enfant(s)"], key="s_couv")
    st.text_area("Notes", key="s_notes")

st.markdown("---")

# --- SECTION 9 : PASSIF ---
st.header("9. Passif & Endettement")
tab_p1, tab_p2 = st.tabs(["🏠 Crédits Immo", "💳 Autres Crédits"])
with tab_p1:
    nb_p_immo = st.number_input("Nombre de crédits immobiliers", min_value=0, key="nb_p_immo")
    for i in range(int(nb_p_immo)):
        with st.expander(f"Crédit n°{i+1}"):
            cp1, cp2, cp3 = st.columns(3)
            with cp1:
                st.text_input(f"Banque {i}", key=f"ban_p_{i}")
                st.selectbox(f"Type {i}", ["Amortissable", "In Fine"], key=f"typ_p_{i}")
            with cp2:
                crdu = st.number_input(f"Restant Dû (€) {i}", key=f"crdu_p_{i}")
                total_passif += crdu
            with cp3:
                m_mens = st.number_input(f"Mensualité (€) {i}", key=f"mens_p_{i}")
                mensualites_totales += m_mens

with tab_p2:
    nb_p_conso = st.number_input("Nombre d'autres crédits", min_value=0, key="nb_p_conso")
    for j in range(int(nb_p_conso)):
        solde_d = st.number_input(f"Reste à payer (€) {j}", key=f"solde_c_{j}")
        total_passif += solde_d

# --- SECTION 11 : OBJECTIFS ---
st.markdown("---")
st.header("🎯 11. Objectifs & Priorités")
col_obj1, col_obj2 = st.columns(2)
with col_obj1:
    st.multiselect("Objectifs", ["Retraite", "Fiscalité", "Famille", "Transmission", "Revenus"], key="obj_multi")
with col_obj2:
    profil_r = st.select_slider("Risque", options=["Prudent", "Équilibré", "Dynamique", "Offensif"], key="profil_r")
    horizon = st.select_slider("Horizon", options=["Court", "Moyen", "Long"], key="horizon_p")

# --- SECTION 12 : RÉSUMÉ EXPERT (DÉBLOQUÉ PAR ADMINOCP) ---
if st.session_state.get('is_expert', False):
    st.sidebar.markdown("---")
    st.sidebar.title("📊 Synthèse Expert")
    pat_brut = total_brut_immo + total_brut_fin
    pat_net = pat_brut - total_passif
    capa_epargne = reste_vivre_brut - mensualites_totales

    st.sidebar.metric("PATRIMOINE NET", f"{pat_net:,.0f} €".replace(",", " "))
    st.sidebar.metric("ÉPARGNE/MOIS", f"{capa_epargne:,.0f} €")
    
    if st.button("🚀 GÉNÉRER LE BILAN"):
        st.balloons()
        st.header("📋 Diagnostic OCP")
        c_an1, c_an2 = st.columns(2)
        c_an1.metric("Poids Immo", f"{(total_brut_immo/pat_brut*100 if pat_brut>0 else 0):.1f}%")
        c_an2.metric("Endettement", f"{(mensualites_totales/(rev_mens_estim if rev_mens_estim>0 else 1)*100):.1f}%")

# --- FIN ---
if not st.session_state.get('is_expert', False):
    st.markdown("---")
    if st.button("📤 ENVOYER MON DOSSIER"):
        st.balloons()
        st.success("Informations transmises avec succès.")
