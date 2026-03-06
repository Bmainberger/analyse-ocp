import streamlit as st
from datetime import date
import pandas as pd

# --- CONFIGURATION ---
st.set_page_config(page_title="OCP Big Expert", page_icon="📈", layout="wide")

# Système de récupération URL
query_params = st.query_params
init_nom = query_params.get("nom", "")
init_prenom = query_params.get("prenom", "")
init_rev = float(query_params.get("rev", 0.0))
init_immo = float(query_params.get("immo", 0.0))
init_fin = float(query_params.get("fin", 0.0))
init_dettes = float(query_params.get("dettes", 0.0))

# Style Personnalisé
st.markdown("""
    <style>
    .stMetric { background-color: #f0f2f6; padding: 10px; border-radius: 10px; }
    div.stButton > button:first-child { background-color: #1d2e4d; color: white; width: 100%; height: 3em; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# Initialisation des compteurs
total_brut_immo = init_immo
total_brut_fin = init_fin
total_passif = init_dettes

# --- ACCÈS EXPERT ---
if 'is_expert' not in st.session_state:
    st.session_state['is_expert'] = False

with st.sidebar:
    st.image("https://www.ocp-patrimoine.com/wp-content/uploads/2021/03/Logo-OCP-Patrimoine-blanc.png", width=150)
    st.title("🔐 Espace Expert")
    code_admin = st.text_input("Code confidentiel", type="password")
    if code_admin == "ADMINOCP":
        st.session_state['is_expert'] = True
        st.success("Mode BIG EXPERT Activé")
    else:
        st.session_state['is_expert'] = False

# --- FORMULAIRE ---
st.title("Bilan Patrimonial Interactif")

# Section 1 : Civil
col1, col2 = st.columns(2)
with col1:
    nom_client = st.text_input("Nom", value=init_nom)
    prenom_client = st.text_input("Prénom", value=init_prenom)
with col2:
    situation = st.selectbox("Situation", ["Célibataire", "Marié(e)", "Pacsé(e)", "Divorcé(e)"])
    nb_enfants = st.number_input("Enfants", min_value=0, step=1)

# Section 2 : Revenus
st.header("Situation Financière")
c1, c2, c3 = st.columns(3)
with c1:
    rev_annuel = st.number_input("Revenu net annuel (€)", value=init_rev)
with c2:
    tmi = st.selectbox("TMI actuelle", ["0%", "11%", "30%", "41%", "45%"])
with c3:
    epargne_mens = st.number_input("Capacité d'épargne mensuelle (€)", min_value=0)

# Section 3 : Patrimoine (Ajout rapide)
st.header("Patrimoine existant")
tab_immo, tab_fin, tab_dettes = st.tabs(["🏠 Immobilier", "💰 Financier", "📉 Dettes"])
with tab_immo:
    val_rp = st.number_input("Valeur Résidence Principale (€)", min_value=0)
    val_locatif = st.number_input("Valeur Immobilier Locatif / SCPI (€)", min_value=0)
    total_brut_immo += (val_rp + val_locatif)
with tab_fin:
    val_livrets = st.number_input("Livrets / Cash (€)", min_value=0)
    val_assurance_vie = st.number_input("Assurance-vie / PEA / PER (€)", min_value=0)
    total_brut_fin += (val_livrets + val_assurance_vie)
with tab_dettes:
    crdu = st.number_input("Restant dû total des crédits (€)", value=init_dettes)
    total_passif = crdu

# --- ANALYSE EXPERT (LA PARTIE HARVEST) ---
if st.session_state.get('is_expert', False):
    st.markdown("---")
    st.header("📊 ANALYSE STRATÉGIQUE (BIG EXPERT)")
    
    pat_brut = total_brut_immo + total_brut_fin
    pat_net = pat_brut - total_passif
    
    # Métriques Clés
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Patrimoine Net", f"{pat_net:,.0f} €")
    m2.metric("Taux d'endettement", f"{(total_passif/pat_brut*100) if pat_brut > 0 else 0:.1f} %")
    m3.metric("Pression Fiscale", tmi)
    m4.metric("Indice de Liquidité", "Bon" if val_livrets > (rev_annuel/12)*6 else "Faible")

    # Graphiques de répartition
    col_chart1, col_chart2 = st.columns(2)
    with col_chart1:
        st.subheader("Répartition des Actifs")
        data = pd.DataFrame({
            'Catégorie': ['Immobilier', 'Financier'],
            'Valeur': [total_brut_immo, total_brut_fin]
        })
        st.bar_chart(data.set_index('Catégorie'))
        

    with col_chart2:
        st.subheader("Diagnostic Retraite")
        retraite_estimee = (rev_annuel / 12) * 0.55 # Estimation simplifiée
        st.warning(f"Baisse de revenu estimée à la retraite : -{ (rev_annuel/12) - retraite_estimee:,.0f} € / mois")
        

    # Recommandations
    st.subheader("📝 Préconisations de l'Expert")
    conseils = st.text_area("Saisissez vos conseils ici...", placeholder="Ex: Augmenter le levier immobilier, ouvrir un PER pour baisser la TMI...")

# --- BOUTON D'ENVOI (CLIENT) ---
if not st.session_state.get('is_expert', False):
    st.markdown("---")
    base_url = "https://analyse.ocp-patrimoine.com/?"
    # On génère le lien magique
    lien_auto = f"{base_url}nom={nom_client}&prenom={prenom_client}&rev={rev_annuel}&immo={total_brut_immo}&fin={total_brut_fin}&dettes={total_passif}"
    
    # Bouton Envoi
    corps_mail = f"NOUVEAU DOSSIER : {prenom_client} {nom_client} \n\nLIEN EXPERT : <{lien_auto}>"
    
    bouton_html = f"""
        <form action='https://formsubmit.co/bmainberger@ocp-patrimoine.com' method='POST'>
            <input type='hidden' name='_subject' value='Nouveau Bilan : {nom_client}'>
            <input type='hidden' name='DOSSIER' value='{corps_mail}'>
            <button type='submit'>🚀 TRANSMETTRE MON ÉTUDE</button>
        </form>
    """
    st.markdown(bouton_html, unsafe_allow_html=True)
