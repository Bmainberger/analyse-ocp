import streamlit as st
from datetime import date
import json

# 1. Configuration Style "SaaS"
st.set_page_config(page_title="OCP Patrimoine - Audit Digital", page_icon="📈", layout="wide")

# --- CSS PERSONNALISÉ (STYLE HARVEST) ---
st.markdown("""
    <style>
    .main { background-color: #ffffff; }
    div.stButton > button {
        background-color: #0047AB;
        color: white;
        border-radius: 8px;
        padding: 0.6em 2em;
        font-weight: bold;
        border: none;
        transition: 0.3s;
    }
    div.stButton > button:hover {
        background-color: #002d6d;
        color: white;
    }
    .hero-title { font-size: 3.5rem; font-weight: 800; color: #1a2b49; line-height: 1.1; }
    .hero-sub { font-size: 1.4rem; color: #556172; margin-top: 20px; margin-bottom: 30px; }
    .feature-box { padding: 20px; border-radius: 10px; background-color: #f1f5f9; border-left: 5px solid #0047AB; }
    </style>
    """, unsafe_allow_html=True)

# --- GESTION DE LA NAVIGATION ---
if 'page' not in st.session_state:
    st.session_state['page'] = 'home'
if 'is_expert' not in st.session_state:
    st.session_state['is_expert'] = False
if 'data' not in st.session_state:
    st.session_state['data'] = {}

def g(key, default=""):
    return st.session_state['data'].get(key, default)

# --- 1. PAGE D'ACCUEIL (LANDING PAGE) ---
if st.session_state['page'] == 'home':
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2 = st.columns([1.2, 1])
    
    with col1:
        st.markdown('<h1 class="hero-title">Votre stratégie <br><span style="color:#0047AB;">patrimoniale</span> commence ici.</h1>', unsafe_allow_html=True)
        st.markdown('<p class="hero-sub">Préparez votre audit privé avec OCP Patrimoine. Une approche digitale, sécurisée et exhaustive pour structurer votre avenir.</p>', unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-box">
        <strong>🚀 Bilan Express 360°</strong><br>
        Anticipez vos besoins en fiscalité, retraite et transmission via notre interface sécurisée.
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("DÉMARRER MON ANALYSE"):
            st.session_state['page'] = 'auth'
            st.rerun()
            
    with col2:
        st.image("https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&w=800", caption="Intelligence Patrimoniale OCP")

# --- 2. PAGE D'AUTHENTIFICATION ---
elif st.session_state['page'] == 'auth':
    st.markdown("<br><br>", unsafe_allow_html=True)
    c_auth, _ = st.columns([1, 1])
    with c_auth:
        st.subheader("🔐 Accès réservé")
        pwd = st.text_input("Veuillez saisir votre code d'accès confidentiel :", type="password")
        
        if st.button("Valider l'accès"):
            if pwd == "OCP2026":
                st.session_state['page'] = 'formulaire'
                st.session_state['is_expert'] = False
                st.rerun()
            elif pwd == "ADMINOCP": # VOTRE CODE SECRET À VOUS
                st.session_state['page'] = 'formulaire'
                st.session_state['is_expert'] = True
                st.rerun()
            else:
                st.error("Code d'accès non reconnu.")
        
        if st.button("← Retour"):
            st.session_state['page'] = 'home'
            st.rerun()

# --- 3. LE FORMULAIRE ---
elif st.session_state['page'] == 'formulaire':
    
    # ADMINISTRATION TOTALEMENT INVISIBLE POUR LE CLIENT
    if st.session_state['is_expert']:
        st.sidebar.title("🛠️ Console Expert OCP")
        uploaded_file = st.sidebar.file_uploader("📂 Charger un dossier client", type=["json"])
        if uploaded_file:
            st.session_state['data'] = json.load(uploaded_file)
            st.sidebar.success("Données chargées")
        
        # Bouton de déconnexion expert
        if st.sidebar.button("Quitter le mode Expert"):
            st.session_state['is_expert'] = False
            st.rerun()

    st.title("🛡️ Questionnaire de Préparation - OCP")
    
    # --- SECTIONS 1 À 11 ---
    st.header("1. État Civil")
    nom_c = st.text_input("Nom", value=g('nom_c'), key="nom_c")
    pre_c = st.text_input("Prénom", value=g('pre_c'), key="pre_c")
    # (Remettre ici tout le reste de vos sections 2 à 11)

    # --- SECTION 12 EXPERT (VISIBLE UNIQUEMENT SI VOUS AVEZ TAPÉ ADMINOCP) ---
    if st.session_state['is_expert']:
        st.markdown("---")
        st.header("🖋️ Analyse & Préconisations (Confidentiel)")
        st.text_area("Audit Successoral", value=g('audit_suc'), key="audit_suc", height=150)
        st.text_area("Analyse Fiscale", value=g('audit_fisc'), key="audit_fisc", height=150)
        st.text_area("Préconisations Stratégiques", value=g('strat'), key="strat", height=200)

    # --- PIED DE PAGE & SAUVEGARDE ---
    st.markdown("---")
    st.subheader("🏁 Fin de la saisie")
    st.write("Pour transmettre vos informations en toute sécurité, téléchargez le fichier ci-dessous.")
    
    # Exportation sans les données de session techniques
    final_fields = {k: v for k, v in st.session_state.items() if k not in ['page', 'data', 'is_expert']}
    
    st.download_button(
        label="📥 Terminer et Sauvegarder mon dossier",
        data=json.dumps(final_fields, default=str, indent=4),
        file_name=f"Dossier_OCP_{nom_c}.json",
        mime="application/json"
    )
