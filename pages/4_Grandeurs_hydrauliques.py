from math import ceil
import streamlit as st

st.title("Grandeurs hydrauliques")

if "section" in st.session_state:
    section = st.session_state.section
    if section:
        
        st.number_input(label="Hauteur d'eau [m]",
                        min_value=0.,
                        max_value=float(ceil(max(section.z)-min(section.z))),
                        step=0.001,
                        format="%0.3f")