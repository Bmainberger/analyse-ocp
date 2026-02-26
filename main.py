import streamlit as st

st.set_page_config(page_title="OCP Patrimoine - Expert v3", layout="wide")
st.title("🛡️ OCP Patrimoine - Bilan Expert 360°")

# --- 1 & 2. ÉTAT CIVIL & ENFANTS ---
st.header("1 & 2. État Civil & Famille")
c1, c2 = st.columns(2)
with c1:
    nom = st.text_input("Nom & Prénom du Client")
    statut = st.selectbox("Statut Pro", ["Salarié", "TNS", "Dirigeant", "Retraité"])
with c2:
    nb_enfants = st.number_input("Nombre d'enfants à charge", min_value=0, step=1)
    # Précision sur les dates de naissance demandée
    dates_naiss = []
    for i in range(nb_enfants):
        dates_naiss.append(st.text_input(f"Date de naissance Enfant {i+1} (JJ/MM/AAAA)", key=f"enf_{i}"))

st.markdown("---")

# --- 3 & 4. IMMOBILIER & PIERRE-PAPIER (DÉTAILLÉ) ---
st.header("3 & 4. Patrimoine Immobilier & Diversification")

# Onglets pour séparer la fiscalité complexe
tab_physique, tab_scpi, tab_divers = st.tabs(["🏠 Immo Physique", "🏢 SCPI / SCI", "🍷 GFV / GFI / Club Deal"])

with tab_physique:
    st.subheader("Détail Fiscalité Immobilière")
    col_im1, col_im2 = st.columns(2)
    with col_im1:
        rp = st.number_input("Résidence Principale (€)", min_value=0)
        pinel = st.number_input("Pinel (Réduction d'impôt) (€)", min_value=0)
    with col_im2:
        lmnp = st.number_input("LMNP (Amortissement/BIC) (€)", min_value=0)
        malraux = st.number_input("Malraux / Monument Historique (€)", min_value=0)

with tab_scpi:
    st.subheader("Fiche SCPI / SCI")
    c_scpi1, c_scpi2 = st.columns(2)
    with c_scpi1:
        nom_scpi = st.text_input("Nom de la SCPI / SCI")
        gestion = st.text_input("Société de gestion")
        mode_det = st.selectbox("Mode de détention", ["Pleine Propriété", "Nue-Propriété", "Usufruit", "Assurance-Vie", "PER", "Compte-titres"])
    with c_scpi2:
        p_part = st.number_input("Prix de part (€)", min_value=0.0)
        n_part = st.number_input("Nombre de parts", min_value=0.0)
        st.write(f"**Valeur totale : {p_part * n_part:,.0f} €**")
    
    st.write("**Indicateurs techniques**")
    col_ind1, col_ind2, col_ind3 = st.columns(3)
    tof = col_ind1.text_input("TOF (Taux d'occupation)")
    ran = col_ind2.text_input("RAN (Report à nouveau)")
    cap = col_ind3.text_input("Capitalisation")

with tab_divers:
    st.subheader("GFV / GFF / GFI & Club Deal")
    c_div1, c_div2 = st.columns(2)
    with c_div1:
        nom_gfv = st.text_input("Nom du groupement / Projet")
        type_gfv = st.selectbox("Type", ["GFV (Vigne)", "GFF (Forêt)", "GFI (Forestier)", "Club Deal Immo"])
        surface = st.text_input("Surface détenue / Unités")
    with c_div2:
        revenus_agr = st.number_input("Revenus annuels (€)", min_value=0)
        tri_cible = st.text_input("TRI Cible (%)")
        avantages = st.multiselect("Avantages fiscaux", ["IFI (Exonération 75%)", "Droit de mutation", "Réduction IR"])

st.markdown("---")

# --- 6, 7 & 8. PRÉVOYANCE & RETRAITE ---
st.header("6, 7 & 8. Analyse & Garanties")
c_p1, c_p2 = st.columns(2)
with c_p1:
    st.subheader("🛡️ Prévoyance (Détail des Garanties)")
    st.checkbox("Assurance Emprunteur")
    st.checkbox("Prévoyance Pro (IJ / Invalidité)")
    st.checkbox("Garantie Décès (Capital)")
    st.checkbox("Rente Éducation (Rente annuelle)")
    st.checkbox("Rente Conjoint")
with c_p2:
    st.subheader("📈 Objectifs Retraite")
    age_r = st.number_input("Âge souhaité", value=64)
    revenu_s = st.number_input("Objectif revenu mensuel (€)", min_value=0)
    # Section spécifique pour les revenus agricoles/forestiers si besoin
    st.write(f"**Revenus divers estimés : {revenus_agr/12:,.0f} € / mois**")

if st.button("Enregistrer ce Bilan Expert"):
    st.balloons()
    st.success("Données enregistrées avec tous les détails techniques.")
