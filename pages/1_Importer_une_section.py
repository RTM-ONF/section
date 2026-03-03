import pandas as pd
import streamlit as st

from section.section import Section

st.title("Importer une section")

if "section" not in st.session_state:
    st.session_state.section = None

if "uploaded_file" not in st.session_state:
    st.session_state.uploaded_file = None

uploaded_file = st.file_uploader(
    "Téléverser ici le fichier contenant la géométrie de la section"
    )

col1, col2 = st.columns(2)

delimiters = {"\t" : "tabulation" ,
              " " : "espace",
              ";" : "point-virgule",
              "," : "virgule"}

if "delimiter" not in st.session_state:
    st.session_state.delimiter = "\t"

if "distance_field" not in st.session_state:
    st.session_state.distance_field = "X"

with col1:
    delimiter = st.selectbox("Délimiteur",
                             options=delimiters.keys(),
                             format_func=lambda x : delimiters[x],
                             index=list(delimiters.keys()).index(st.session_state.delimiter)
                             )

    distance_field = st.text_input("Nom du champ des distances",
                                   st.session_state.distance_field)

if "separator" not in st.session_state:
    st.session_state.separator = "."

if "altitude_field" not in st.session_state:
    st.session_state.altitude_field = "Z"

separators = {"." : "point",
              "," : "virgule"}

with col2:
    separator = st.selectbox("Séparateur décimal",
                             options=separators.keys(),
                             format_func=lambda x : separators[x],
                             index=list(separators.keys()).index(st.session_state.separator)
                             )

    altitude_field = st.text_input("Nom du champ des altitudes",
                                   st.session_state.altitude_field)

st.write("")

if st.button("Importer la section !"):
    st.session_state.uploaded_file = uploaded_file
    st.session_state.delimiter = delimiter
    st.session_state.separator = separator
    st.session_state.distance_field = distance_field
    st.session_state.altitude_field = altitude_field

    try:
        df = pd.read_csv(uploaded_file,
                         delimiter=delimiter,
                         decimal=separator)
    except:
        df = None

    section = Section()
    if section.from_df(df, x_field=distance_field, z_field=altitude_field):
        st.success("Géométrie chargée avec succès !")
        st.session_state.section = section
    else:
        st.error("Fichier ou géométrie non conforme.")
        st.session_state.section = None

if st.session_state.section:
    st.write(f"Nom du fichier téléversé : {st.session_state.uploaded_file.name}")