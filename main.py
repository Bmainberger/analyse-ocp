import streamlit as st
from datetime import date

# Configuration de la page
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
    lieu_naissance = st.text_input("Lieu de naissance", key="ln_c")
    nationalite = st.text_input("Nationalité", key="nat_c")

with col2:
    st.subheader("💍 Situation")
    situation = st.selectbox("Situation Matrimoniale", ["Célibataire", "Marié(e)", "Pacsé(e)", "Divorcé(e)", "Veuf/Veuve"])
    
    # Logique Conjoint
    en_couple = situation in ["Marié(e)", "Pacsé(e)"]
    
    if en_couple:
        st.info("ℹ️ Informations du Conjoint / Partenaire")
        nom_conjoint = st.text_input("Nom du Conjoint")
        prenom_conjoint = st.text_input("Prénom du Conjoint")
        date_naissance_conj = st.date_input("Date de naissance Conjoint", value=date(1980, 1, 1), key="dn_conj")
    
    nb_enfants = st.number_input("Nombre d'enfants à charge", min_value=0, max_value=15, step=1)

if nb_enfants > 0:
    st.write("📅 **Détail des enfants :**")
    c_enf = st.columns(3)
    for i in range(nb_enfants):
        with c_enf[i % 3]:
            st.date_input(f"Date de naissance Enfant n°{i+1}", value=date(2010, 1, 1), key=f"dnaiss_enf_{i}")

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

# --- SECTION 3 : PROFESSION & REVENUS DÉTAILLÉS ---
st.header("3. Situation Professionnelle & Revenus")

if en_couple:
    col_pro1, col_pro2 = st.columns(2)
    with col_pro1:
        st.subheader("💼 Client")
        statut_pro = st.selectbox("Statut (Client)", ["Salarié", "TNS", "Dirigeant", "Fonctionnaire", "Retraité", "Sans activité"], key="stat_c")
        profession = st.text_input("Profession (Client)", key="prof_c")
        rev_c = st.number_input("Salaire / BNC / BIC net annuel (Client) (€)", min_value=0, key="rev_c")
    with col_pro2:
        st.subheader("💼 Conjoint")
        statut_pro_conj = st.selectbox("Statut (Conjoint)", ["Salarié", "TNS", "Dirigeant", "Fonctionnaire", "Retraité", "Sans activité"], key="stat_conj")
        profession_conj = st.text_input("Profession (Conjoint)", key="prof_conj")
        rev_conj = st.number_input("Salaire / BNC / BIC net annuel (Conjoint) (€)", min_value=0, key="rev_conj")
else:
    cp1, cp2 = st.columns(2)
    with cp1:
        statut_pro = st.selectbox("Statut Professionnel", ["Salarié", "TNS", "Dirigeant", "Fonctionnaire", "Retraité", "Sans activité"])
        profession = st.text_input("Profession")
    with cp2:
        rev_c = st.number_input("Salaire / BNC / BIC net annuel (€)", min_value=0)

st.write(" ")
st.subheader("📊 Autres revenus & Fiscalité du foyer")
cf1, cf2, cf3 = st.columns(3)
with cf1:
    rev_foncier = st.number_input("Revenus Fonciers nets (€)", min_value=0)
    rev_dividendes = st.number_input("Dividendes / Intérêts (€)", min_value=0)
with cf2:
    rev_pensions = st.number_input("Pensions / Rentes perçues (€)", min_value=0)
    autres_rev_divers = st.number_input("Autres revenus divers (€)", min_value=0)
with cf3:
    tmi = st.selectbox("Tranche Marginale d'Imposition (TMI)", ["0%", "11%", "30%", "41%", "45%"])
    pression_fiscale = st.number_input("Impôt sur le revenu global (€)", min_value=0)

st.markdown("---")

# --- SECTION 4 & 5 : PATRIMOINE IMMOBILIER ---
st.header("4 & 5. Patrimoine Immobilier")
tab1, tab2 = st.tabs(["🏠 Immobilier Physique", "🏢 Pierre-Papier (SCPI, SCI, GFV...)"])

with tab1:
    nb_biens = st.number_input("Nombre de biens immobiliers physiques", min_value=0)
    for i in range(nb_biens):
        with st.expander(f"Bien n°{i+1}", expanded=True):
            c1, c2 = st.columns(2)
            with c1:
                st.selectbox(f"Type de bien {i+1}", ["Résidence Principale", "Résidence Secondaire", "Appartement", "Maison", "Terrain", "Parking / Garage", "Immeuble de rapport"], key=f"type_i_{i}")
                st.number_input(f"Valeur vénale (€) {i+1}", min_value=0, key=f"val_i_{i}")
            with c2:
                st.selectbox(f"Régime / Dispositif fiscal {i+1}", ["Droit Commun (Nu)", "LMNP (Amortissement)", "LMP", "Pinel / Duflot", "Malraux", "Monument Historique", "Denormandie"], key=f"fisc_i_{i}")
                st.radio(f"Crédit en cours ? {i+1}", ["Non", "Oui"], key=f"cred_i_{i}")

with tab2:
    nb_coll = st.number_input("Nombre de placements collectifs", min_value=0)
    for j in range(nb_coll):
        with st.expander(f"Placement Collectif n°{j+1}", expanded=True):
            t_coll = st.selectbox(f"Type de support", ["SCPI", "SCI", "OPCI", "GFV / GFI", "Club Deal"], key=f"type_c_{j}")
            c1, c2, c3 = st.columns(3)
            with c1:
                st.text_input("Nom du support", key=f"nom_c_{j}")
                st.selectbox("Mode de détention", ["Pleine Propriété", "Nue-Propriété", "Usufruit", "Via Assurance-Vie", "Via PER"], key=f"det_c_{j}")
            with c2:
                px_p = st.number_input("Prix de part (€)", min_value=0.0, key=f"px_c_{j}")
                nb_p = st.number_input("Nombre de parts", min_value=0.0, key=f"nb_c_{j}")
                st.number_input("Valeur de retrait (€)", value=px_p * nb_p, key=f"liq_c_{j}")
            with c3:
                if t_coll == "SCPI":
                    st.number_input("TOF (%)", min_value=0.0, max_value=100.0, key=f"tof_c_{j}")
                elif t_coll == "GFV / GFI":
                    st.text_input("Surface / Exploitation", key=f"surf_c_{j}")

st.markdown("---")

# --- SECTION 6 : PATRIMOINE FINANCIER ---
st.header("6. Patrimoine Financier")
nb_fin = st.number_input("Nombre de comptes/contrats financiers", min_value=0)
total_fin = 0.0
for k in range(nb_fin):
    with st.expander(f"Contrat n°{k+1}"):
        f1, f2, f3 = st.columns(3)
        with f1:
            t_f = st.selectbox("Type", ["Livret", "Assurance-Vie", "PER", "PEA", "Compte-Titres"], key=f"typ_f_{k}")
        with f2:
            m_f = st.number_input("Solde (€)", min_value=0.0, key=f"m_f_{k}")
            total_fin += m_f
        with f3:
            if t_f in ["Assurance-Vie", "PER"]:
                st.selectbox("Support", ["Mono-support", "Multi-support"], key=f"gest_f_{k}")
if total_fin > 0:
    st.metric("Total Épargne Financière", f"{total_fin:,.0f} €".replace(",", " "))

st.markdown("---")

# --- SECTION 7 : PRÉVOYANCE ---
st.header("7. Prévoyance & Protection")
nb_prev_input = st.number_input("Nombre de contrats de prévoyance", min_value=0)
for p in range(nb_prev_input):
    with st.expander(f"Contrat Prévoyance n°{p+1}"):
        p1, p2, p3 = st.columns(3)
        with p1:
            type_p = st.selectbox("Type de garantie", ["Décès (Capital)", "Rente Éducation", "Rente Conjoint", "IJ (Revenu)", "Invalidité", "Emprunteur"], key=f"p_t_{p}")
        with p2:
            st.number_input("Montant Garanti (€)", key=f"p_m_{p}")
        with p3:
            st.text_input("Bénéficiaires / Enfants", key=f"p_b_{p}")

st.markdown("---")

# --- SECTION 8 : SANTÉ ---
st.header("8. Santé / Mutuelle")
s1, s2 = st.columns(2)
with s1:
    st.text_input("Assureur Santé")
    st.selectbox("Type", ["Individuel", "Collectif", "Madelin"])
with s2:
    st.number_input("Cotisation Annuelle (€)", min_value=0)
    st.select_slider("Niveau de couverture", options=["100%", "200%", "300%", "400%+"])

st.markdown("---")
st.success("Analyse des revenus détaillée prête !")
