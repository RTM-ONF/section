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
        | longueur 2D        | {round(section.length(), 3)} m         |
        | longueur 3D        | {round(section.length(dim="3D"), 3)} m |
        | altitude min       | {round(min(section.z), 3)} m           |
        | altitude max       | {round(max(section.z), 3)} m           |
        | altitude moyenne   | {round(np.mean(section.z), 3)} m       |
        | écart-type         | {round(np.std(section.z), 3)} m        |
        | premier quartile   | {round(z_Q1, 3)} m                     |
        | médiane            | {round(z_median, 3)} m                 |
        | troisième quartile | {round(z_Q3, 3)} m                     |
        | neuvième décile    | {round(z_D9, 3)} m                     |
        """)
