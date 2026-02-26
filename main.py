import streamlit as st
from datetime import date

# 1. CONFIGURATION ET TITRE
st.set_page_config(page_title="OCP Patrimoine - Analyse", page_icon="🛡️", layout="wide")

st.title("🛡️ OCP Patrimoine - Bilan et Analyse")
st.markdown("---")

# 2. SECTION 1 : ÉTAT CIVIL & US PERSON
st.header("1. État Civil & Situation Familiale")
col1, col2 = st.columns(2)

with col1:
    st.subheader("👤 Client (Principal)")
    nom_client = st.text_input("Nom du Client")
    prenom_client = st.text_input("Prénom du Client")
    
    # Alerte US Person Client
    us_person_c = st.checkbox("🇺🇸 Citoyen Américain / US Person (Client)")
    if us_person_c:
        st.warning("⚠️ **Vigilance US Person :** Soumis à la convention franco-américaine. Vérifiez l'éligibilité des supports (PEA/Assurance-Vie) et les obligations FATCA.")
    
    date_naissance = st.date_input("Date de naissance", value=date(1980, 1, 1), key="dn_c")
    nationalite = st.text_input("Nationalité", key="nat_c")

with col2:
    st.subheader("💍 Situation")
    situation = st.selectbox("Situation Matrimoniale", ["Célibataire", "Marié(e)", "Pacsé(e)", "Divorcé(e)", "Veuf/Veuve"])
    
    en_couple = situation in ["Marié(e)", "Pacsé(e)"]
    if en_couple:
        st.info("ℹ️ Informations du Conjoint")
        nom_conjoint = st.text_input("Nom du Conjoint")
        
        # Alerte US Person Conjoint
        us_person_conj = st.checkbox("🇺🇸 Citoyen Américain / US Person (Conjoint)")
        if us_person_conj:
            st.warning("⚠️ **Vigilance Conjoint :** Citoyen US. Vérifiez l'impact sur l'imposition commune du foyer.")
            
        date_naissance_conj = st.date_input("Date de naissance Conjoint", value=date(1980, 1, 1), key="dn_conj")
    
    nb_enfants = st.number_input("Nombre d'enfants à charge", min_value=0, max_value=15, step=1)

st.markdown("---")

# 3. SECTION PROFESSION & REVENUS (DÉTAILLÉS)
st.header("3. Situation Professionnelle & Revenus")

if en_couple:
    col_pro1, col_pro2 = st.columns(2)
    with col_pro1:
        st.subheader("💼 Client")
        st.selectbox("Statut (Client)", ["Salarié", "TNS", "Dirigeant", "Fonctionnaire", "Retraité"], key="stat_c")
        st.number_input("Salaire / BNC / BIC annuel net (€)", min_value=0, key="rev_c")
    with col_pro2:
        st.subheader("💼 Conjoint")
        st.selectbox("Statut (Conjoint)", ["Salarié", "TNS", "Dirigeant", "Fonctionnaire", "Retraité"], key="stat_conj")
        st.number_input("Salaire / BNC / BIC annuel net (€)", min_value=0, key="rev_conj")
else:
    c1, c2 = st.columns(2)
    with c1:
        st.selectbox("Statut Professionnel", ["Salarié", "TNS", "Dirigeant", "Fonctionnaire", "Retraité"])
    with c2:
        st.number_input("Revenu net annuel (€)", min_value=0)

st.write(" ")
st.subheader("📊 Fiscalité & Autres revenus")
cf1, cf2, cf3 = st.columns(3)
with cf1:
    st.number_input("Revenus Fonciers nets (€)", min_value=0)
with cf2:
    st.number_input("Dividendes / Intérêts (€)", min_value=0)
with cf3:
    st.selectbox("TMI estimée", ["0%", "11%", "30%", "41%", "45%"])

st.markdown("---")

# 4. PATRIMOINE IMMOBILIER & FINANCIER (RÉSUMÉ)
st.header("4, 5 & 6. Actifs Patrimoniaux")
t1, t2 = st.tabs(["🏠 Immobilier", "💰 Financier"])

with t1:
    nb_biens = st.number_input("Nombre de biens", min_value=0)
    for i in range(nb_biens):
        st.text_input(f"Désignation du bien {i+1}")

with t2:
    nb_comptes = st.number_input("Nombre de contrats financiers", min_value=0)
    for j in range(nb_comptes):
        st.selectbox(f"Type de contrat {j+1}", ["Assurance-Vie", "PER", "PEA", "Livret"], key=f"typ_{j}")

st.markdown("---")
st.success("Configuration complète validée !")
