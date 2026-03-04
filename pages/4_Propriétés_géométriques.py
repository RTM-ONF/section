from math import ceil
import plotly.graph_objects as go
import streamlit as st

st.title("Propriétés géométriques")

if "water_height" not in st.session_state:
    st.session_state.water_height = 0.

if "section" in st.session_state:
    section = st.session_state.section
    if section:
        
        water_height = st.number_input(label="Hauteur d'eau [m]",
                                       value=st.session_state.water_height,
                                       min_value=0.,
                                       max_value=float(ceil(max(section.z)-min(section.z))),
                                       step=0.001,
                                       format="%0.3f"
                                       )
        
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
                                    name=f"water line (h = {water_height} m)",
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

            st.markdown(f"""
            | Grandeur               | Valeur                       |
            |------------------------|------------------------------|
            | Largeur au miroir      | {round(B, 3)} m              |
            | Périmètre mouillé      | {round(P, 3)} m              |
            | Surface mouillée       | {round(A, 3)} m²              |
            | Rayon hydraulique      | {round(R, 3)} m              |
            | Profondeur hydraulique | {round(D, 3)} m              |

            """)

    if st.button("Enregistrer les paramètres"):
        st.session_state.water_height = water_height