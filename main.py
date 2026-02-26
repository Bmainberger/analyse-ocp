# --- SECTION 1 : ÉTAT CIVIL & FAMILLE ---
st.header("1. État Civil & Situation Familiale")
col1, col2 = st.columns(2)

with col1:
    st.subheader("👤 Client (Principal)")
    nom_client = st.text_input("Nom du Client")
    prenom_client = st.text_input("Prénom du Client")
    
    # Vigilance US Person pour le Client
    us_person_c = st.checkbox("🇺🇸 Citoyen Américain / US Person (Client)")
    if us_person_c:
        st.warning("⚠️ **Vigilance US Person :** Soumis à la convention franco-américaine. Vérifier l'éligibilité des supports (Ex: PEA et Assurance-Vie souvent problématiques) et les obligations de reporting FATCA.")
    
    date_naissance = st.date_input("Date de naissance", value=date(1980, 1, 1), key="dn_c")
    lieu_naissance = st.text_input("Lieu de naissance", key="ln_c")
    nationalite = st.text_input("Nationalité", key="nat_c")

with col2:
    st.subheader("💍 Situation")
    situation = st.selectbox("Situation Matrimoniale", ["Célibataire", "Marié(e)", "Pacsé(e)", "Divorcé(e)", "Veuf/Veuve"])
    
    en_couple = situation in ["Marié(e)", "Pacsé(e)"]
    
    if en_couple:
        st.info("ℹ️ Informations du Conjoint / Partenaire")
        nom_conjoint = st.text_input("Nom du Conjoint")
        prenom_conjoint = st.text_input("Prénom du Conjoint")
        
        # Vigilance US Person pour le Conjoint
        us_person_conj = st.checkbox("🇺🇸 Citoyen Américain / US Person (Conjoint)")
        if us_person_conj:
            st.warning("⚠️ **Vigilance Conjoint :** Citoyen US. Vérifier l'impact sur la déclaration commune et les comptes joints.")
            
        date_naissance_conj = st.date_input("Date de naissance Conjoint", value=date(1980, 1, 1), key="dn_conj")
    
    nb_enfants = st.number_input("Nombre d'enfants à charge", min_value=0, max_value=15, step=1)
