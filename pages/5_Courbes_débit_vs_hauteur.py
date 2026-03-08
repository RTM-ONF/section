import numpy as np
import plotly.graph_objects as go
import streamlit as st


st.title("Courbes débit vs hauteur")

if "laws" not in st.session_state:
    st.session_state.laws = ["Critique", "Ferguson"]

if "height_step" not in st.session_state:
    st.session_state.height_step = 0.10

if "slope" not in st.session_state:
    st.session_state.slope = 5.

if "d84" not in st.session_state:
    st.session_state.d84 = 0.01

if "section" in st.session_state:
    section = st.session_state.section
    if section:

        def update_laws():
            st.session_state.laws = st.session_state._laws

        def update_height_step():
            st.session_state.height_step = st.session_state._height_step

        def update_slope():
            st.session_state.slope = st.session_state._slope

        def update_d84():
            st.session_state.d84 = st.session_state._d84

        laws = st.multiselect("Sélectionner les lois d'écoulement",
                              ["Critique", "Ferguson"],
                              default=st.session_state.laws,
                              key="_laws",
                              on_change=update_laws
                             )

        st.write("")

        with st.expander("Paramètres"):

            height_step = st.number_input(label="Pas de discrétisation en hauteur [m]",
                                        value=st.session_state.height_step,
                                        min_value=0.05,
                                        max_value=float(int(max(section.z) - min(section.z))),
                                        step=0.05,
                                        format="%0.2f",
                                        key="_height_step",
                                        on_change=update_height_step
                                        )

            slope = st.number_input(label="Pente [m/100m] (Ferguson)",
                                    value=st.session_state.slope,
                                    min_value=0.01,
                                    step=0.1,
                                    format="%0.2f",
                                    key="_slope",
                                    on_change=update_slope
                                    )

            d84 = st.number_input(label="D_84 [m] (Ferguson)",
                                  value=st.session_state.d84,
                                  min_value=0.001,
                                  step=0.005,
                                  format="%0.3f",
                                  key="_d84",
                                  on_change=update_d84
                                  )

        if len(laws) > 0:
            results = {
                "heights" : [0.],
                "discharges_critique" : [0.],
                "discharges_ferguson" : [0.]
            }

            dz = max(section.z) - min(section.z)
            heights = np.arange(height_step, dz, height_step)
            if dz not in heights:
                heights = np.append(heights, dz)

            for height in heights:
                if "Ferguson" in laws:
                    discharge = section.ferguson(min(section.z) + height, slope/100, d84)
                    if discharge:
                        if height not in results["heights"]:
                            results["heights"].append(height)
                        results["discharges_ferguson"].append(discharge)
                if "Critique" in laws:
                    discharge = section.critical(min(section.z) + height)
                    if discharge:
                        if height not in results["heights"]:
                            results["heights"].append(height)
                        results["discharges_critique"].append(discharge)

            fig = go.Figure()
            for law in laws:
                fig.add_trace(go.Scatter(x=results["heights"],
                                         y=results[f"discharges_{law.lower()}"],
                                         mode="lines",
                                         name=f"{law}"))

            fig.update_layout(
                xaxis=dict(
                    title="hauteur d'eau [m]"
                ),
                yaxis=dict(
                    title="débit [m<sup>3</sup>/s]"
                ),
                showlegend=True
            )

            fig.update_xaxes(showgrid=True)
            fig.update_yaxes(showgrid=True)

            st.plotly_chart(fig)

    # if st.checkbox("Afficher l'aide"):
    with st.expander("Documentation"):
        st.markdown(
            """
            $\\boxed{Q = v \\times A}$

            - Q : débit liquide ;
            - v : vitesse d'écoulement ;
            - A : surface mouillée.

            #### Régime critique

            $\\boxed{F_r = \\frac{v}{\\sqrt{g \\times D}} = 1  \\Leftrightarrow v = \\sqrt{g \\times D}}$

            $\\boxed{v = \\sqrt{g \\times D}}$

            - $v$ : vitesse d'écoulement ;
            - $g$ : accélération de la pesanteur ;
            - $D$ : profondeur hydraulique.

            #### Ferguson

            $\\boxed{\\frac{v}{\\sqrt{g J R_h}} = \\frac{2.5\\left(\\frac{R_h}{D_{84}}\\right)}{\\sqrt{1 + 0.15\\left(\\frac{R_h}{D_{84}}\\right)^{\\frac{5}{3}}}}}$

            - $v$ : vitesse d'écoulement ;
            - $g$ : accélération de la pesanteur ;
            - $J$ : pente ;
            - $R_h$ : rayon hydraulique ;
            - $D_{84}$ : diamètre caractéristique.
            """
        )

