import numpy as np
import streamlit as st

st.title("Coordonnées")

if "section" in st.session_state:
    if st.session_state.section:
        st.dataframe(st.session_state.section.to_df())

st.title("Statistiques basiques")

if "section" in st.session_state:
    section = st.session_state.section
    if section:
        z_Q1, z_median, z_Q3, z_D9 = np.percentile(section.z, [25, 50, 75, 90])

        st.markdown(f"""
        | Grandeur           | Valeur                                 |
        |--------------------|----------------------------------------|
        | Longueur 2D        | {round(section.length(), 3)} m         |
        | Longueur 3D        | {round(section.length(dim="3D"), 3)} m |
        | Altitude min       | {round(min(section.z), 3)} m           |
        | Altitude max       | {round(max(section.z), 3)} m           |
        | Altitude moyenne   | {round(np.mean(section.z), 3)} m       |
        | Ecart-type         | {round(np.std(section.z), 3)} m        |
        | Premier quartile   | {round(z_Q1, 3)} m                     |
        | Médiane            | {round(z_median, 3)} m                 |
        | Troisième quartile | {round(z_Q3, 3)} m                     |
        | Neuvième décile    | {round(z_D9, 3)} m                     |
        """)
