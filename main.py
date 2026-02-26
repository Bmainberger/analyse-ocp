import streamlit as st
from datetime import date

# Configuration de la page
st.set_page_config(page_title="OCP Patrimoine - Analyse Experte", page_icon="🛡️", layout="wide")

st.title("🛡️ OCP Patrimoine - Bilan et Analyse")
st.markdown("---")

# --- SECTION 1 : ÉTAT CIVIL ---
st.header("1. État Civil & Situation Familiale")
col1, col2 = st.columns(2)
with col1:
    nom_client = st.text_input("Nom du Client")
    prenom_client = st.text_input("Prénom du Client")
with col2:
    situation = st.selectbox("Situation Matrimoniale", ["Célibataire", "Marié(e)", "Pacsé(e)", "Divorcé(e)", "Veuf/Veuve"])
    nb_enfants = st.number_input("Nombre d'enfants à charge", min_value=0, max_value=15, step=1)

st.markdown("---")

# --- SECTIONS 3 & 4 : PATRIMOINE IMMOBILIER ---
st.header("3 & 4. Patrimoine Immobilier")
tab1, tab2 = st.tabs(["🏠 Immobilier Physique", "🏢 Pierre-Papier (SCPI, SCI, GFV...)"])

total_immo = 0.0

with tab1:
    nb_biens = st.number_input("Nombre de biens physiques", min_value=0)
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
            px_p = st.number_input(f"Prix de part (€) {j+1}", min_value=0.0, key=f"px_c_{j}")
            nb_p = st.number_input(f"Nombre de parts {j+1}", min_value=0.0, key=f"nb_c_{j}")
            val_retrait = px_p * nb_p
            st.number_input(f"Valeur de retrait (€) {j+1}", value=val_retrait, key=f"liq_c_{j}")
            total_immo += val_retrait

st.markdown("---")

# --- SECTION 5 : PATRIMOINE FINANCIER ---
st.header("5. Patrimoine Financier")
nb_fin = st.number_input("Nombre de contrats financiers", min_value=0)
total_fin = 0.0
for k in range(nb_fin):
    with st.expander(f"Contrat n°{k+1}", expanded=True):
        f1, f2, f3 = st.columns(3)
        with f1:
            t_f = st.selectbox("Type", 
                ["Livret A / LDD", "PEL / CEL", "Livret Boosté", "Assurance-Vie", "Contrat de Capi", "PER", "PERCO / PEE", "Madelin", "Article 83 / PERO", "PEA", "Compte-Titres"], 
                key=f"typ_f_{k}")
        with f2:
            m_f = st.number_input("Solde (€)", min_value=0.0, key=f"m_f_{k}")
            total_fin += m_f
        with f3:
            if t_f in ["Assurance-Vie", "PER", "Contrat de Capi", "Madelin"]:
                st.selectbox("Support", ["Mono-support (Fonds Euro)", "Multi-support"], key=f"gest_f_{k}")
            else:
                st.text_input("Établissement", key=f"etab_f_{k}")

st.markdown("---")

# --- SECTION 6 : PRÉVOYANCE (VERSION EXPERTE) ---
st.header("6. Prévoyance & Protection")
nb_prev = st.number_input("Nombre de contrats de prévoyance", min_value=0)
for p in range(nb_prev):
    with st.expander(f"Contrat Prévoyance n°{p+1}", expanded=True):
        p1, p2 = st.columns(2)
        with p1:
            cat_p = st.selectbox("Catégorie", 
                ["Garantie Décès", "Invalidité / Incapacité", "Arrêt de travail (IJ)", "Dépendance", "GAV", "Prévoyance TNS", "Assurance Emprunteur", "Contrat Collectif Entreprise"], 
                key=f"cat_p_{p}")
            st.text_input("Assureur", key=f"ass_p_{p}")
        with p2:
            st.number_input("Montant / Capital Garanti (€)", min_value=0.0, key=f"cap_p_{p}")
            st.number_input("Cotisation Annuelle (€)", min_value=0.0, key=f"cot_p_{p}")

        if cat_p == "Assurance Emprunteur":
            st.markdown("**Garanties Emprunteur :**")
            ge1, ge2, ge3 = st.columns(3)
            with ge1:
                st.number_input("Quotité (%)", min_value=0, max_value=100, value=100, key=f"quo_p_{p}")
                st.checkbox("Décès", value=True, key=f"dec_p_{p}")
            with ge2:
                st.checkbox("PTIA", value=True, key=f"ptia_p_{p}")
                st.checkbox("IPT / IPP", key=f"ipt_p_{p}")
            with ge3:
                st.checkbox("ITT", key=f"itt_p_{p}")
                st.checkbox("Perte d'emploi", key=f"pe_p_{p}")
        
        if cat_p in ["Garantie Décès", "Prévoyance TNS", "Contrat Collectif Entreprise"]:
             st.multiselect("Détails Rentes", ["Rente Éducation", "Rente Conjoint", "Rente Invalidité"], key=f"rent_p_{p}")

st.markdown("---")

# --- SECTION 8 : OBJECTIFS CLIENT ---
st.header("8. Objectifs du Client")
obj_col1, obj_col2 = st.columns(2)
with obj_col1:
    st.multiselect("Priorités", ["Retraite", "Fiscalité", "Transmission", "Protection Famille", "Études Enfants", "Épargne de précaution"])
with obj_col2:
    st.select_slider("Horizon", options=["Court terme", "Moyen terme", "Long terme"])

st.markdown("---")

# --- SECTION 9 : SYNTHÈSE ---
st.header("9. Synthèse")
p_total = total_immo + total_fin
c_syn1, c_syn2, c_syn3 = st.columns(3)
with c_syn1: st.metric("Immobilier", f"{total_immo:,.0f} €")
with c_syn2: st.metric("Financier", f"{total_fin:,.0f} €")
with c_syn3: st.metric("PATRIMOINE BRUT", f"{p_total:,.0f} €")

st.markdown("---")
st.success("Version Experte 1.0 - Prévoyance et Assurance-vie complétées !")
