from math import ceil

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

st.title("Propriétés géométriques")

if "water_height" not in st.session_state:
    st.session_state.water_height = 0.

if "section" in st.session_state:
    section = st.session_state.section
    if section:

        def update():
            st.session_state.water_height = st.session_state._water_height
        
        water_height = st.number_input(label="Hauteur d'eau [m]",
                                       value=st.session_state.water_height,
                                       min_value=0.,
                                       max_value=float(ceil(max(section.z)-min(section.z))),
                                       step=0.001,
                                       format="%0.3f",
                                       key="_water_height",
                                       on_change=update
                                       )

        st.write(f"Altitude de la ligne d'eau : {round(min(section.z) + water_height, 3)} m")
        
        water_lines = section.water_lines(min(section.z) + water_height)

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=section.x,
                                y=section.z,
                                mode="lines",
                                name="section",
                                ))

        for line in water_lines:
            fig.add_trace(go.Scatter(x=[x for x, z in line],
                                    y=[z for x, z in line],
                                    mode="lines",
                                    name=f"ligne d'eau",
                                    ))

        fig.update_layout(xaxis_title="distance [m]",
                        yaxis_title="altitude [m]",
                        yaxis_scaleanchor="x",
                        showlegend=True
                        )

        fig.update_xaxes(showgrid=True)
        fig.update_yaxes(showgrid=True)

        st.plotly_chart(fig)

        geom_props = section.geometric_properties(min(section.z) + water_height)

        if geom_props:
            B, P, A, R, D = geom_props

            data = {
                "Grandeur" : ["largeur au miroir [m]",
                              "périmètre mouillé [m]",
                              "surface mouillée [m²]",
                              "rayon hydraulique [m]",
                              "profondeur hydraulique [m]"],
                "Valeur" : [round(B, 3),
                            round(P, 3),
                            round(A, 3),
                            round(R, 3),
                            round(D, 3)]
            }

            st.dataframe(pd.DataFrame(data), hide_index=True)