import streamlit as st
from datetime import date
import pandas as pd

# --- 1. CONFIGURATION & STYLE ---
st.set_page_config(page_title="OCP Big Expert", page_icon="📈", layout="wide")

# Masquage du lien et style du bouton (Visuel propre garanti)
st.markdown("""
    <style>
    div.stButton > button:first-child {
        background-color: #1d2e4d;
        color: white;
        font-size: 20px;
        font-weight: bold;
        width: 100%;
        border-radius: 8px;
        border: none;
        height: 3em;
    }
    .reportview-container .main .block-container { padding-top: 1rem; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. RÉCUPÉRATION DES DONNÉES (LIEN MAGIQUE) ---
query_params = st.query_params
init_nom = query_params.get("nom", "")
init_prenom = query_params.get("prenom", "")
init_rev = float(query_params.get("rev", 0.0))
init_immo = float(query_params.get("immo", 0.0))
init_fin = float(query_params.get("fin", 0.0))
init_dettes = float(query_params.get("dettes", 0.0))

# --- 3. GESTION ACCÈS EXPERT ---
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

# --- 4. LE FORMULAIRE (MODULES 1 À 11) ---
st.title("Votre Stratégie Patrimoniale OCP")

# Section 1 : État Civil
st.header("1. État Civil")
col1, col2 = st.columns(2)
with col1:
    nom_client = st.text_input("Nom du Client", value=init_nom, key="nom_c")
    prenom_client = st.text_input("Prénom du Client", value=init_prenom, key="pre_c")
with col2:
    situation = st.selectbox("Situation Matrimoniale", ["Célibataire", "Marié(e)", "Pacsé(e)", "Divorcé(e)", "Veuf/Veuve"], key="sit_mat")
    nb_enfants = st.number_input("Nombre d'enfants", min_value=0, value=0, key="nb_e")

# Section 3 : Revenus
st.markdown("---")
st.header("3. Revenus & Fiscalité")
c1, c2, c3 = st.columns(3)
with c1:
    rev_annuel = st.number_input("Revenu net annuel (€)", value=init_rev, key="rev_a")
with c2:
    tmi_c = st.selectbox("TMI", ["0%", "11%", "30%", "41%", "45%"], key="tmi_c")
with c3:
    epargne_mens = st.number_input("Capacité d'épargne mensuelle (€)", min_value=0, key="ep_m")

# Section 4 & 5 : Patrimoine
st.markdown("---")
st.header("4 & 5. Patrimoine")
t1, t2, t3 = st.tabs(["🏠 Immobilier", "💰 Financier", "📉 Dettes"])
with t1:
    val_immo = st.number_input("Valeur totale Immobilier (€)", value=init_immo, key="val_im")
with t2:
    val_fin = st.number_input("Valeur totale Placements (€)", value=init_fin, key="val_fi")
with t3:
    val_dettes = st.number_input("Total des Dettes (€)", value=init_dettes, key="val_de")

# Section 11 : Objectifs
st.markdown("---")
st.header("🎯 11. Objectifs & Priorités")
col_obj1, col_obj2 = st.columns(2)
with col_obj1:
    obj_multi = st.multiselect("Objectifs principaux ?", ["Retraite", "Fiscalité", "Famille", "Transmission", "Immobilier"], key="obj_m")
with col_obj2:
    horizon = st.select_slider("Horizon", options=["Court", "Moyen", "Long", "Transmission"], key="horiz")

# --- 5. SYNTHÈSE EXPERT (VISIBLE UNIQUEMENT EN MODE ADMIN) ---
if st.session_state.get('is_expert', False):
    st.markdown("---")
    st.header("📊 Analyse Big Expert OCP")
    
    pat_brut = val_immo + val_fin
    pat_net = pat_brut - val_dettes
    
    m1, m2, m3 = st.columns(3)
    m1.metric("PATRIMOINE NET", f"{pat_net:,.0f} €".replace(",", " "))
    m2.metric("ENDETTEMENT", f"{(val_dettes/pat_brut*100) if pat_brut > 0 else 0:.1f} %")
    m3.metric("REVENU ANNUEL", f"{rev_annuel:,.0f} €")

    if st.button("🚀 GÉNÉRER LE RÉSUMÉ DU BILAN"):
        st.balloons()
        st.subheader("📋 Diagnostic OCP")
        st.write(f"Analyse pour {prenom_client} {nom_client}")
        st.info(f"Le patrimoine est composé à { (val_immo/pat_brut*100) if pat_brut > 0 else 0:.0f}% d'immobilier.")

# --- 6. SECTION ENVOI (CLIENT) ---
if not st.session_state.get('is_expert', False):
    st.markdown("---")
    # Construction du lien magique (totalement invisible sur l'écran)
    base_url = "https://analyse.ocp-patrimoine.com/?"
    lien_auto = f"{base_url}nom={nom_client}&prenom={prenom_client}&rev={rev_annuel}&immo={val_immo}&fin={val_fin}&dettes={val_dettes}"
    
    corps_mail = f"DOSSIER : {prenom_client} {nom_client} \n\nLIEN EXPERT : <{lien_auto}>"

    # Le bouton HTML (Pas d'affichage de texte au-dessus)
    bouton_html = f"""
        <form action='https://formsubmit.co/bmainberger@ocp-patrimoine.com' method='POST'>
            <input type='hidden' name='_subject' value='Nouveau Bilan OCP : {nom_client}'>
            <input type='hidden' name='_captcha' value='false'>
            <input type='hidden' name='DOSSIER_COMPLET' value='{corps_mail}'>
            <button type='submit' style='background-color: #1d2e4d; color: white; padding: 20px; font-size: 18px; border-radius: 8px; width: 100%; border: none; cursor: pointer; font-weight: bold;'>
                🚀 TRANSMETTRE MON ÉTUDE
            </button>
        </form>
    """
    st.markdown(bouton_html, unsafe_allow_html=True)
