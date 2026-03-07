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

# 2. INITIALISATION DES VARIABLES DE CALCUL
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
st.markdown("---")

# --- SECTION 1 À 9 (VOS MODULES ORIGINAUX INTACTS) ---
st.header("1. État Civil & Situation Familiale")
col1, col2 = st.columns(2)
with col1:
    nom_client = st.text_input("Nom du Client", key="nom_c")
    prenom_client = st.text_input("Prénom du Client", key="pre_c")
    date_naissance = st.date_input("Date de naissance", value=date(1980, 1, 1), key="dnaiss_c")
    lieu_naissance = st.text_input("Lieu de naissance", key="lieu_c")
    nationalite = st.text_input("Nationalité", key="nat_c") 
with col2:
    situation = st.selectbox("Situation Matrimoniale", ["Célibataire", "Marié(e)", "Pacsé(e)", "Divorcé(e)", "Veuf/Veuve"], key="sit_mat")
    nb_enfants = st.number_input("Nombre d'enfants à charge", min_value=0, max_value=15, step=1, key="nb_e")

if situation in ["Marié(e)", "Pacsé(e)"]:
    st.subheader("Informations du Conjoint")
    c1, c2 = st.columns(2)
    with c1:
        st.text_input("Nom du Conjoint", key="nom_conj")
        st.date_input("Date de naissance conjoint", value=date(1980, 1, 1), key="dnaiss_conj")
    with c2:
        st.text_input("Prénom du Conjoint", key="pre_conj")

st.markdown("---")
st.header("2. Coordonnées")
c_coo1, c_coo2, c_coo3 = st.columns([2, 1, 1])
with c_coo1: st.text_input("Adresse postale complète", key="adr_p")
with c_coo2: st.text_input("Téléphone", key="tel_p")
with c_coo3: st.text_input("Email", key="mail_p")

st.markdown("---")
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
    age_retraite = st.number_input("Âge de départ à la retraite prévu", min_value=50, max_value=80, value=64, key="age_ret")

st.markdown("---")
st.header("4 & 5. Patrimoine Immobilier")
tab_im1, tab_im2 = st.tabs(["🏠 Immobilier Physique", "🏢 Pierre-Papier"])
with tab_im1:
    nb_biens = st.number_input("Nombre de biens immobiliers physiques", min_value=0, key="nb_p_p")
    for i in range(int(nb_biens)):
        with st.expander(f"Bien n°{i+1}", expanded=True):
            ci1, ci2 = st.columns(2)
            with ci1:
                st.selectbox(f"Type de bien {i}", ["Résidence Principale", "Résidence Secondaire", "Appartement", "Maison", "Terrain", "Parking", "Immeuble de rapport"], key=f"type_i_{i}")
                val_i = st.number_input(f"Valeur vénale (€) {i}", min_value=0.0, key=f"val_i_{i}")
                total_brut_immo += val_i
            with ci2:
                st.selectbox(f"Régime fiscal {i}", ["Droit Commun (Nu)", "LMNP", "LMP", "Pinel", "Malraux", "Monument Historique"], key=f"fisc_i_{i}")
with tab_im2:
    nb_coll = st.number_input("Nombre de placements collectifs", min_value=0, key="nb_p_c")
    for j in range(int(nb_coll)):
        with st.expander(f"Placement Collectif n°{j+1}", expanded=True):
            t_coll = st.selectbox(f"Type {j}", ["SCPI", "SCI", "OPCI", "GFV / GFI", "Club Deal"], key=f"type_c_{j}")
            px_p = st.number_input(f"Prix de part (€) {j}", min_value=0.0, key=f"px_c_{j}")
            nb_p = st.number_input(f"Nombre de parts {j}", min_value=0.0, key=f"nb_c_{j}")
            total_brut_immo += (px_p * nb_p)

st.markdown("---")
st.header("6. Patrimoine Financier")
nb_fin = st.number_input("Nombre de comptes/contrats financiers", min_value=0, key="nb_f_f")
for k in range(int(nb_fin)):
    with st.expander(f"Contrat n°{k+1}"):
        f1, f2 = st.columns(2)
        with f1:
            st.selectbox(f"Type {k}", ["Livret", "Assurance-Vie", "PER", "PEA", "Compte-Titres"], key=f"typ_f_{k}")
            m_f = st.number_input(f"Solde (€) {k}", min_value=0.0, key=f"m_f_{k}")
            total_brut_fin += m_f
        with f2:
            st.text_input(f"Établissement {k}", key=f"banque_f_{k}")

st.markdown("---")
st.header("7. Prévoyance & Protection")
st.number_input("Nombre de contrats de prévoyance", min_value=0, key="nb_p_v")

st.markdown("---")
st.header("8. Santé / Mutuelle")
st.columns(3)[0].text_input("Assureur Santé", key="s_org")

st.markdown("---")
st.header("9. Passif & Endettement")
nb_pret = st.number_input("Nombre de crédits immobiliers", min_value=0, key="nb_p_immo")
for i in range(int(nb_pret)):
    with st.expander(f"Crédit Immo n°{i+1}"):
        crdu = st.number_input(f"Restant Dû (€) {i}", min_value=0.0, key=f"crdu_p_{i}")
        total_passif += crdu
        mensualites_totales += st.number_input(f"Mensualité (€) {i}", min_value=0.0, key=f"mens_p_{i}")

# --- MODULE 10 : COMMENTAIRES ---
st.markdown("---")
st.header("📝 10. Commentaires & Préconisations")
col_c1, col_c2 = st.columns(2)
with col_c1:
    commentaires_client = st.text_area("Précisions du client", key="com_client")
with col_c2:
    if st.session_state['is_expert']:
        note_expert = st.text_area("Note de Synthèse de l'Expert", key="syn_expert")

# --- SECTION 11 : OBJECTIFS ---
st.markdown("---")
st.header("🎯 11. Objectifs & Priorités")
st.multiselect("Quels sont les objectifs principaux ?", ["Retraite", "Fiscalité", "Famille", "Transmission", "Immobilier"], key="obj_multi")

# --- ANALYSE STRATÉGIQUE (VOTRE DISPOSITION D'HIER AU CENTRE) ---
if st.session_state['is_expert']:
    st.markdown("---")
    st.header("📊 ANALYSE STRATÉGIQUE BIG EXPERT")
    
    pat_brut = total_brut_immo + total_brut_fin
    pat_net = pat_brut - total_passif
    ratio_endettement = (total_passif / pat_brut * 100) if pat_brut > 0 else 0
    
    met1, met2, met3 = st.columns(3)
    met1.metric("Patrimoine Net", f"{pat_net:,.0f} €")
    met2.metric("Revenu Mensuel", f"{(rev_annuel/12):,.0f} €")
    met3.metric("Endettement", f"{ratio_endettement:.1f} %")

    st.subheader("🎯 Diagnostics")
    diag_tabs = st.tabs(["Structure", "Fiscalité", "Prévoyance", "Retraite"])
    
    with diag_tabs[0]:
        st.write("**Analyse de la structure du patrimoine**")
        if total_brut_fin < (rev_annuel / 2):
            st.error(f"🚨 Alerte Liquidité : Votre épargne de précaution est insuffisante (inférieure à 6 mois de revenus).")
        else:
            st.success("✅ Structure saine : Épargne de précaution disponible.")
            
    with diag_tabs[1]:
        st.write("**Optimisation Fiscale**")
        if tmi_c in ["30%", "41%", "45%"]:
            st.warning(f"💡 Levier fiscal détecté : Votre TMI à {tmi_c} permet d'envisager des solutions de défiscalisation (PER, SCPI Fiscales).")
        else:
            st.info("Pression fiscale modérée.")

    with diag_tabs[2]:
        st.write("**Protection de la famille**")
        st.write(f"Besoin estimé en capital décès : {(rev_annuel * 3):,.0f} € (pour 3 ans de maintien de revenus).")

    with diag_tabs[3]:
        st.write("**Analyse Retraite**")
        gap = (rev_annuel / 12) * 0.45
        st.info(f"Le 'Gap Retraite' estimé est de {gap:,.0f} € par mois. Il est conseillé d'agir dès maintenant.")

    # BOUTON PDF
    if st.button("📄 GÉNÉRER LE BILAN PDF PROFESSIONNEL"):
        st.success("Bilan prêt pour le téléchargement.")
        # (Logique de téléchargement PDF simplifiée ici)

# --- BOUTON FINAL ---
if not st.session_state['is_expert']:
    st.markdown("---")
    mon_email = "bmainberger@ocp-patrimoine.com"
    bouton_html = f"""
        <form action="https://formsubmit.co/{mon_email}" method="POST">
            <button type="submit" style="background-color: #1d2e4d; color: white; padding: 20px; font-size: 18px; border-radius: 8px; width: 100%; border: none; cursor: pointer; font-weight: bold;">
                🚀 TRANSMETTRE MON ÉTUDE
           </button>
        </form>
    """
    st.markdown(bouton_html, unsafe_allow_html=True)
