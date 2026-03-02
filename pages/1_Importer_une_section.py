import pandas as pd
import streamlit as st

st.title("Importer une section")

uploaded_file = st.file_uploader(
    "Téléverser le fichier contenant la géométrie de la section")

col1, col2 = st.columns(2)

delimiters = {"\t" : "tabulation" ,
              " " : "espace",
              ";" : "point-virgule",
              "," : "virgule"}

with col1:
    delimiter = st.selectbox("Délimiteur",
                             options=delimiters.keys(),
                             format_func=lambda x : delimiters[x])

    distance_field = st.text_input("Nom du champ des distances",
                                   "X")

separators = {"." : "point",
              "," : "virgule"}

with col2:
    separator = st.selectbox("Séparateur décimal",
                             options=separators.keys(),
                             format_func=lambda x : separators[x])

    altitude_field = st.text_input("Nom du champ des altitudes",
                                   "Z")

if uploaded_file is not None:
    if st.button("Importer la section !"):
        try:
            # Lire le fichier CSV avec pandas
            df = pd.read_csv(uploaded_file,
                             delimiter=delimiter,
                             decimal=separator)
            
            # Affichage du dataframe
            st.success("Géométrie chargée avec succès !")
            st.write(f"Nom du fichier téléversé : {uploaded_file.name}")
            st.dataframe(df)
        except Exception as e:
            st.error(f"Erreur lors du chargement : {e}")