import streamlit as st

# Configuration de base
st.set_page_config(page_title="OCP Patrimoine", layout="wide")
st.title("🛡️ OCP Patrimoine - Bilan")

# --- SECTIONS ---
st.header("1 & 2. État Civil & Profession")
nom = st.text_input("Nom & Prénom")
revenus = st.number_input("Revenu Annuel Net (€)", min_value=0)

st.markdown("---")

st.header("3 & 4. Patrimoine Immobilier")
val_immo = st.number_input("Valeur totale de l'immobilier (€)", min_value=0)

st.markdown("---")

st.header("5. Patrimoine Financier")
val_fin = st.number_input("Valeur totale du financier (€)", min_value=0)

st.markdown("---")

# --- SYNTHÈSE SIMPLE ---
st.header("Synthèse")
total = val_immo + val_fin
st.subheader(f"Patrimoine Total : {total:,.0f} €")

if st.button("Calculer"):
    st.success(f"Bilan mis à jour pour {nom}")
