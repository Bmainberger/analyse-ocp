with tab2:
    nb_coll = st.number_input("Nombre de placements collectifs", min_value=0)
    for j in range(nb_coll):
        with st.expander(f"Placement Collectif n°{j+1}", expanded=True):
            # 1. Sélection du type principal
            t_coll = st.selectbox(
                f"Type de support", 
                ["SCPI", "SCI", "OPCI", "GFV", "GFI", "Club Deal"], 
                key=f"type_c_{j}"
            )
            
            # 2. Logique dynamique pour les sous-types (inspirée de ton JSON)
            if t_coll == "SCPI":
                st.selectbox("Sous-type SCPI", ["Rendement", "Fiscale", "Plus-value", "Européenne", "Thématique"], key=f"st_scpi_{j}")
            elif t_coll == "GFV":
                st.selectbox("Sous-type GFV", ["Viticole", "Agricole"], key=f"st_gfv_{j}")
            elif t_coll == "GFI":
                st.selectbox("Sous-type GFI", ["Forestier", "Chasse"], key=f"st_gfi_{j}")

            c1, c2 = st.columns(2)
            with c1:
                st.text_input("Nom du support", key=f"nom_c_{j}")
                st.selectbox("Mode de détention", ["Pleine Propriété", "Nue-Propriété", "Usufruit", "Via Assurance-Vie"], key=f"det_c_{j}")
            with c2:
                st.number_input("Valeur estimée (€)", min_value=0, key=f"liq_c_{j}")
                st.number_input("Revenus annuels nets (€)", min_value=0, key=f"rev_c_{j}")
