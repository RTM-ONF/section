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

st.write("")

# if st.checkbox("Afficher l'aide"):
with st.expander("Documentation"):
    st.markdown(
        """
        Le fichier contenant la géométrie de la section doit comporter, au minimum, deux colonnes (avec en-tête) indiquant les valeurs de distance et d’altitude (en mètres).

        Exemple :
        ```
        X	Z
        0.00	548.60
        1.07	548.60
        2.13	548.62
        3.20	548.21
        4.27	547.25
        5.33	546.43
        6.40	545.76
        7.47	545.50
        8.53	545.22
        9.60	544.98
        10.67	544.77
        11.73	544.86
        12.80	545.16
        13.87	545.76
        14.93	546.17
        16.00	546.77
        17.07	547.23
        18.13	547.71
        19.20	548.29
        20.27	548.92
        21.33	549.55
        22.40	550.38
        23.47	550.84
        24.54	550.42
        25.60	550.38
        26.67	550.36
        ```
        """
    )