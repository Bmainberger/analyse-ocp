import streamlit as st
from datetime import date

# Configuration de la page
st.set_page_config(page_title="OCP Patrimoine - Analyse", page_icon="🛡️", layout="wide")

st.title("🛡️ OCP Patrimoine - Bilan et Analyse")
st.markdown("---")

# --- SECTION 1 : ÉTAT CIVIL ---
st.header("1. État Civil & Situation Familiale")
col1, col2 = st.columns(2)
with col1:
    nom_client = st.text_input("Nom du Client")
    prenom_client = st.text_input("Prénom du Client")
    date_naissance = st.date_input("Date de naissance", value=date(1980, 1, 1))
with col2:
    situation = st.selectbox("Situation Matrimoniale", ["Célibataire", "Marié(e)", "Pacsé(e)", "Divorcé(e)", "Veuf/Veuve"])
    nb_enfants = st.number_input("Nombre d'enfants à charge", min_value=0, max_value=15, step=1)

st.markdown("---")

# --- SECTIONS 3 & 4 : PATRIMOINE IMMOBILIER ---
st.header("3 & 4. Patrimoine Immobilier")
tab1, tab2 = st.tabs(["🏠 Immobilier Physique", "🏢 Pierre-Papier (SCPI, SCI, GFV...)"])

total_immo = 0.0

with tab1:
    nb_biens = st.number_input("Nombre de biens immobiliers physiques", min_value=0)
    for i in range(nb_biens):
        with st.expander(f"Bien n°{i+1}", expanded=True):
            c1, c2 = st.columns(2)
            with c1:
                st.selectbox(f"Type {i+1}", ["Résidence Principale", "Résidence Secondaire", "Appartement", "Maison", "Terrain", "Parking", "Immeuble"], key=f"type_i_{i}")
                val_i = st.number_input(f"Valeur vénale (€) {i+1}", min_value=0.0, key=f"val_i_{i}")
                total_immo += val_i
            with c2:
                st.selectbox(f"Régime fiscal {i+1}", ["Droit Commun", "LMNP", "LMP", "Pinel", "Malraux", "MH", "Denormandie"], key=f"fisc_i_{i}")

with tab2:
    nb_coll = st.number_input("Nombre de placements collectifs", min_value=0)
    for j in range(nb_coll):
        with st.expander(f"Placement Collectif n°{j+1}", expanded=True):
            px_p = st.number_input("Prix de part (€)", min_value=0.0, key=f"px_c_{j}")
            nb_p = st.number_input("Nombre de parts", min_value=0.0, key=f"nb_c_{j}")
            val_retrait = px_p * nb_p
            st.number_input("Valeur de retrait (€)", value=val_retrait, key=f"liq_c_{j}")
            total_immo += val_retrait

st.markdown("---")

# --- SECTION 5 : PATRIMOINE FINANCIER (AVEC PERCO, MADELIN...) ---
st.header("5. Patrimoine Financier")
nb_fin = st.number_input("Nombre de contrats financiers", min_value=0)
total_fin = 0.0
for k in range(nb_fin):
    with st.expander(f"Contrat n°{k+1}"):
        f1, f2, f3 = st.columns(3)
        with f1:
            t_f = st.selectbox("Type", 
                ["Livret", "Assurance-Vie", "Contrat de Capi", "PER", "PERCO / PEE", "Madelin", "Article 83 / PERO", "PEA", "Compte-Titres", "Crypto"], 
                key=f"typ_f_{k}")
        with f2:
            m_f = st.number_input("Solde (€)", min_value=0.0, key=f"m_f_{k}")
            total_fin += m_f
        with f3:
            st.text_input("Établissement", key=f"etab_f_{k}")

st.markdown("---")

# --- SECTION 6 & 7 : PRÉVOYANCE & SANTÉ ---
# (Gardé simplifié pour la clarté)
st.header("6 & 7. Prévoyance & Santé")
col_ps1, col_ps2 = st.columns(2)
with col_ps1:
    st.selectbox("Prévoyance principale", ["Décès", "Rente Éducation", "Rente Conjoint", "IJ", "Invalidité"])
with col_ps2:
    st.text_input("Mutuelle Santé")

st.markdown("---")

# --- SECTION 8 : OBJECTIFS CLIENT ---
st.header("8. Objectifs du Client")
obj_col1, obj_col2 = st.columns(2)
with obj_col1:
    st.multiselect("Priorités (plusieurs choix possibles)", 
        ["Préparer la retraite", "Réduire l'impôt (IR)", "Protéger la famille", "Transmettre un capital", "Financer les études des enfants", "Se constituer une épargne de précaution"])
with obj_col2:
    st.select_slider("Horizon de placement", options=["Court terme (0-2 ans)", "Moyen terme (2-8 ans)", "Long terme (8 ans +)"])

st.markdown("---")

# --- SECTION 9 : SYNTHÈSE GLOBALE ---
st.header("9. Synthèse du Patrimoine")
patrimoine_total = total_immo + total_fin

col_syn1, col_syn2, col_syn3 = st.columns(3)
with col_syn1:
    st.metric("Total Immobilier", f"{total_immo:,.0f} €".replace(",", " "))
with col_syn2:
    st.metric("Total Financier", f"{total_fin:,.0f} €".replace(",", " "))
with col_syn3:
    st.metric("PATRIMOINE BRUT", f"{patrimoine_total:,.0f} €".replace(",", " "))

if patrimoine_total > 0:
    st.progress(total_immo / patrimoine_total, text=f"Répartition Immobilier ({ (total_immo/patrimoine_total)*100:.1f}%)")
    st.progress(total_fin / patrimoine_total, text=f"Répartition Financier ({ (total_fin/patrimoine_total)*100:.1f}%)")

st.markdown("---")
st.success("Structure complète (1-9) déployée avec calcul de synthèse !")
