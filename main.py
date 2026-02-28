import streamlit as st
from datetime import date
import json

# 1. Configuration de la page
st.set_page_config(page_title="OCP Patrimoine - Audit & Stratégie", page_icon="🛡️", layout="wide")

# --- SYSTÈME DE MOT DE PASSE ---
def check_password():
    if "password_correct" not in st.session_state:
        st.title("🔐 Accès Questionnaire OCP")
        pwd = st.text_input("Veuillez saisir votre code d'accès confidentiel :", type="password")
        if st.button("Accéder au formulaire"):
            if pwd == "OCP2026": # Votre mot de passe client
                st.session_state["password_correct"] = True
                st.rerun()
            else:
                st.error("Code incorrect")
        return False
    return True

if check_password():
    # --- LOGIQUE DE MÉMOIRE ---
    if 'data' not in st.session_state:
        st.session_state['data'] = {}

    # --- BARRE LATÉRALE (ADMINISTRATION & EXPERT) ---
    st.sidebar.title("🛠️ Espace Administration")
    
    # Case à cocher pour vous (L'Expert)
    mode_expert = st.sidebar.checkbox("🔓 Activer le Mode Expert (Calculs & Notes)", value=False)
    
    # Chargement du fichier client
    uploaded_file = st.sidebar.file_uploader("Charger un dossier client (.json)", type=["json"])
    if uploaded_file is not None:
        st.session_state['data'] = json.load(uploaded_file)
        st.sidebar.success("✅ Dossier client chargé")

    def g(key, default=""):
        return st.session_state['data'].get(key, default)

    # --- EN-TÊTE CLIENT ---
    st.title("🛡️ OCP Patrimoine - Collecte d'informations")
    
    if not mode_expert:
        with st.expander("ℹ️ Instructions pour votre bilan", expanded=True):
            st.markdown("""
            **Bienvenue.** Ce formulaire permet de recueillir les informations pour votre bilan patrimonial. 
            **Confidentialité :** Vos données sont traitées uniquement sur votre navigateur. Aucune donnée n'est stockée sur nos serveurs.
            **Procédure :** Remplissez les sections ci-dessous, puis cliquez sur **'📥 Terminer et Sauvegarder'** tout en bas.
            """)

    st.markdown("---")

    # --- INITIALISATION CALCULS (EN ARRIÈRE-PLAN) ---
    total_brut_immo = 0.0
    total_brut_fin = 0.0
    total_passif = 0.0
    mensualites_totales = 0.0

    # --- SECTION 1 : ÉTAT CIVIL --- (CODE INCHANGÉ)
    st.header("1. État Civil & Famille")
    col1, col2 = st.columns(2)
    with col1:
        nom_c = st.text_input("Nom", value=g('nom_c'), key="nom_c")
        pre_c = st.text_input("Prénom", value=g('pre_c'), key="pre_c")
        d_n = g('dnaiss_c', "1980-01-01")
        dnaiss_c = st.date_input("Date de naissance", value=date.fromisoformat(d_n) if isinstance(d_n, str) else d_n, key="dnaiss_c")
        lieu_c = st.text_input("Lieu de naissance", value=g('lieu_c'), key="lieu_c")
        nat_c = st.text_input("Nationalité", value=g('nat_c'), key="nat_c") 
    with col2:
        sit_opts = ["Célibataire", "Marié(e)", "Pacsé(e)", "Divorcé(e)", "Veuf/Veuve"]
        sit_val = g('sit_mat', "Célibataire")
        sit_mat = st.selectbox("Situation Matrimoniale", sit_opts, index=sit_opts.index(sit_val), key="sit_mat")
        nb_e = st.number_input("Nombre d'enfants à charge", min_value=0, value=int(g('nb_e', 0)), key="nb_e")

    # (Ici vos sections 2 à 11 restent à l'identique dans votre code complet)
    # J'inclus les calculs automatiques pour qu'ils fonctionnent en Mode Expert
    
    # --- CALCULS FINAUX ---
    pat_net = total_brut_immo + total_brut_fin - total_passif

    # --- SECTION 12 : ANALYSE EXPERT (VISIBLE UNIQUEMENT SI MODE_EXPERT COCHÉ) ---
    if mode_expert:
        st.markdown("---")
        st.header("🖋️ 12. Analyse Expert & Préconisations (Confidentiel)")
        
        # Affichage des métriques pour votre travail
        res1, res2 = st.columns(2)
        res1.metric("PATRIMOINE NET CALCULÉ", f"{pat_net:,.0f} €")
        
        st.subheader("📝 Vos conclusions de Peer")
        
        # Champs de texte ajoutés sans modifier l'existant
        audit_successoral = st.text_area("🔍 Audit Successoral (Civil)", value=g('audit_suc'), key="audit_suc", height=150)
        analyse_fiscale = st.text_area("📉 Analyse Fiscale (IR / IFI)", value=g('audit_fisc'), key="audit_fisc", height=150)
        notes_rdv = st.text_area("📅 Notes de rendez-vous", value=g('notes_rdv'), key="notes_rdv", height=100)
        strategie_expert = st.text_area("🚀 Stratégie & Préconisations", value=g('strat_expert'), key="strat_expert", height=200)
        
        st.success("Ces analyses internes seront enregistrées dans le fichier de sauvegarde.")

    # --- BOUTON DE SAUVEGARDE FINAL (VISIBLE PAR TOUS) ---
    st.markdown("---")
    st.subheader("🏁 Fin de la saisie")
    
    # On capture tout le session_state pour que vos notes soient enregistrées
    all_fields = {k: v for k, v in st.session_state.items() if k not in ["password_correct", "data", "password"]}
    
    st.download_button(
        label="📥 Terminer et Sauvegarder mon dossier OCP",
        data=json.dumps(all_fields, default=str, indent=4),
        file_name=f"Dossier_OCP_{nom_c}.json",
        mime="application/json"
    )

st.caption("OCP Patrimoine - Outil d'Audit Professionnel 2026")
