# --- SECTION 1 : ÉTAT CIVIL & FAMILLE ---
st.header("1. État Civil & Situation Familiale")
col1, col2 = st.columns(2)

with col1:
    st.subheader("👤 Client (Principal)")
    nom_client = st.text_input("Nom du Client")
    prenom_client = st.text_input("Prénom du Client")
    # Ajout de la vigilance US Person
    us_person_c = st.checkbox("🇺🇸 Citoyen Américain / US Person (Client)")
    if us_person_c:
        st.warning("Fiscalité spécifique : Convention Franco-Américaine & FATCA à vérifier.")
    
    date_naissance = st.date_input("Date de naissance", value=date(1980, 1, 1), key="dn_c")
    nationalite = st.text_input("Nationalité", key="nat_c")

with col2:
    st.subheader("💍 Situation")
    situation = st.selectbox("Situation Matrimoniale", ["Célibataire", "Marié(e)", "Pacsé(e)", "Divorcé(e)", "Veuf/Veuve"])
    
    en_couple = situation in ["Marié(e)", "Pacsé(e)"]
    if en_couple:
        st.info("ℹ️ Informations du Conjoint")
        nom_conjoint = st.text_input("Nom du Conjoint")
        # Vigilance US Person Conjoint
        us_person_conj = st.checkbox("🇺🇸 Citoyen Américain / US Person (Conjoint)")
        if us_person_conj:
            st.warning("Vérifier l'impact sur l'imposition commune du foyer.")
