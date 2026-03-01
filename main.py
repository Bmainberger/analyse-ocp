import streamlit as st
from datetime import date

# 1. CONFIGURATION ET STYLE
st.set_page_config(page_title="OCP Patrimoine", page_icon="🛡️", layout="wide")

st.markdown("""
    <style>
    div.stButton > button {
        background-color: #26e291; color: #1a2b49; border-radius: 8px;
        padding: 0.7em 2.5em; font-weight: bold; border: none;
    }
    .hero-title { font-size: 3rem; font-weight: 800; color: #1a2b49; }
    .benefit-card { background-color: #f8fafc; padding: 20px; border-radius: 10px; border-left: 5px solid #26e291; height: 100%; }
    </style>
    """, unsafe_allow_html=True)

# Navigation
if 'page' not in st.session_state:
    st.session_state['page'] = 'home'

# --- 1. PAGE D'ACCUEIL PRO ---
if st.session_state['page'] == 'home':
    st.markdown('<h1 class="hero-title">Prenez de la hauteur sur votre patrimoine.</h1>', unsafe_allow_html=True)
    
    col_b1, col_b2, col_b3 = st.columns(3)
    with col_b1:
        st.markdown('<div class="benefit-card"><h3>🔭 Vision 360°</h3><p>Regroupez immo, placements et dettes sur une seule interface.</p></div>', unsafe_allow_html=True)
    with col_b2:
        st.markdown('<div class="benefit-card"><h3>📈 Optimisation</h3><p>Réduisez vos impôts et préparez votre transmission.</p></div>', unsafe_allow_html=True)
    with col_b3:
        st.markdown('<div class="benefit-card"><h3>🛡️ Sérénité</h3><p>Un diagnostic clair réalisé par un expert OCP.</p></div>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.subheader("📝 Le Processus")
    st.write("**1. Remplissez vos données (5 min) / 2. Analyse par votre conseiller / 3. Entretien de restitution.**")
    
    st.write("")
    if st.button("🚀 DÉMARRER MON BILAN GRATUIT"):
        st.session_state['page'] = 'formulaire'
        st.rerun()
    st.stop()

# --- 2. LE FORMULAIRE COMPLET (RETOUR À VOTRE CODE ORIGINAL) ---

# SECTION 1 & 2 & 3 (État Civil, Coordonnées, Profession)
st.header("1. État Civil & Famille")
c1, c2 = st.columns(2)
with c1:
    st.text_input("Nom du Client", key="nom_c")
    st.text_input("Prénom du Client", key="pre_c")
    st.date_input("Date de naissance", value=date(1980, 1, 1), key="dnaiss_c")
with c2:
    st.selectbox("Situation Matrimoniale", ["Célibataire", "Marié(e)", "Pacsé(e)", "Divorcé(e)", "Veuf/Veuve"], key="sit_mat")
    st.number_input("Nombre d'enfants à charge", min_value=0, step=1, key="nb_e")

st.header("2. Coordonnées")
cc1, cc2 = st.columns([2, 1])
cc1.text_input("Adresse postale complète", key="adr_p")
cc2.text_input("Téléphone", key="tel_p")

st.header("3. Situation Professionnelle")
cp1, cp2 = st.columns(2)
cp1.selectbox("Statut", ["Salarié", "TNS / Libéral", "Dirigeant", "Retraité"], key="statut_pro")
cp2.number_input("Revenu net annuel (€)", min_value=0.0, key="rev_a")

st.markdown("---")

# SECTIONS 4 & 5 : IMMOBILIER
st.header("4 & 5. Patrimoine Immobilier")
tab1, tab2 = st.tabs(["🏠 Physique", "🏢 Pierre-Papier"])
with tab2:
    nb_coll = st.number_input("Nombre de placements collectifs", min_value=0, value=1, key="nb_p_c")
    for j in range(int(nb_coll)):
        with st.expander(f"Placement Collectif n°{j+1}", expanded=True):
            t_coll = st.selectbox(f"Type de support {j}", ["SCPI", "SCI", "GFV / GFI", "OPCI"], key=f"type_c_{j}")
            ca, cb, cc = st.columns(3)
            with ca:
                st.text_input(f"Nom du support {j}", key=f"nom_c_{j}")
                st.selectbox(f"Mode de détention {j}", ["Pleine Propriété", "Nue-Propriété", "Usufruit", "Via Assurance-Vie", "Via PER"], key=f"det_c_{j}")
            with cb:
                px_p = st.number_input(f"Prix de part (€) {j}", min_value=0.0, key=f"px_c_{j}")
                nb_p = st.number_input(f"Nombre de parts {j}", min_value=0.0, key=f"nb_c_{j}")
            with cc:
                if t_coll == "SCPI": st.number_input(f"TOF (%) {j}", key=f"tof_c_{j}")
                elif t_coll == "GFV / GFI": st.text_input(f"Surface / Exploitation {j}", key=f"surf_c_{j}")
            st.write(f"Valeur estimée : {px_p * nb_p:,.0f} €")

# SECTION 6 : FINANCIER
st.header("6. Patrimoine Financier")
st.number_input("Nombre de contrats financiers", min_value=0, value=1, key="nb_f")

# SECTION 7 : PRÉVOYANCE
st.header("7. Prévoyance & Protection")
st.number_input("Nombre de contrats de prévoyance", min_value=0, value=1, key="nb_p_prev")

# --- SECTION 8 : SANTÉ / MUTUELLE (RÉTABLIE) ---
st.header("8. Santé / Mutuelle")
with st.expander("Détails de la Couverture Santé", expanded=True):
    s1, s2, s3 = st.columns(3)
    with s1:
        st.text_input("Organisme / Assureur", key="s_org")
        st.selectbox("Type de contrat", ["Individuel", "Collectif (Entreprise)", "Madelin (TNS)"], key="s_type")
    with s2:
        st.number_input("Cotisation mensuelle (€)", min_value=0.0, key="s_cot")
        st.select_slider("Niveau de garantie", options=["Éco", "Standard", "Renforcé", "Frais Réels"], key="s_niv")
    with s3:
        st.multiselect("Personnes couvertes", ["Client", "Conjoint", "Enfant(s)"], key="s_couv")

# SECTION 9 : PASSIF
st.header("9. Passif & Endettement")
st.number_input("Nombre de crédits", min_value=0, value=0, key="nb_cred")

st.markdown("---")
if st.button("ENREGISTRER LE DOSSIER"):
    st.balloons()
    st.success("Données enregistrées.")
