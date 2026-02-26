# --- Remplace la partie de la SECTION 4 (tab2) par ce code ---

with tab2:
    nb_coll = st.number_input("Nombre de placements collectifs", min_value=0)
    for j in range(nb_coll):
        with st.expander(f"Placement Collectif n°{j+1}", expanded=True):
            t_coll = st.selectbox(f"Type de support", ["SCPI", "SCI", "OPCI", "GFV / GFI", "Club Deal"], key=f"type_c_{j}")
            c1, c2, c3 = st.columns(3)
            
            with c1:
                st.text_input("Nom du support", key=f"nom_c_{j}")
                st.text_input("Société de gestion", key=f"sdg_c_{j}")
                st.selectbox("Mode de détention", ["Pleine Propriété", "Nue-Propriété", "Usufruit", "Via Assurance-Vie", "Via PER"], key=f"det_c_{j}")
            
            with c2:
                px_part = st.number_input("Prix de part (€)", min_value=0.0, key=f"px_c_{j}")
                nb_parts = st.number_input("Nombre de parts", min_value=0.0, key=f"nb_c_{j}")
                
                # CALCUL AUTOMATIQUE ICI
                valeur_auto = px_part * nb_parts
                
                st.number_input("Valeur de retrait / liquidative (€)", min_value=0.0, value=valeur_auto, key=f"liq_c_{j}")
            
            with c3:
                if t_coll == "SCPI":
                    st.number_input("TOF (%)", min_value=0.0, max_value=100.0, key=f"tof_c_{j}")
                    st.number_input("Report à Nouveau (jours)", min_value=0, key=f"ran_c_{j}")
                elif t_coll == "GFV / GFI":
                    st.text_input("Type d'exploitation / Surface", key=f"surf_c_{j}")
