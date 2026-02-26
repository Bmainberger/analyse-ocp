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
st.write("Détaillez vos actifs immobiliers physiques et financiers (Pierre-Papier)")

t1, t2 = st.tabs(["🏠 Immobilier Physique", "🏢 SCPI / GFV / SCI"])

total_immo = 0.0

with t1:
    col_i1, col_i2 = st.columns(2)
    with col_i1:
        rp = st.number_input("Résidence Principale (€)", min_value=0, step=5000)
        rs = st.number_input("Résidence Secondaire (€)", min_value=0, step=5000)
    with col_i2:
        locatif = st.number_input("Investissement Locatif (Pinel, LMNP...) (€)", min_value=0, step=5000)
        foncier = st.number_input("Terrains / Foncier (€)", min_value=0, step=5000)
    total_immo += (rp + rs + locatif + foncier)

with t2:
    st.info("Calcul automatique de la valeur Pierre-Papier")
    c_s1, c_s2 = st.columns(2)
    with c_s1:
        p_part = st.number_input("Prix de la part (€)", min_value=0, step=10, key="price_part")
        n_part = st.number_input("Nombre de parts", min_value=0, step=1, key="nb_part")
    with c_s2:
        type_pp = st.selectbox("Type de support", ["SCPI Rendement", "SCPI Fiscale", "SCI / SC", "GFV (Groupement Foncier Viticole)", "GFI (Forestier)"])
        val_calculee = p_part * n_part
        st.write(f"**Valeur totale estimée : {val_calculee:,.0f} €**")
    total_immo += val_calculee

st.markdown("---")

# --- SECTION 5 : PATRIMOINE FINANCIER & RETRAITE ---
st.header("5. Patrimoine Financier & Retraite")
c_f1, c_f2 = st.columns(2)
with c_f1:
    assurance_vie = st.number_input("Assurance-Vie / Capitalisation (€)", min_value=0, step=1000)
    livrets = st.number_input("Liquidités (Livrets, Compte Courant) (€)", min_value=0, step=1000)
    pea = st.number_input("PEA / Compte Titres (€)", min_value=0, step=1000)
with c_f2:
    per = st.number_input("PER (Individuel ou Collectif) (€)", min_value=0, step=1000)
    madelin = st.number_input("Contrats Madelin / Art. 83 (€)", min_value=0, step=1000)
    pEE = st.number_input("Épargne Salariale (PEE / PERCO) (€)", min_value=0, step=1000)

total_fin = assurance_vie + livrets + pea + per + madelin + pEE

st.markdown("---")

# --- SECTION 6, 7 & 8 : PRÉVOYANCE, SUCCESSION & RENTES ---
st.header("6, 7 & 8. Analyse des Risques & Objectifs")
c_a1, c_a2 = st.columns(2)
with c_a1:
    st.subheader("🛡️ Prévoyance & Succession")
    st.checkbox("Assurance Emprunteur (Couverture des prêts)")
    st.checkbox("Prévoyance Professionnelle (IJ / Invalidité)")
    st.checkbox("Garantie Décès / Rente Éducation")
    st.checkbox("Protection du conjoint (Testament / Donation)")
with c_a2:
    st.subheader("📈 Objectifs Retraite")
    age_retraite = st.number_input("Âge de départ souhaité", value=64, min_value=50)
    revenu_souhaite = st.number_input("Revenu mensuel net souhaité (€)", min_value=0, step=100)
    st.write("Le bilan analysera l'effort d'épargne nécessaire.")

st.markdown("---")

# --- SECTION 9 : SYNTHÈSE FINALE ---
st.header("9. Synthèse du Patrimoine Brut")
total_patrimoine = total_immo + total_fin

col_m1, col_m2 = st.columns(2)
with col_m1:
    st.metric("PATRIMOINE IMMOBILIER", f"{total_immo:,.0f} €")
    st.metric("PATRIMOINE FINANCIER", f"{total_fin:,.0f} €")
with col_m2:
    st.subheader("Total Global")
    st.title(f"{total_patrimoine:,.0f} €")

if st.button("Valider et Enregistrer le Bilan"):
    st.balloons()
    st.success(f"Bilan de {nom} enregistré avec succès !")
