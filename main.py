import streamlit as st

# Configuration de la page
st.set_page_config(page_title="OCP Patrimoine", layout="wide")

# Titre principal
st.title("🛡️ OCP Patrimoine - Bilan 360°")

# --- SECTION 1 & 2 : CLIENT ---
st.header("1 & 2. État Civil & Profession")
col1, col2 = st.columns(2)
with col1:
    nom = st.text_input("Nom & Prénom du Client")
    statut = st.selectbox("Statut Professionnel", ["Salarié", "TNS", "Dirigeant", "Retraité"])
with col2:
    situation = st.selectbox("Situation Familiale", ["Célibataire", "Marié(e)", "Pacsé(e)", "Divorcé(e)"])
    revenus = st.number_input("Revenu Annuel Net (€)", min_value=0, step=1000)

st.markdown("---")

# --- SECTION 3 & 4 : IMMOBILIER ---
st.header("3 & 4. Patrimoine Immobilier")
val_immo = st.number_input("Valeur totale estimée de l'immobilier (€)", min_value=0, step=5000)

st.markdown("---")

# --- SECTION 5 : FINANCIER ---
st.header("5. Patrimoine Financier")
val_fin = st.number_input("Valeur totale du patrimoine financier (€)", min_value=0, step=1000)

st.markdown("---")

# --- SECTION 6 : PRÉVOYANCE ---
st.header("6. Prévoyance & Emprunteur")
st.checkbox("Assurance Emprunteur (Prêts)")
st.checkbox("Prévoyance (IJ, Rente, Invalidité)")

st.markdown("---")

# --- SECTION 7 : SUCCESSION & TRANSMISSION ---
st.header("7. Succession & Transmission")
st.checkbox("Présence d'un testament")
st.checkbox("Donations antérieures effectuées")
st.checkbox("Clause bénéficiaire Assurance-Vie mise à jour")

st.markdown("---")

# --- SECTION 8 : RENTES & RETRAITE ---
st.header("8. Rentes & Objectifs Retraite")
col_r1, col_r2 = st.columns(2)
with col_r1:
    age_retraite = st.number_input("Âge de départ souhaité", min_value=50, max_value=80, value=64)
    rente_souhaitee = st.number_input("Revenu mensuel souhaité à la retraite (€)", min_value=0)
with col_r2:
    capital_retraite = st.number_input("Capital déjà constitué pour la retraite (€)", min_value=0)
    st.write("Calcul de l'effort d'épargne nécessaire...")

st.markdown("---")

# --- SECTION 9 : SYNTHÈSE ---
st.header("9. Synthèse du Bilan")
total_patrimoine = val_immo + val_fin
st.metric("PATRIMOINE BRUT TOTAL", f"{total_patrimoine:,.0f} €")

if st.button("Enregistrer le bilan"):
    st.balloons()
    st.success(f"Analyse terminée pour {nom} !")
