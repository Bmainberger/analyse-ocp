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

# --- SECTION 2 : ADRESSE & PRO ---
st.header("2. Coordonnées et Situation Professionnelle")
c_pro1, c_pro2 = st.columns(2)
with c_pro1:
    adresse = st.text_input("Adresse complète")
    residence_statut = st.radio("Statut résidence", ["Propriétaire", "Locataire", "Logé par l'employeur"])
with c_pro2:
    statut_pro = st.selectbox("Statut professionnel", ["Salarié", "TNS", "Fonctionnaire", "Retraité"])
    revenu_annuel = st.number_input("Revenu Annuel Net (€)", min_value=0, step=1000)

st.markdown("---")

# --- SECTION 3 & 4 : PATRIMOINE IMMOBILIER & COLLECTIF ---
st.header("3 & 4. Patrimoine Immobilier")
tab1, tab2 = st.tabs(["🏠 Immobilier Physique", "🏢 Pierre-Papier (SCPI, SCI, GFV...)"])

with tab1:
    nb_biens = st.number_input("Nombre de biens immobiliers physiques", min_value=0)
    for i in range(nb_biens):
        with st.expander(f"Bien n°{i+1}"):
            st.selectbox(f"Type", ["Résidence Principale", "Résidence Secondaire", "Locatif"], key=f"type_i_{i}")
            st.number_input(f"Valeur vénale (€)", min_value=0, key=f"val_i_{i}")

with tab2:
    nb_coll = st.number_input("Nombre de placements collectifs", min_value=0)
    for j in range(nb_coll):
        with st.expander(f"Placement Collectif n°{j+1}", expanded=True):
            t_coll = st.selectbox(f"Type de support", ["SCPI", "SCI", "OPCI", "GFV / GFI", "Club Deal"], key=f"type_c_{j}")
            c1, c2, c3 = st.columns(3)
            with c1:
                st.text_input("Nom du support", key=f"nom_c_{j}")
                st.text_input("Société de gestion", key=f"sdg_c_{j}")
                st.selectbox("Mode de détention", ["Pleine Propriété", "Nue-Propriété", "Usufruit", "Via Assurance-Vie", "Via PER"], key=f"det_c_{j}")
            with c2:
                px_part = st.number_input("Prix de part (€)", min_value=0.0, key=f"px_c_{j}")
                nb_parts = st.number_input("Nombre de parts", min_value=0.0, key=f"nb_c_{j}")
                # Calculateur automatique
                val_auto = px_part * nb_parts
                st.number_input("Valeur de retrait / liquidative (€)", min_value=0.0, value=val_auto, key=f"liq_c_{j}")
            with c3:
                if t_coll == "SCPI":
                    st.number_input("TOF (%)", min_value=0.0, max_value=100.0, key=f"tof_c_{j}")
                    st.number_input("Report à Nouveau (jours)", min_value=0, key=f"ran_c_{j}")
                elif t_coll == "GFV / GFI":
                    st.text_input("Type d'exploitation / Surface", key=f"surf_c_{j}")
                elif t_coll == "Club Deal":
                    st.number_input("TRI Cible (%)", key=f"tri_c_{j}")

st.markdown("---")

# --- SECTION 5 : PATRIMOINE FINANCIER ---
st.header("5. Patrimoine Financier")
nb_fin = st.number_input("Nombre de comptes/contrats financiers", min_value=0)
total_fin = 0.0
for k in range(nb_fin):
    with st.expander(f"Contrat n°{k+1}"):
        f1, f2, f3 = st.columns(3)
        with f1:
            t_fin = st.selectbox("Type de placement", ["Livret", "Assurance-Vie", "PER", "PEA", "Compte-Titres"], key=f"typ_f_{k}")
            st.text_input("Établissement", key=f"etab_f_{k}")
        with f2:
            m_f = st.number_input("Valeur actuelle (€)", min_value=0.0, key=f"m_f_{k}")
            total_fin += m_f
        with f3:
            if t_fin in ["Assurance-Vie", "PER"]:
                st.selectbox("Gestion", ["Mono-support", "Multi-support"], key=f"gest_f_{k}")
                st.slider("% Unités de Compte", 0, 100, 30, key=f"risk_f_{k}")
if total_fin > 0:
    st.metric("Total Épargne Financière", f"{total_fin:,.0f} €".replace(",", " "))

st.markdown("---")

# --- SECTION 6 : PRÉVOYANCE ---
st.header("6. Prévoyance & Protection")
nb_p = st.number_input("Nombre de contrats de prévoyance", min_value=0)
for p in range(nb_p):
    with st.expander(f"Contrat Prévoyance n°{p+1}"):
        p1, p2 = st.columns(2)
        with p1:
            type_p = st.selectbox("Garantie", ["Décès", "IJ (Revenu)", "Invalidité", "Emprunteur", "GAV"], key=f"p_t_{p}")
            st.text_input("Assureur", key=f"p_a_{p}")
        with p2:
            st.number_input("Capital/Rente garanti (€)", key=f"p_c_{p}")
            if type_p == "IJ (Revenu)":
                st.selectbox("Franchise", ["7j", "15j", "30j", "90j"], key=f"p_f_{p}")
            elif type_p == "Emprunteur":
                st.number_input("Quotité (%)", value=100, key=f"p_q_{p}")

st.markdown("---")

# --- SECTION 7 : SANTÉ ---
st.header("7. Santé / Mutuelle")
s1, s2 = st.columns(2)
with s1:
    st.text_input("Nom de la Mutuelle")
    st.selectbox("Type", ["Individuel", "Collectif", "Senior", "Madelin"])
with s2:
    st.number_input("Cotisation Mensuelle (€)", min_value=0)
    st.select_slider("Niveau de remboursement", options=["100%", "200%", "300%", "400%+"])

st.markdown("---")
st.success("Toutes les sections (1-7) sont restaurées et le calculateur SCPI est prêt !")
