import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import xarray as xr
import io

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
    "Scientific data integration in progress"
)
st.markdown("---")


st.markdown("### 🛰️ NASA Data Upload")

uploaded_file = st.file_uploader(
    "Upload your NASA Earth observation data",
    type=["nc", "csv", "zip"]
)

if uploaded_file is not None:
    st.success("NASA data file uploaded successfully!")
    st.write("File name:", uploaded_file.name)
    st.write("File size:", uploaded_file.size, "bytes")

    st.subheader("NASA Data Preview")

    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
            st.dataframe(df.head(10), use_container_width=True)
            st.success("Data processed successfully!")
        else:
            st.info("NASA file uploaded. Specialized processing will be added next.")
    except Exception as e:  
        st.error(f"Error processing file:{e}")
        st.success("Data processed successfully!")

    except Exception as e:
        st.warning("This file may not be a CSV file.")
        st.write
        (e)
        
st.divider()

st.header("🌍 TerraLens Dashboard")
st.write("NASA Earth Observation Analysis")

st.subheader("Global Earth Monitoring")

# TERRALENS INVESTIGATION CONTROLS

st.markdown("### 🌍 Select Investigation Area")

study_area = st.selectbox(
    "Choose your study region",
    [
        "Global",
        "Asia",
        "Africa",
        "Europe",
        "North America",
        "South America",
        "Oceania"
    ]
)

st.markdown("### 📅 Select Study Period")

start_year = st.selectbox(
    "Start Year",
    list(range(2001, 2027)),
    index=0
)

end_year = st.selectbox(
    "End Year",
    list(range(start_year, 2027)),
    index=len(list(range(start_year, 2027))) - 1
)

st.write("Selected Region:", study_area)
st.write("Selected Period:", start_year, "-", end_year)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Data Source", "NASA")

with col2:
    st.metric("Study Area", "Global")

with col3:
    st.metric("Status", "Awaiting Data")

st.divider()

st.subheader("🌱 NDVI Analysis")

st.info(
    "NASA vegetation data visualization "
    "will appear here after data processing."
)

st.subheader("🗺️ Global Map")
# REGIONAL INVESTIGATION MAP

region_coordinates = {
    "Global": (0, 0),
    "Asia": (34, 100),
    "Africa": (0, 20),
    "Europe": (54, 15),
    "North America": (40, -100),
    "South America": (-15, -60),
    "Oceania": (-25, 135)
}

latitude, longitude = region_coordinates[study_area]

map_data = pd.DataFrame({
    "latitude": [latitude],
    "longitude": [longitude]
})

fig = px.scatter_geo(
    map_data,
    lat="latitude",
    lon="longitude",
    projection="natural earth",
    title=f"TerraLens - {study_area} Investigation"
)

fig.update_layout(
    geo=dict(
        showland=True,
        landcolor="lightgreen",
        showocean=True,
        oceancolor="lightblue",
        showcountries=True
    )
)

st.plotly_chart(fig, use_container_width=True)



# ==================================
# TERRALENS - NASA NETCDF DATA READER
# ==================================

def load_nasa_netcdf(uploaded_file):
    try:
        file_bytes = io.BytesIO(uploaded_file.getvalue())

        dataset = xr.open_dataset(
            file_bytes,
            engine="netcdf4"
        )

        dataset.load()
        dataset.close()

        return dataset

    except Exception as e:
        st.error(f"NASA data reading error: {e}")
        return None
        
# NASA DATA UPLOAD PROCESSING

if uploaded_file is not None:
    nasa_dataset = load_nasa_netcdf(uploaded_file)

    if nasa_dataset is not None:
        st.success("NASA NetCDF data loaded successfully!")

        st.subheader("NASA Dataset Information")
        st.write("Dimensions:", nasa_dataset.sizes)
        st.write("Variables:", list(nasa_dataset.data_vars))
    

    

