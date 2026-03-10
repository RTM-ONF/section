from math import ceil

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st


@st.cache_data
def convert_for_download(d):
    csv = pd.DataFrame(d).to_csv(index=False, sep=";")
    return csv.encode("utf-8-sig")


st.title("Ecoulements liquides")

if "laws" not in st.session_state:
    st.session_state.laws = ["Critique", "Ferguson", "Strickler"]

if "height_step" not in st.session_state:
    st.session_state.height_step = 0.10

if "slope" not in st.session_state:
    st.session_state.slope = 6.

if "d84" not in st.session_state:
    st.session_state.d84 = 0.10

if "strickler_coef" not in st.session_state:
    st.session_state.strickler_coef = 25.

if "results" not in st.session_state:
    st.session_state.results = dict({})

if "water_height" not in st.session_state:
    st.session_state.water_height = 0.

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

        def update_strickler_coef():
            st.session_state.strickler_coef = st.session_state._strickler_coef

        laws = st.multiselect("Sélectionner les lois d'écoulement",
                              ["Critique", "Ferguson", "Strickler"],
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

            slope = st.number_input(label="Pente [%] (Ferguson, Strickler)",
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

            strickler_coef = st.number_input(label="Coefficient de Strickler [$m^{1/3}.s^{-1}$] (Strickler)",
                                             value=st.session_state.strickler_coef,
                                             min_value=1.,
                                             max_value=100.,
                                             step=0.1,
                                             format="%0.1f",
                                             key="_strickler_coef",
                                             on_change=update_strickler_coef
                                             )

        if len(laws) > 0:
            dz = max(section.z) - min(section.z)
            heights = np.arange(height_step, dz, height_step)
            if dz not in heights:
                heights = np.append(heights, dz)

            n = len(heights)

            st.session_state.results = dict({})
            st.session_state.results["hauteur [m]"] = [0.]
            st.session_state.results["altitude [m]"] = [round(min(section.z), 3)]
            st.session_state.results["pente [%]"] = [round(slope, 3)]
            st.session_state.results["d84 [m]"] = [round(d84, 3)]
            st.session_state.results["coefficient de Strickler [m^(1/3)/s]"] = [round(strickler_coef, 3)]
            st.session_state.results["largeur au miroir [m]"] = [0.]
            st.session_state.results["périmètre mouillé [m]"] = [0.]
            st.session_state.results["surface mouillée [m²]"] = [0.]
            st.session_state.results["rayon hydraulique [m]"] = [0.]
            st.session_state.results["profondeur hydraulique [m]"] = [0.]
            st.session_state.results["contrainte hydraulique [Pa]"] = [0.]

            st.session_state.results["vitesse Critique [m/s]"] = [0.]
            st.session_state.results["débit Critique [m^3/s]"] = [0.]
            st.session_state.results["charge spécifique Critique [m]"] = [0.]
            st.session_state.results["charge Critique [m]"] = [0.]
            

            st.session_state.results["vitesse Ferguson [m/s]"] = [0.]
            st.session_state.results["débit Ferguson [m^3/s]"] = [0.]
            st.session_state.results["charge spécifique Ferguson [m]"] = [0.]
            st.session_state.results["charge Ferguson [m]"] = [0.]


            st.session_state.results["vitesse Strickler [m/s]"] = [0.]
            st.session_state.results["débit Strickler [m^3/s]"] = [0.]
            st.session_state.results["charge spécifique Strickler [m]"] = [0.]
            st.session_state.results["charge Strickler [m]"] = [0.]

            for height in heights:
                height = float(height)
                geom_props = section.geometric_properties(min(section.z) + height)
                
                if geom_props:
                    B, P, A, R, D = geom_props
                    st.session_state.results["hauteur [m]"].append(round(height, 3))
                    st.session_state.results["altitude [m]"].append(round(min(section.z) + height, 3))
                    st.session_state.results["pente [%]"].append(round(slope, 3))
                    st.session_state.results["d84 [m]"].append(round(d84, 3))
                    st.session_state.results["coefficient de Strickler [m^(1/3)/s]"].append(round(strickler_coef, 3))
                    st.session_state.results["largeur au miroir [m]"].append(round(B, 3))
                    st.session_state.results["périmètre mouillé [m]"].append(round(P, 3))
                    st.session_state.results["surface mouillée [m²]"].append(round(A, 3))
                    st.session_state.results["rayon hydraulique [m]"].append(round(R, 3))
                    st.session_state.results["profondeur hydraulique [m]"].append(round(D, 3))
                    st.session_state.results["contrainte hydraulique [Pa]"].append(round(1000. * 9.81 * R * slope/100, 3))
                else:
                    continue

                if "Critique" in laws:
                    critical = section.critical(min(section.z) + height)
                    if critical:
                        v, Q = critical
                        st.session_state.results["vitesse Critique [m/s]"].append(round(v, 3))
                        st.session_state.results["débit Critique [m^3/s]"].append(round(Q, 3))
                        st.session_state.results["charge spécifique Critique [m]"].append(round(height + v**2 / (2. * 9.81), 3))
                        st.session_state.results["charge Critique [m]"].append(round(min(section.z) + height + v**2 / (2. * 9.81), 3))

                    else:
                        st.session_state.results["vitesse Critique [m/s]"].append(0.)
                        st.session_state.results["débit Critique [m^3/s]"].append(0.)
                        st.session_state.results["charge spécifique Critique [m]"].append(0.)
                        st.session_state.results["charge Critique [m]"].append(0.)

                else:
                    st.session_state.results["vitesse Critique [m/s]"].append(0.)
                    st.session_state.results["débit Critique [m^3/s]"].append(0.)
                    st.session_state.results["charge spécifique Critique [m]"].append(0.)
                    st.session_state.results["charge Critique [m]"].append(0.)


                if "Ferguson" in laws:
                    ferguson = section.ferguson(min(section.z) + height, slope/100., d84)
                    if ferguson:
                        v, Q = ferguson
                        st.session_state.results["vitesse Ferguson [m/s]"].append(round(v, 3))
                        st.session_state.results["débit Ferguson [m^3/s]"].append(round(Q, 3))
                        st.session_state.results["charge spécifique Ferguson [m]"].append(round(height + v**2 / (2. * 9.81), 3))
                        st.session_state.results["charge Ferguson [m]"].append(round(min(section.z) + height + v**2 / (2. * 9.81), 3))

                    else:
                        st.session_state.results["vitesse Ferguson [m/s]"].append(0.)
                        st.session_state.results["débit Ferguson [m^3/s]"].append(0.)
                        st.session_state.results["charge spécifique Ferguson [m]"].append(0.)
                        st.session_state.results["charge Ferguson [m]"].append(0.)

                else:
                    st.session_state.results["vitesse Ferguson [m/s]"].append(0.)
                    st.session_state.results["débit Ferguson [m^3/s]"].append(0.)
                    st.session_state.results["charge spécifique Ferguson [m]"].append(0.)
                    st.session_state.results["charge Ferguson [m]"].append(0.)

                if "Strickler" in laws:
                    strickler = section.strickler(min(section.z) + height, slope/100., strickler_coef)
                    if strickler:
                        v, Q = strickler
                        st.session_state.results["vitesse Strickler [m/s]"].append(round(v, 3))
                        st.session_state.results["débit Strickler [m^3/s]"].append(round(Q, 3))
                        st.session_state.results["charge spécifique Strickler [m]"].append(round(height + v**2 / (2. * 9.81), 3))
                        st.session_state.results["charge Strickler [m]"].append(round(min(section.z) + height + v**2 / (2. * 9.81), 3))

                    else:
                        st.session_state.results["vitesse Strickler [m/s]"].append(0.)
                        st.session_state.results["débit Strickler [m^3/s]"].append(0.)
                        st.session_state.results["charge spécifique Strickler [m]"].append(0.)
                        st.session_state.results["charge Strickler [m]"].append(0.)

                else:
                    st.session_state.results["vitesse Strickler [m/s]"].append(0.)
                    st.session_state.results["débit Strickler [m^3/s]"].append(0.)
                    st.session_state.results["charge spécifique Strickler [m]"].append(0.)
                    st.session_state.results["charge Strickler [m]"].append(0.)

            st.subheader("Courbe Q = f(h)")

            fig = go.Figure()
            for law in laws:
                fig.add_trace(go.Scatter(x=st.session_state.results["hauteur [m]"],
                                         y=st.session_state.results[f"débit {law} [m^3/s]"],
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

            st.subheader("Courbe v = f(Q)")

            fig = go.Figure()
            for law in laws:
                fig.add_trace(go.Scatter(x=st.session_state.results[f"débit {law} [m^3/s]"],
                                        y=st.session_state.results[f"vitesse {law} [m/s]"],
                                        mode="lines",
                                        name=f"{law}"))

            fig.update_layout(
                xaxis=dict(
                    title="débit [m<sup>3</sup>/s]"
                ),
                yaxis=dict(
                    title="vitesse [m/s]"
                ),
                showlegend=True
            )

            fig.update_xaxes(showgrid=True)
            fig.update_yaxes(showgrid=True)

            st.plotly_chart(fig)

            st.subheader("Courbe $\\tau$ = f(Q)")

            fig = go.Figure()
            for law in laws:
                fig.add_trace(go.Scatter(x=st.session_state.results[f"débit {law} [m^3/s]"],
                                        y=st.session_state.results["contrainte hydraulique [Pa]"],
                                        mode="lines",
                                        name=f"{law}"))

            fig.update_layout(
                xaxis=dict(
                    title="débit [m<sup>3</sup>/s]"
                ),
                yaxis=dict(
                    title="contrainte hydraulique [Pa]"
                ),
                showlegend=True
            )

            fig.update_xaxes(showgrid=True)
            fig.update_yaxes(showgrid=True)

            st.plotly_chart(fig)

            csv = convert_for_download(st.session_state.results)

            st.download_button(label="Télécharger tous les résultats dans un fichier .csv",
                               data=csv,
                               file_name="irregular_section_results.csv"
                               )

        st.header("Interpolation")

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

        geom_props = section.geometric_properties(min(section.z) + water_height)
                
        if geom_props:
            B, P, A, R, D = geom_props
            st.write(f"Contrainte hydraulique : {round(1000. * 9.81 * R * slope/100, 3)} Pa")

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

        if len(laws) > 0:
            data = {
                "Grandeur" : ["vitesse [m/s]",
                              "débit [m^3/s]",
                              "charge spécifique [m]",
                              "charge [m]"]
                              }

            if "Critique" in laws:
                v = float(np.interp(water_height, st.session_state.results["hauteur [m]"], st.session_state.results["vitesse Critique [m/s]"], left=np.nan, right=np.nan))
                Q = float(np.interp(water_height, st.session_state.results["hauteur [m]"], st.session_state.results["débit Critique [m^3/s]"], left=np.nan, right=np.nan))
                Hs = float(np.interp(water_height, st.session_state.results["hauteur [m]"], st.session_state.results["charge spécifique Critique [m]"], left=np.nan, right=np.nan))
                H = float(np.interp(water_height, st.session_state.results["hauteur [m]"], st.session_state.results["charge Critique [m]"], left=np.nan, right=np.nan))
                data["Critique"] = [round(v, 3), round(Q, 3), round(Hs, 3), round(H, 3)]

            if "Ferguson" in laws:
                v = float(np.interp(water_height, st.session_state.results["hauteur [m]"], st.session_state.results["vitesse Ferguson [m/s]"], left=np.nan, right=np.nan))
                Q = float(np.interp(water_height, st.session_state.results["hauteur [m]"], st.session_state.results["débit Ferguson [m^3/s]"], left=np.nan, right=np.nan))
                Hs = float(np.interp(water_height, st.session_state.results["hauteur [m]"], st.session_state.results["charge spécifique Ferguson [m]"], left=np.nan, right=np.nan))
                H = float(np.interp(water_height, st.session_state.results["hauteur [m]"], st.session_state.results["charge Ferguson [m]"], left=np.nan, right=np.nan))
                data["Ferguson"] = [round(v, 3), round(Q, 3), round(Hs, 3), round(H, 3)]

            if "Strickler" in laws:
                v = float(np.interp(water_height, st.session_state.results["hauteur [m]"], st.session_state.results["vitesse Strickler [m/s]"], left=np.nan, right=np.nan))
                Q = float(np.interp(water_height, st.session_state.results["hauteur [m]"], st.session_state.results["débit Strickler [m^3/s]"], left=np.nan, right=np.nan))
                Hs = float(np.interp(water_height, st.session_state.results["hauteur [m]"], st.session_state.results["charge spécifique Strickler [m]"], left=np.nan, right=np.nan))
                H = float(np.interp(water_height, st.session_state.results["hauteur [m]"], st.session_state.results["charge Strickler [m]"], left=np.nan, right=np.nan))
                data["Strickler"] = [round(v, 3), round(Q, 3), round(Hs, 3), round(H, 3)]

            st.dataframe(pd.DataFrame(data),
                         hide_index=True)

    # if st.checkbox("Afficher l'aide"):
    with st.expander("Documentation"):
        st.markdown(
            """
            #### Contrainte hydraulique

            $\\boxed{\\tau = \\rho \\times g \\times R_h \\times J}$

            - $\\tau$ : contrainte hydraulique [$Pa$] ;
            - $\\rho$ : masse volumique de l'eau [$kg/m^3$] ;
            - $g$ : accélération de la pesanteur [$m/s^2$] ;
            - $R_h$ : rayon hydraulique [$m$] ;
            - $J$ : pente.

            #### Débit liquide

            $\\boxed{Q = v \\times A}$

            - $Q$ : débit liquide [$m^3/s$] ;
            - $v$ : vitesse d'écoulement [$m/s$] ;
            - $A$ : surface mouillée [$m^2$].

            #### Charge spécifique

            $\\boxed{H_s = h + \\frac{v^2}{2 \\times g}}$

            - $H_s$ : charge spécifique [$m$] ;
            - $h$ : hauteur d'eau [$m$] ;
            - $v$ : vitesse d'écoulement [$m/s$] ;
            - $g$ : accélération de la pesanteur [$m/s^2$].

            #### Charge

            $\\boxed{H = z_{min} + h + \\frac{v^2}{2 \\times g}}$

            - $H$ : charge [$m$] ;
            - $z_{min}$ : altitude min de la section [$m$] ;
            - $h$ : hauteur d'eau [$m$] ;
            - $v$ : vitesse d'écoulement [$m/s$] ;
            - $g$ : accélération de la pesanteur [$m/s^2$].

            #### Régime critique

            $\\boxed{F_r = \\frac{v}{\\sqrt{g \\times D}} = 1  \\Leftrightarrow v = \\sqrt{g \\times D}}$

            $\\boxed{v = \\sqrt{g \\times D}}$

            - $v$ : vitesse d'écoulement [$m/s$] ;
            - $g$ : accélération de la pesanteur [$m/s^2$] ;
            - $D$ : profondeur hydraulique [$m$].

            #### Ferguson

            $\\boxed{\\frac{v}{\\sqrt{g J R_h}} = \\frac{2.5\\left(\\frac{R_h}{D_{84}}\\right)}{\\sqrt{1 + 0.15\\left(\\frac{R_h}{D_{84}}\\right)^{\\frac{5}{3}}}}}$

            - $v$ : vitesse d'écoulement [$m/s$] ;
            - $g$ : accélération de la pesanteur [$m/s^2$] ;
            - $J$ : pente ;
            - $R_h$ : rayon hydraulique [$m$] ;
            - $D_{84}$ : diamètre caractéristique [$m$].

            #### Strickler

            $\\boxed{v = K \\times R_h^{\\frac{2}{3}} \\times J^{\\frac{1}{2}}}$

            - $v$ : vitesse d'écoulement [$m/s$] ;
            - $K$ : coefficient de Strickler [$m^{\\frac{1}{3}}/s$] ;
            - $R_h$ : rayon hydraulique [$m$] ;
            - $J$ : pente.

            """
        )

