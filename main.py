import streamlit as st

# Configuration de la page
st.set_page_config(page_title="OCP Patrimoine - Expert", layout="wide")

# Titre principal
st.title("🛡️ OCP Patrimoine - Bilan 360°")

# --- SECTIONS 1 & 2 : CLIENT & PRO ---
st.header("1 & 2. État Civil & Profession")
c1, c2 = st.columns(2)
with c1:
    nom = st.text_input("Nom & Prénom du Client")
    age = st.number_input("Âge", min_value=18, max_value=100, value=45)
    statut_pro = st.selectbox("Statut Professionnel", ["Salarié", "TNS / Libéral", "Dirigeant (SAS/SARL)", "Retraité", "Sans activité"])
with c2:
    situation = st.selectbox("Situation Familiale", ["Célibataire", "Marié(e) (Communauté)", "Marié(e) (Séparation)", "Pacsé(e)", "Divorcé(e)", "Veuf(ve)"])
    revenus = st.number_input("Revenu Annuel Net Global (€)", min_value=0, step=1000)
    enfants = st.number_input("Nombre d'enfants à charge", min_value=0, step=1)

st.markdown("---")

# --- SECTIONS 3 & 4 : PATRIMOINE IMMOBILIER ---
st.header("3 & 4. Patrimoine Immobilier")
col_immo1, col_immo2 = st.columns(2)

with col_immo1:
    st.subheader("🏠 Immobilier Physique")
    rp = st.number_input("Résidence Principale (€)", min_value=0, step=5000)
    rs = st.number_input("Résidence Secondaire (€)", min_value=0, step=5000)
    locatif = st.number_input("Investissement Locatif (Pinel, LMNP, Malraux...) (€)", min_value=0, step=5000)
    foncier = st.number_input("Terrains / Foncier (€)", min_value=0, step=5000)

with col_immo2:
    st.subheader("🏢 Pierre-Papier (Calcul Automatique)")
    type_pp = st.selectbox("Type de support", ["SCPI de Rendement", "SCPI Fiscale", "SCI / SC", "GFV (Viticole)", "GFI (Forestier)"])
    p_part = st.number_input("Prix d'une part (€)", min_value=0, step=10)
    n_part = st.number_input("Nombre de parts détenues", min_value=0, step=1)
    val_pierre_papier = p_part * n_part
    st.write(f"**Valeur calculée : {val_pierre_papier:,.0f} €**")

total_immo = rp + rs + locatif + foncier + val_pierre_papier

st.markdown("---")

# --- SECTION 5 : PATRIMOINE FINANCIER & RETRAITE ---
st.header("5. Patrimoine Financier & Retraite")
c_f1, c_f2 = st.columns(2)
with c_f1:
    st.subheader("💰 Épargne Disponibles")
    assurance_vie = st.number_input("Assurance-Vie / Capitalisation (€)", min_value=0, step=1000)
    livrets = st.number_input("Liquidités (Livrets, CC) (€)", min_value=0, step=1000)
    pea = st.number_input("PEA / Comptes Titres (€)", min_value=0, step=1000)
with c_f2:
    st.subheader("📉 Épargne Retraite & Salariale")
    per = st.number_input("PER (Individuel ou Collectif) (€)", min_value=0, step=1000)
    madelin = st.number_input("Contrats Madelin (€)", min_value=0, step=1000)
    art83 = st.number_input("Article 83 (€)", min_value=0, step=1000)
    pee = st.number_input("PEE / PERCO (€)", min_value=0, step=1000)

total_fin = assurance_vie + livrets + pea + per + madelin + art83 + pee

st.markdown("---")

# --- SECTIONS 6, 7 & 8 : PRÉVOYANCE, SUCCESSION & RETRAITE ---
st.header("6, 7 & 8. Analyse des Risques & Objectifs")
c_a1, c_a2 = st.columns(2)
with c_a1:
    st.subheader("🛡️ Prévoyance & Succession")
    st.checkbox("Assurance Emprunteur (Couverture des prêts)")
    st.checkbox("Prévoyance Professionnelle (IJ / Invalidité)")
    st.checkbox("Garantie Décès (Capital)")
    st.checkbox("Rente Éducation")
    st.checkbox("Rente Conjoint")
    st.checkbox("Protection du conjoint (Testament / Donation)")
    st.checkbox("Clause Bénéficiaire (Mise à jour)")
with c_a2:
    st.subheader("📈 Objectifs Retraite")
    age_retraite = st.number_input("Âge de départ souhaité", value=64, min_value=50)
    revenu_souhaite = st.number_input("Revenu mensuel net souhaité à la retraite (€)", min_value=0, step=100)
    rente_estimee = st.number_input("Rente estimée actuelle (Relevé carrière) (€)", min_value=0, step=100)

st.markdown("---")

# --- SECTION 9 : SYNTHÈSE FINALE ---
st.header("9. Synthèse du Patrimoine Brut")
total_global = total_immo + total_fin

col_m1, col_m2 = st.columns(2)
with col_m1:
    st.metric("TOTAL IMMOBILIER", f"{total_immo:,.0f} €")
    st.metric("TOTAL FINANCIER", f"{total_fin:,.0f} €")
with col_m2:
    st.subheader("Patrimoine Global")
    st.title(f"{total_global:,.0f} €")

if st.button("Valider et Enregistrer le Bilan"):
    st.balloons()
    st.success(f"Dossier de {nom} enregistré avec succès.")
