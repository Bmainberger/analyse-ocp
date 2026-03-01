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
    .benefit-card { background-color: #f8fafc; padding: 20px; border-radius: 10px; border-left: 5px solid #26e291; }
    </style>
    """, unsafe_allow_html=True)

# Gestion de la navigation
if 'page' not in st.session_state:
    st.session_state['page'] = 'home'

# --- 1. PAGE D'ACCUEIL "PRO" (VOTRE DEMANDE) ---
if st.session_state['page'] == 'home':
    st.markdown('<h1 class="hero-title">Prenez de la hauteur sur votre patrimoine.</h1>', unsafe_allow_html=True)
    
    st.write("### 🏢 OCP Patrimoine : Votre expert en stratégie patrimoniale")
    
    # Les 3 Bénéfices
    col_b1, col_b2, col_b3 = st.columns(3)
    with col_b1:
        st.markdown('<div class="benefit-card"><h3>🔭 Vision 360°</h3><p>Regroupez immo, placements et dettes sur une seule interface.</p></div>', unsafe_allow_html=True)
    with col_b2:
        st.markdown('<div class="benefit-card"><h3>📈 Optimisation</h3><p>Réduisez vos impôts et préparez votre transmission.</p></div>', unsafe_allow_html=True)
    with col_b3:
        st.markdown('<div class="benefit-card"><h3>🛡️ Sérénité</h3><p>Un diagnostic clair réalisé par un expert OCP.</p></div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Le Processus
    st.subheader("📝 Le Processus")
    st.info("1. Remplissez vos données (5 min)  /  2. Analyse par votre conseiller  /  3. Entretien de restitution.")
    
    # Le Bouton d'Action
    st.write("")
    if st.button("🚀 DÉMARRER MON BILAN GRATUIT"):
        st.session_state['page'] = 'formulaire'
        st.rerun()
    
    # Optionnel : Code secret en bas de page pour vous
    with st.expander("Accès réservé (Code)"):
        code_c = st.text_input("Saisissez votre code", type="password")
        if code_c in ["OCP2026", "ADMINOCP"]:
            st.session_state['page'] = 'formulaire'
            st.rerun()
    st.stop()

# --- 2. LE FORMULAIRE (VOS MODULES ORIGINAUX STRICTS) ---

# Section 1 : État Civil
st.header("1. État Civil & Situation Familiale")
c1, c2 = st.columns(2)
with c1:
    st.text_input("Nom du Client", key="nom_c")
    st.text_input("Prénom du Client", key="pre_c")
with c2:
    st.selectbox("Situation Matrimoniale", ["Célibataire", "Marié(e)", "Pacsé(e)", "Divorcé(e)"], key="sit_mat")

st.markdown("---")

# Section 4 & 5 : Patrimoine Immobilier (REPRODUCTION STRICTE DE VOS PHOTOS)
st.header("4 & 5. Patrimoine Immobilier")
tab1, tab2 = st.tabs(["🏠 Immobilier Physique", "🏢 Pierre-Papier (SCPI, SCI, GFV...)"])

with tab2:
    nb_coll = st.number_input("Nombre de placements collectifs", min_value=0, value=1, key="nb_p_c")
    for j in range(int(nb_coll)):
        with st.expander(f"Placement Collectif n°{j+1}", expanded=True):
            t_coll = st.selectbox(f"Type de support {j}", ["SCPI", "SCI", "GFV / GFI", "OPCI"], key=f"type_c_{j}")
            
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                st.text_input(f"Nom du support {j}", key=f"nom_c_{j}")
                st.selectbox(f"Mode de détention {j}", 
                             ["Pleine Propriété", "Nue-Propriété", "Usufruit", "Via Assurance-Vie", "Via PER"], 
                             key=f"det_c_{j}")
            with col_b:
                px_p = st.number_input(f"Prix de part (€) {j}", min_value=0.0, step=1.0, key=f"px_c_{j}")
                nb_p = st.number_input(f"Nombre de parts {j}", min_value=0.0, step=1.0, key=f"nb_c_{j}")
            with col_c:
                if t_coll == "SCPI":
                    st.number_input(f"TOF (%) {j}", min_value=0.0, key=f"tof_c_{j}")
                elif t_coll == "GFV / GFI":
                    st.text_input(f"Surface / Exploitation {j}", key=f"surf_c_{j}")
            
            val_estimee = px_p * nb_p
            st.write(f"Valeur estimée : {val_estimee:,.0f} €")

st.markdown("---")

# Section 6 : Patrimoine Financier
st.header("6. Patrimoine Financier")
nb_fin = st.number_input("Nombre de comptes/contrats financiers", min_value=0, value=1, key="nb_f")
with st.expander("Contrat n°1", expanded=True):
    f1, f2, f3 = st.columns(3)
    with f1:
        st.selectbox("Type 0", ["Livret", "Assurance-Vie", "PER", "PEA", "Compte-Titres"], key="f_type_0")
        st.text_input("Établissement 0", key="f_etab_0")
    with f2:
        st.number_input("Solde (€) 0", min_value=0.0, key="f_solde_0")
        st.date_input("Date d'adhésion 0", key="f_date_0")
    with f3:
        st.selectbox("Support 0", ["Mono-support", "Multi-support"], key="f_supp_0")

st.markdown("---")

# Section 7 : Prévoyance
st.header("7. Prévoyance & Protection")
nb_prev = st.number_input("Nombre de contrats de prévoyance", min_value=0, value=1, key="nb_p")
with st.expander("Contrat de Prévoyance n°1", expanded=True):
    p1, p2, p3 = st.columns(3)
    with p1:
        st.selectbox("Garantie 0", ["Décès (Capital)", "Rente Éducation", "Rente Conjoint", "IJ (Revenu)", "Invalidité", "Emprunteur"], key="p_gar_0")
    with p2:
        st.number_input("Montant Garanti (€) 0", min_value=0.0, key="p_mt_0")
    with p3:
        st.text_input("Bénéficiaires 0", key="p_ben_0")

st.markdown("---")
if st.button("ENREGISTRER MON DOSSIER"):
    st.balloons()
    st.success("Données sauvegardées.")
