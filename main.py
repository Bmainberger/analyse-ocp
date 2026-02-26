import streamlit as st
from datetime import date

# --- CONFIGURATION ET TITRE ---
st.set_page_config(page_title="OCP Patrimoine - Analyse", page_icon="🛡️", layout="wide")

st.title("🛡️ OCP Patrimoine - Bilan et Analyse")
st.markdown("---")

# --- SECTION 1 : ÉTAT CIVIL & FAMILLE ---
st.header("1. État Civil & Situation Familiale")
col1, col2 = st.columns(2)

with col1:
    st.subheader("👤 Client (Principal)")
    nom_client = st.text_input("Nom du Client")
    prenom_client = st.text_input("Prénom du Client")
    date_naissance = st.date_input("Date de naissance", value=date(1980, 1, 1), key="dn_c")
    nationalite = st.text_input("Nationalité", key="nat_c")

with col2:
    st.subheader("💍 Situation")
    situation = st.selectbox("Situation Matrimoniale", ["Célibataire", "Marié(e)", "Pacsé(e)", "Divorcé(e)", "Veuf/Veuve"])
    
    en_couple = situation in ["Marié(e)", "Pacsé(e)"]
    if en_couple:
        st.info("ℹ️ Informations du Conjoint")
        nom_conjoint = st.text_input("Nom du Conjoint")
        prenom_conjoint = st.text_input("Prénom du Conjoint")
        date_naissance_conj = st.date_input("Date de naissance Conjoint", value=date(1980, 1, 1), key="dn_conj")
    
    nb_enfants = st.number_input("Nombre d'enfants à charge", min_value=0, max_value=15, step=1)

st.markdown("---")

# --- SECTION 2 : COORDONNÉES ---
st.header("2. Coordonnées")
c_coo1, c_coo2, c_coo3 = st.columns([2, 1, 1])
with c_coo1:
    adresse = st.text_input("Adresse postale complète")
with c_coo2:
    telephone = st.text_input("Téléphone")
with c_coo3:
    email = st.text_input("Email")

st.markdown("---")

# --- SECTION 3 : PROFESSION & REVENUS ---
st.header("3. Situation Professionnelle & Revenus")

if en_couple:
    col_pro1, col_pro2 = st.columns(2)
    with col_pro1:
        st.subheader("💼 Client")
        st.selectbox("Statut (Client)", ["Salarié", "TNS", "Dirigeant", "Fonctionnaire", "Retraité", "Sans activité"], key="stat_c")
        st.text_input("Profession (Client)", key="prof_c")
        st.number_input("Revenu annuel net (Client) (€)", min_value=0, key="rev_c")
    with col_pro2:
        st.subheader("💼 Conjoint")
        st.selectbox("Statut (Conjoint)", ["Salarié", "TNS", "Dirigeant", "Fonctionnaire", "Retraité", "Sans activité"], key="stat_conj")
        st.text_input("Profession (Conjoint)", key="prof_conj")
        st.number_input("Revenu annuel net (Conjoint) (€)", min_value=0, key="rev_conj")
else:
    cp1, cp2 = st.columns(2)
    with cp1:
        st.selectbox("Statut Professionnel", ["Salarié", "TNS", "Dirigeant", "Fonctionnaire", "Retraité", "Sans activité"])
        st.text_input("Profession")
    with cp2:
        st.number_input("Revenu net annuel (€)", min_value=0)

st.write(" ")
st.subheader("📊 Autres revenus & TMI")
cf1, cf2, cf3 = st.columns(3)
with cf1:
    st.number_input("Revenus Fonciers nets (€)", min_value=0)
    st.number_input("Dividendes / Intérêts (€)", min_value=0)
with cf2:
    st.number_input("Pensions / Rentes perçues (€)", min_value=0)
    st.number_input("Autres revenus divers (€)", min_value=0)
with cf3:
    st.selectbox("Tranche Marginale d'Imposition (TMI)", ["0%", "11%", "30%", "41%", "45%"])

st.markdown("---")

# --- SECTION 4 & 5 : PATRIMOINE IMMOBILIER ---
st.header("4 & 5. Patrimoine Immobilier")
tab1, tab2 = st.tabs(["🏠 Immobilier Physique", "🏢 Pierre-Papier (SCPI, SCI...)"])

with tab1:
    nb_biens = st.number_input("Nombre de biens immobiliers physiques", min_value=0)
    for i in range(nb_biens):
        with st.expander(f"Bien n°{i+1}", expanded=True):
            st.selectbox(f"Type de bien {i+1}", ["Résidence Principale", "Résidence Secondaire", "Investissement Locatif"], key=f"type_i_{i}")
            st.number_input(f"Valeur vénale (€) {i+1}", min_value=0, key=f"val_i_{i}")

with tab2:
    nb_coll = st.number_input("Nombre de placements collectifs", min_value=0)
    for j in range(nb_coll):
        with st.expander(f"Placement n°{j+1}", expanded=True):
            st.selectbox(f"Type", ["SCPI", "SCI", "OPCI", "GFV"], key=f"type_c_{j}")
            st.text_input("Nom du support", key=f"nom_c_{j}")
            st.number_input("Valeur estimée (€)", min_value=0, key=f"val_c_{j}")

st.markdown("---")
st.success("Application mise à jour !")
