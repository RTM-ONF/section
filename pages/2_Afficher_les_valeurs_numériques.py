import streamlit as st

st.title("Afficher les valeurs numériques")

if "section" in st.session_state:
    if st.session_state.section:
        st.dataframe(st.session_state.section.to_df())