# --- SECTION 11 : OBJECTIFS DU CLIENT ---
st.markdown("---")
st.header("🎯 11. Objectifs & Priorités")

col_obj1, col_obj2 = st.columns(2)

with col_obj1:
    st.subheader("Priorités Patrimoniales")
    obj_prioritaires = st.multiselect(
        "Quels sont les objectifs principaux ?",
        ["Préparer la Retraite", "Réduire la fiscalité (Impôts)", "Protéger la famille / le conjoint", 
         "Transmettre un capital aux enfants", "Développer le patrimoine immobilier", 
         "Générer des revenus immédiats", "Financer les études des enfants"],
        key="obj_multi"
    )

with col_obj2:
    st.subheader("Horizon & Profil")
    horizon = st.select_slider(
        "Horizon de placement",
        options=["Court terme (0-2 ans)", "Moyen terme (2-8 ans)", "Long terme (8 ans +)", "Transmission / Vie"],
        key="horizon_p"
    )
    profil_risque = st.select_slider(
        "Profil de risque",
        options=["Prudent", "Équilibré", "Dynamique", "Offensif"],
        key="profil_r"
    )

st.text_area("Commentaires libres / Projets spécifiques (ex: Achat d'une résidence secondaire...)", key="obj_notes")
