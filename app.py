import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.set_page_config(
    page_title="TerraLens",
    page_icon="🌍",
    layout="wide"
)

st.title("🌍 TerraLens")
st.subheader("Earth System Trend Detective")

st.markdown(
    "Investigating environmental changes "
    "across our planet using Earth observation data."
)

st.info(
    "Development preview: Charts currently use "
    "illustrative data, not NASA observations."
)

st.sidebar.title("Investigation Controls")

topic = st.sidebar.selectbox(
    "Environmental parameter",
    ["Precipitation", "Temperature", "Vegetation"]
)

start_year = st.sidebar.selectbox(
    "Start year", [2001, 2005, 2010, 2015]
)

end_year = st.sidebar.selectbox(
    "End year", [2020, 2022, 2023, 2024]
)

st.markdown("### Global Investigation")

col1, col2, col3 = st.columns(3)

col1.metric("Study area", "Global")
col2.metric("Study period", f"{start_year}–{end_year}")
col3.metric("Data connection", "Pending")

st.markdown("---")

st.markdown("### Environmental Trend Preview")

years = np.arange(start_year, end_year + 1)

# Illustrative values only.
values = np.linspace(10, 15, len(years))

df = pd.DataFrame({
    "Year": years,
    "Illustrative value": values
})

fig = px.line(
    df,
    x="Year",
    y="Illustrative value",
    markers=True,
    title=f"{topic} - Interface Preview"
)

st.plotly_chart(fig, use_container_width=True)

st.warning(
    "This graph is illustrative. "
    "It must not be interpreted as a real environmental trend."
)

st.markdown("---")

st.markdown("### Our Investigation Modules")

a, b, c = st.columns(3)

a.write("🌧️ **Rainfall Analysis**")
a.caption("Investigate global precipitation patterns.")

b.write("🌡️ **Temperature Analysis**")
b.caption("Study changes in Earth's temperature.")

c.write("🌱 **Vegetation Analysis**")
c.caption("Investigate vegetation changes.")

st.markdown("---")

st.caption(
    "TerraLens | NASA Space Apps Challenge Project | "
    "Scientific data

integration in progress"

    
)
