import streamlit as st
from datetime import date

# 1. Configuration de la page
st.set_page_config(page_title="OCP Patrimoine - Bilan Complet", page_icon="🛡️", layout="wide")

st.title("🛡️ OCP Patrimoine - Bilan et Analyse")
st.markdown("---")

# --- SECTION 1 : ÉTAT CIVIL & FAMILLE ---
st.header("1. État Civil & Situation Familiale")
col1, col2 = st.columns(2)
with col1:
    st.subheader("Le Client")
    nom_client = st.text_input("Nom du Client")
    prenom_client = st.text_input("Prénom du Client")
    date_naissance = st.date_input("Date de naissance", value=date(1980, 1, 1), key="dnaiss_c")
    lieu_naissance = st.text_input("Lieu de naissance", key="lieu_c")
    nationalite = st.text_input("Nationalité", key="nat_c") 

with col2:
    st.subheader("Situation")
    situation = st.selectbox("Situation Matrimoniale", ["Célibataire", "Marié(e)", "Pacsé(e)", "Divorcé(e)", "Veuf/Veuve"])
    nb_enfants = st.number_input("Nombre d'enfants à charge", min_value=0, max_value=15, step=1)

if situation in ["Marié(e)", "Pacsé(e)"]:
    st.subheader("Informations du Conjoint")
    c_col1, c_col2 = st.columns(2)
    with c_col1:
        st.text_input("Nom du Conjoint", key="nom_conj")
        st.date_input("Date de naissance conjoint", value=date(1980, 1, 1), key="dnaiss_conj")
        st.text_input("Lieu de naissance conjoint", key="lieu_conj")
    with c_col2:
        st.text_input("Prénom du Conjoint", key="pre_conj")
        st.text_input("Nationalité Conjoint", key="nat_conj")

if nb_enfants > 0:
    st.write("📅 **Détail des enfants :**")
    c_enf = st.columns(3)
    for i in range(int(nb_enfants)):
        with c_enf[i % 3]:
            st.date_input(f"Date de naissance Enfant n°{i+1}", value=date(2010, 1, 1), key=f"dnaiss_enf_{i}")

st.markdown("---")

# --- SECTION 2 : COORDONNÉES ---
st.header("2. Coordonnées")
c_coo1, c_coo2, c_coo3 = st.columns([2, 1, 1])
with c_coo1:
    st.text_input("Adresse postale complète")
with c_coo2:
    st.text_input("Téléphone")
with c_coo3:
    st.text_input("Email")

st.markdown("---")

# --- SECTION 3 : PROFESSION & REVENUS ---
st.header("3. Situation Professionnelle & Revenus")
cp1, cp2, cp3 = st.columns(3)
with cp1:
    st.selectbox("Statut Professionnel", ["Salarié", "TNS / Libéral", "Dirigeant", "Fonctionnaire", "Retraité", "Sans activité"])
    st.text_input("Profession / Intitulé du poste")
with cp2:
    st.number_input("Revenu net annuel (€)", min_value=0)
    st.number_input("Autres revenus (Foncier, etc.) (€)", min_value=0)
with cp3:
    st.selectbox("Tranche Marginale d'Imposition (TMI)", ["0%", "11%", "30%", "41%", "45%"])
    st.number_input("Âge de départ à la retraite prévu", min_value=50, max_value=80, value=64)

st.markdown("---")

# --- SECTION 4 & 5 : PATRIMOINE IMMOBILIER ---
st.header("4 & 5. Patrimoine Immobilier")
tab1, tab2 = st.tabs(["🏠 Immobilier Physique", "🏢 Pierre-Papier (SCPI, SCI, GFV...)"])

with tab1:
    nb_biens = st.number_input("Nombre de biens immobiliers physiques", min_value=0, key="nb_p_p")
    for i in range(int(nb_biens)):
        with st.expander(f"Bien n°{i+1}", expanded=True):
            c1, c2 = st.columns(2)
            with c1:
                st.selectbox(f"Type de bien {i+1}", ["Résidence Principale", "Résidence Secondaire", "Appartement", "Maison", "Terrain", "Parking", "Immeuble de rapport"], key=f"type_i_{i}")
                st.number_input(f"Valeur vénale (€) {i+1}", min_value=0, key=f"val_i_{i}")
            with c2:
                st.selectbox(f"Régime / Dispositif fiscal {i+1}", ["Droit Commun (Nu)", "LMNP", "LMP", "Pinel", "Malraux", "Monument Historique"], key=f"fisc_i_{i}")
                st.radio(f"Crédit en cours ? {i+1}", ["Non", "Oui"], key=f"cred_i_{i}")

with tab2:
    nb_coll = st.number_input("Nombre de placements collectifs", min_value=0, key="nb_p_c")
    for j in range(int(nb_coll)):
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

# --- SECTION 6 : PATRIMOINE FINANCIER (AJOUTS : BANQUE & DATE) ---
st.header("6. Patrimoine Financier")
nb_fin = st.number_input("Nombre de comptes/contrats financiers", min_value=0, key="nb_f_f")
total_fin = 0.0
for k in range(int(nb_fin)):
    with st.expander(f"Contrat n°{k+1}"):
        f1, f2, f3 = st.columns(3)
        with f1:
            st.selectbox("Type", ["Livret", "Assurance-Vie", "PER", "PEA", "Compte-Titres"], key=f"typ_f_{k}")
            st.text_input("Établissement / Compagnie", key=f"banque_f_{k}")
        with f2:
            m_f = st.number_input("Solde (€)", min_value=0.0, key=f"m_f_{k}")
            total_fin += m_f
            st.date_input("Date d'adhésion", key=f"date_f_{k}")
        with f3:
            st.selectbox("Support / Gestion", ["Mono-support", "Multi-support", "Gestion Pilotée"], key=f"gest_f_{k}")
if total_fin > 0:
    st.metric("Total Épargne Financière", f"{total_fin:,.0f} €".replace(",", " "))

st.markdown("---")

# --- SECTION 7 : PRÉVOYANCE (AJOUT : QUOTITÉ) ---
st.header("7. Prévoyance & Protection")
nb_prev_input = st.number_input("Nombre de contrats de prévoyance", min_value=0, key="nb_p_v")
for p in range(int(nb_prev_input)):
    with st.expander(f"Contrat Prévoyance n°{p+1}"):
        p1, p2, p3 = st.columns(3)
        with p1:
            type_p = st.selectbox("Type de garantie", ["Décès (Capital)", "Rente Éducation", "Rente Conjoint", "IJ (Revenu)", "Invalidité", "Emprunteur"], key=f"p_t_{p}")
        with p2:
            st.number_input("Montant Garanti (€)", key=f"p_m_{p}")
            if type_p == "Emprunteur":
                st.number_input("Quotité assurée (%)", min_value=0, max_value=100, value=100, key=f"p_q_{p}")
        with p3:
            st.text_input("Bénéficiaires / Organisme", key=f"p_b_{p}")

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
st.success("Toutes les sections sont opérationnelles !")
