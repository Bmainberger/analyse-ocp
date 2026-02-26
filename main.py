import streamlit as st

# 1. Configuration de base
st.set_page_config(page_title="OCP Patrimoine - Expert", layout="wide")
st.title("🛡️ OCP Patrimoine - Bilan Expert 360°")

# --- 1 & 2. ÉTAT CIVIL & FAMILLE ---
st.header("1 & 2. État Civil & Famille")
c1, c2 = st.columns(2)
with c1:
    nom = st.text_input("Nom & Prénom du Client")
    age_client = st.number_input("Âge", min_value=18, value=45)
    statut_pro = st.selectbox("Statut Professionnel", ["Salarié", "TNS / Libéral", "Dirigeant", "Retraité"])
with c2:
    situation = st.selectbox("Situation Familiale", ["Célibataire", "Marié (Communauté)", "Marié (Séparation)", "Pacsé", "Divorcé", "Veuf"])
    nb_enfants = st.number_input("Nombre d'enfants à charge", min_value=0, step=1)
    # Précision demandée : Dates de naissance
    for i in range(nb_enfants):
        st.text_input(f"Date de naissance Enfant {i+1} (JJ/MM/AAAA)", key=f"dnaiss_enf_{i}")

st.markdown("---")

# --- 3 & 4. IMMOBILIER & PIERRE-PAPIER DÉTAILLÉ ---
st.header("3 & 4. Patrimoine Immobilier & Diversification")

t1, t2, t3 = st.tabs(["🏠 Immobilier Physique", "🏢 SCPI / SCI", "🍷 GFV / Club Deal"])

with t1:
    col_im1, col_im2 = st.columns(2)
    with col_im1:
        rp = st.number_input("Résidence Principale (€)", min_value=0)
        rs = st.number_input("Résidence Secondaire (€)", min_value=0)
    with col_im2:
        pinel = st.number_input("Investissement Pinel (€)", min_value=0)
        lmnp = st.number_input("Investissement LMNP (€)", min_value=0)
        malraux = st.number_input("Malraux / Monument Historique (€)", min_value=0)

with t2:
    st.subheader("Fiche Technique SCPI / SCI")
    c_sc1, c_sc2 = st.columns(2)
    with c_sc1:
        nom_scpi = st.text_input("Nom de la SCPI / SCI")
        gestion = st.text_input("Société de gestion")
        mode_det = st.selectbox("Mode de détention", ["Pleine Propriété", "Nue-Propriété", "Usufruit", "Assurance-Vie", "PER", "Compte-titres"])
    with c_sc2:
        p_part = st.number_input("Prix de part (€)", min_value=0.0)
        n_part = st.number_input("Nombre de parts", min_value=0.0)
        st.write(f"**Valeur totale : {p_part * n_part:,.0f} €**")
    
    col_ind1, col_ind2, col_ind3 = st.columns(3)
    tof = col_ind1.text_input("TOF (Taux d'occupation)")
    ran = col_ind2.text_input("Report à Nouveau (RAN)")
    capi = col_ind3.text_input("Capitalisation")

with t3:
    st.subheader("GFV / GFF / GFI & Club Deal")
    c_div1, c_div2 = st.columns(2)
    with c_div1:
        nom_projet = st.text_input("Nom du groupement / Projet")
        type_div = st.selectbox("Type", ["GFV (Vigne)", "GFF (Forêt)", "GFI", "Club Deal Immo"])
        surface = st.text_input("Surface détenue")
    with c_div2:
        tri_cible = st.text_input("TRI cible (%)")
        duree_projet = st.text_input("Durée du projet")
        avantages_fiscaux = st.multiselect("Avantages", ["IFI (75%)", "Droit de mutation", "Réduction IR"])

st.markdown("---")

# --- 5. FINANCIER & RETRAITE ---
st.header("5. Patrimoine Financier")
cf1, cf2 = st.columns(2)
with cf1:
    assurance_vie = st.number_input("Assurance-Vie (€)", min_value=0)
    pea_cto = st.number_input("PEA / Compte-Titres (€)", min_value=0)
with cf2:
    per_ind = st.number_input("PER Individuel (€)", min_value=0)
    madelin_art83 = st.number_input("Madelin / Article 83 (€)", min_value=0)

st.markdown("---")

# --- 6, 7 & 8. PRÉVOYANCE & ANALYSE ---
st.header("6, 7 & 8. Prévoyance & Objectifs")
cp1, cp2 = st.columns(2)
with cp1:
    st.subheader("🛡️ Garanties de Prévoyance")
    st.checkbox("Assurance Emprunteur")
    st.checkbox("Prévoyance Pro (IJ/Invalidité)")
    st.checkbox("Garantie Décès (Capital)")
    st.checkbox("Rente Éducation")
    st.checkbox("Rente Conjoint")
with cp2:
    st.subheader("📈 Retraite & Succession")
    age_retraite = st.number_input("Âge de départ souhaité", value=64)
    revenu_cible = st.number_input("Revenu mensuel souhaité (€)", min_value=0)
    st.checkbox("Protection Conjoint (Donation/Testament)")

# --- 9. SYNTHÈSE ---
st.markdown("---")
st.header("9. Synthèse")
total_immo = rp + rs + pinel + lmnp + malraux + (p_part * n_part)
total_fin = assurance_vie + pea_cto + per_ind + madelin_art83
st.metric("PATRIMOINE GLOBAL", f"{total_immo + total_fin:,.0f} €")

if st.button("Enregistrer le Bilan"):
    st.balloons()
    st.success("Bilan enregistré avec tous les détails techniques.")
