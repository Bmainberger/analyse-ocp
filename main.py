import streamlit as st
from datetime import date
import json

# 1. Configuration Style "SaaS" Premium
st.set_page_config(page_title="OCP Patrimoine - Audit Digital", page_icon="📈", layout="wide")

# --- STYLE CSS (LOOK HARVEST / KWIPER) ---
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
        width: auto;
    }
    .hero-title { font-size: 3.2rem; font-weight: 800; color: #1a2b49; line-height: 1.2; }
    .hero-sub { font-size: 1.3rem; color: #556172; margin-bottom: 30px; }
    .feature-box { padding: 20px; border-radius: 10px; background-color: #f1f5f9; border-left: 5px solid #0047AB; margin-bottom: 20px; }
    h2 { color: #0047AB; border-bottom: 2px solid #f1f5f9; padding-bottom: 10px; margin-top: 40px; }
    </style>
    """, unsafe_allow_html=True)

# --- INITIALISATION DES VARIABLES ---
if 'page' not in st.session_state: st.session_state['page'] = 'home'
if 'is_expert' not in st.session_state: st.session_state['is_expert'] = False
if 'data' not in st.session_state: st.session_state['data'] = {}

def g(key, default=""):
    return st.session_state['data'].get(key, default)

# --- 1. PAGE D'ACCUEIL (LANDING PAGE) ---
if st.session_state['page'] == 'home':
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2 = st.columns([1.2, 1])
    with col1:
        st.markdown('<h1 class="hero-title">Votre stratégie <br><span style="color:#0047AB;">patrimoniale</span> commence ici.</h1>', unsafe_allow_html=True)
        st.markdown('<p class="hero-sub">Réalisez votre pré-audit confidentiel avec OCP Patrimoine. Une approche digitale pour structurer votre avenir sereinement.</p>', unsafe_allow_html=True)
        st.markdown('<div class="feature-box"><strong>🚀 Audit Express 360°</strong><br>Anticipez vos besoins en fiscalité, retraite et transmission via notre interface sécurisée.</div>', unsafe_allow_html=True)
        if st.button("DÉMARRER MON ANALYSE"):
            st.session_state['page'] = 'auth'
            st.rerun()
    with col2:
        st.image("https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&w=800")

# --- 2. PAGE D'AUTHENTIFICATION ---
elif st.session_state['page'] == 'auth':
    st.markdown("<br><br>", unsafe_allow_html=True)
    c_auth, _ = st.columns([1, 1])
    with c_auth:
        st.subheader("🔐 Accès réservé")
        pwd = st.text_input("Veuillez saisir votre code d'accès confidentiel :", type="password")
        if st.button("Valider l'accès"):
            if pwd == "OCP2026": # Code Client
                st.session_state['page'] = 'formulaire'
                st.session_state['is_expert'] = False
                st.rerun()
            elif pwd == "ADMINOCP": # VOTRE Code Expert
                st.session_state['page'] = 'formulaire'
                st.session_state['is_expert'] = True
                st.rerun()
            else: st.error("Code d'accès non reconnu.")
        if st.button("← Retour"):
            st.session_state['page'] = 'home'
            st.rerun()

# --- 3. LE FORMULAIRE COMPLET ---
elif st.session_state['page'] == 'formulaire':
    
    # Barre latérale (INVISIBLE POUR LE CLIENT)
    if st.session_state['is_expert']:
        st.sidebar.title("🛠️ Console Expert OCP")
        uploaded_file = st.sidebar.file_uploader("📂 Charger un dossier client", type=["json"])
        if uploaded_file:
            st.session_state['data'] = json.load(uploaded_file)
            st.sidebar.success("Données chargées")
        if st.sidebar.button("Quitter le mode Expert"):
            st.session_state['is_expert'] = False
            st.rerun()

    st.title("🛡️ Questionnaire de Préparation - OCP")
    
    # INITIALISATION CALCULS
    total_brut_immo, total_brut_fin, total_passif, mens_totales = 0.0, 0.0, 0.0, 0.0

    # SECTIONS
    st.header("1. État Civil & Famille")
    c1, c2 = st.columns(2)
    with c1:
        nom_c = st.text_input("Nom", value=g('nom_c'), key="nom_c")
        pre_c = st.text_input("Prénom", value=g('pre_c'), key="pre_c")
        d_n = g('dnaiss_c', "1980-01-01")
        st.date_input("Date de naissance", value=date.fromisoformat(d_n) if isinstance(d_n, str) else d_n, key="dnaiss_c")
    with c2:
        sit_opts = ["Célibataire", "Marié(e)", "Pacsé(e)", "Divorcé(e)", "Veuf/Veuve"]
        st.selectbox("Situation Matrimoniale", sit_opts, index=sit_opts.index(g('sit_mat', "Célibataire")), key="sit_mat")
        nb_e = st.number_input("Enfants à charge", min_value=0, value=int(g('nb_e', 0)), key="nb_e")

    st.header("2. Coordonnées")
    c_coo1, c_coo2 = st.columns(2)
    with c_coo1: st.text_input("Adresse postale", value=g('adr_p'), key="adr_p")
    with c_coo2: st.text_input("Email", value=g('mail_p'), key="mail_p")

    st.header("3. Profession & Revenus")
    cp1, cp2, cp3 = st.columns(3)
    with cp1: st.text_input("Profession", value=g('poste_pro'), key="poste_pro")
    with cp2: 
        rev_a = st.number_input("Revenu net annuel (€)", value=float(g('rev_a', 0.0)), key="rev_a")
        rev_f = st.number_input("Autres revenus (€)", value=float(g('rev_f', 0.0)), key="rev_f")
    with cp3: 
        st.selectbox("TMI", ["0%", "11%", "30%", "41%", "45%"], index=2, key="tmi_c")
        st.number_input("Âge retraite", value=int(g('age_ret', 64)), key="age_ret")

    st.header("3 bis. Budget Mensuel")
    cb1, cb2 = st.columns(2)
    with cb1: budget_vie = st.number_input("Train de vie mensuel (€)", value=float(g('budget_vie', 0.0)), key="budget_vie")
    with cb2: budget_impot = st.number_input("Impôts mensuels (€)", value=float(g('budget_impot', 0.0)), key="budget_impot")

    st.header("4 & 5. Patrimoine Immobilier")
    nb_immo = st.number_input("Nombre de biens immobiliers", min_value=0, value=int(g('nb_immo', 0)), key="nb_immo")
    for i in range(nb_immo):
        total_brut_immo += st.number_input(f"Valeur Bien {i+1} (€)", value=float(g(f"val_immo_{i}", 0.0)), key=f"val_immo_{i}")

    st.header("6. Patrimoine Financier")
    nb_fin = st.number_input("Nombre de comptes/contrats", min_value=0, value=int(g('nb_fin', 0)), key="nb_fin")
    for i in range(nb_fin):
        total_brut_fin += st.number_input(f"Solde Contrat {i+1} (€)", value=float(g(f"val_fin_{i}", 0.0)), key=f"val_fin_{i}")

    st.header("9. Passif (Dettes)")
    nb_det = st.number_input("Nombre de crédits en cours", min_value=0, value=int(g('nb_det', 0)), key="nb_det")
    for i in range(nb_det):
        total_passif += st.number_input(f"Restant dû Crédit {i+1} (€)", value=float(g(f"crdu_{i}", 0.0)), key=f"crdu_{i}")
        mens_totales += st.number_input(f"Mensualité Crédit {i+1} (€)", value=float(g(f"mens_{i}", 0.0)), key=f"mens_{i}")

    st.header("11. Objectifs & Priorités")
    st.multiselect("Quels sont vos objectifs ?", ["Retraite", "Fiscalité", "Protection", "Transmission", "Immobilier"], key="obj")

    # MODE EXPERT : ANALYSE INTERNE
    if st.session_state['is_expert']:
        st.markdown("---")
        st.header("🖋️ 12. Analyse Expert (Confidentiel)")
        pat_net = total_brut_immo + total_brut_fin - total_passif
        rev_m = (rev_a + rev_f) / 12
        flux_m = rev_m - (budget_vie + budget_impot + mens_totales)
        
        rex1, rex2 = st.columns(2)
        rex1.metric("PATRIMOINE NET", f"{pat_net:,.0f} €")
        rex2.metric("FLUX MENSUEL DISPO", f"{flux_m:,.0f} €")
        
        st.text_area("🔍 Audit Successoral", value=g('audit_suc'), key="audit_suc", height=100)
        st.text_area("📉 Analyse Fiscale", value=g('audit_fisc'), key="audit_fisc", height=100)
        st.text_area("🚀 Préconisations Stratégiques", value=g('strat'), key="strat", height=150)

    # SAUVEGARDE
    st.markdown("---")
    st.subheader("🏁 Terminer")
    st.write("Veuillez télécharger le fichier ci-dessous et le renvoyer à votre conseiller.")
    save_fields = {k: v for k, v in st.session_state.items() if k not in ['page', 'data', 'is_expert', 'password']}
    st.download_button(label="📥 Terminer et Sauvegarder", data=json.dumps(save_fields, default=str, indent=4),
                      file_name=f"Dossier_OCP_{nom_c}.json", mime="application/json")

st.caption("OCP Patrimoine 2026 - Outil de stratégie patrimoniale.")
