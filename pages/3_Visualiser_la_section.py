import plotly.graph_objects as go
import streamlit as st

st.title("Visualiser la section")

if "section" in st.session_state:
    section = st.session_state.section
    if section:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=section.x,
                                 y=section.z,
                                 mode="lines")
                                 )

        fig.update_layout(
            xaxis_title="distance [m]",
            yaxis_title="altitude [m]",
            yaxis_scaleanchor="x"
        )

        fig.update_xaxes(showgrid=True)
        fig.update_yaxes(showgrid=True)

        st.plotly_chart(fig)

