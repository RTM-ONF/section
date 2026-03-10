import numpy as np
import pandas as pd
import streamlit as st

st.title("Coordonnées")

if "section" in st.session_state:
    if st.session_state.section:
        st.dataframe(st.session_state.section.to_df())

st.title("Statistiques")

if "section" in st.session_state:
    section = st.session_state.section
    if section:
        z_Q1, z_median, z_Q3, z_D9 = np.percentile(section.z, [25, 50, 75, 90])

        data = {
            "Grandeur" : ["longueur 2D [m]",
                          "longueur 3D [m]",
                          "altitude min [m]",
                          "altitude max [m]",
                          "altitude moyenne [m]",
                          "écart-type [m]",
                          "premier quartile [m]",
                          "médiane [m]",
                          "troisième quartile [m]",
                          "neuvième décile [m]"],
            "Valeur" : [round(section.length(), 3),
                        round(section.length(dim="3D"), 3),
                        round(min(section.z), 3),
                        round(max(section.z), 3),
                        round(np.mean(section.z), 3),
                        round(np.std(section.z), 3),
                        round(z_Q1, 3),
                        round(z_median, 3),
                        round(z_Q3, 3),
                        round(z_D9, 3)]
        }

        st.dataframe(pd.DataFrame(data),
                     hide_index=True)
