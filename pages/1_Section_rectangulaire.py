import pandas as pd
import streamlit as st

st.title("Section rectangulaire")

st.header("Définition de la géométrie")

width = st.number_input(
    "Largeur de la section - b (m)",
    min_value=0.01,
    value=5.00,
    step=0.01,
    format="%.2f"
)

water_height = st.number_input(
    "Hauteur d'eau - h (m)",
    min_value=0.01,
    value=1.00,
    step=0.01,
    format="%.2f"
)

st.header("Grandeurs géométriques de la section d'écoulement")

b = width
h = water_height

P = b + 2. * h
A = b * h
R = A / P

df = pd.DataFrame({ "Grandeur": ["Périmètre mouillé (m)", "Aire mouillée (m)", "Rayon hydraulique (m)"], "Valeur": [P, A, R] })
st.dataframe(df)

st.subheader("Formulaire")

st.markdown(
    """
    ##### Périmètre mouillé
    """
)

st.latex(
    r"""
    P = b + 2 \times h
    """
)

st.markdown(
    """
    ##### Aire mouillée
    """
)

st.latex(
    r"""
    A = b \times h
    """
)

st.markdown(
    """
    ##### Rayon hydraulique
    """
)

st.latex(
    r"""
    R = \frac{A}{P} = \frac{b \times h}{b + 2 \times h}
    """
)