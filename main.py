import streamlit as st

st.set_page_config(page_title="OCP Patrimoine", page_icon="🛡️")

st.title("🛡️ OCP Patrimoine - Analyse")
st.write("Félicitations Béatrice ! Le logiciel est officiellement en ligne.")

st.sidebar.header("Menu")
nom = st.text_input("Entrez votre nom pour tester :")
if nom:
    st.success(f"Bienvenue {nom} ! Le moteur de calcul est prêt.")

st.info("Ceci est une version de test pour valider l'hébergement.")
