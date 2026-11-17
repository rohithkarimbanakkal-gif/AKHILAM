import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import xarray as xr
import io
import folium
from streamlit_folium import st_folium
from streamlit_geolocation import streamlit_geolocation

st.set_page_config(
    page_title="TerraLens",
    page_icon="🌍",
    layout="wide"
)

st.title("AKHILAM")
st.subheader("🗺️ AKHILAM Smart Navigation")

from geopy.geocoders import Nominatim

with st.form("akhilam_search"):
    place_name = st.text_input(
        "🔍 Search any place in India",
        placeholder="Example: Kochi, Kerala"
    )

    search_button = st.form_submit_button(
        "ENTER",
        type="primary",
        use_container_width=True
    )

# Get device location
st.write("📍 **Find My Live Location**")

location = streamlit_geolocation()
st.write("GPS DEBUG:", location)

live_location = None

if isinstance(location, dict):
    if location.get("latitude") is not None and location.get("longitude") is not None:
        live_location = (
            location["latitude"],
            location["longitude"]
        )

# Search location
# Search location
if "search_location" not in st.session_state:
    st.session_state.search_location = None

if search_button and place_name:
    try:
        geolocator = Nominatim(
            user_agent="akhilam_navigation"
        )

        found_location = geolocator.geocode(
            place_name + ", India",
            timeout=20
        )

        st.session_state.search_location = found_location

    except Exception as e:
        st.error(f"Location search error: {e}")

search_location = st.session_state.search_location
# Select map position
if search_location:
    map_lat = search_location.latitude
    map_lon = search_location.longitude
    map_zoom = 12
    st.success(f"Location found: {search_location.address}")

elif live_location:
    map_lat, map_lon = live_location
    map_zoom = 14
    st.success("Your live location is available!")

else:
    map_lat = 10.8505
    map_lon = 76.2711
    map_zoom = 7


# Create map
akhilam_map = folium.Map(
    location=[map_lat, map_lon],
    zoom_start=map_zoom
)

# Show live location with directional arrow
if live_location:
    live_marker = folium.Marker(
        live_location,
        popup="Your Current Location",
        tooltip="Your Direction",
        icon=folium.DivIcon(
            html="""
            <div class="akhilam-heading-arrow"
                 style="width:40px;height:40px;
                 transform:rotate(0deg);
                 transform-origin:center;">
                <svg width="40" height="40"
                     viewBox="0 0 40 40">
                    <path
                        d="M20 2 L36 38 L20 29 L4 38 Z"
                        fill="#1677ff"
                        stroke="white"
                        stroke-width="2"
                        stroke-linejoin="round"
                    />
                </svg>
            </div>
            """,
            icon_size=(40, 40),
            icon_anchor=(20, 20)
        )
    ).add_to(akhilam_map)
        from branca.element import Element

    compass_html = f"""
    <div id="akhilam-compass-panel"
         style="position:fixed;top:12px;left:55px;
         z-index:99999;background:white;padding:10px;
         border-radius:10px;box-shadow:0 2px 8px #888;
         font-family:Arial;">

        <button id="akhilam-enable-compass"
                type="button"
                style="background:#1677ff;color:white;
                border:none;padding:10px 15px;
                border-radius:8px;font-weight:bold;">
            Enable Compass
        </button>

        <div id="akhilam-compass-status"
             style="font-size:12px;margin-top:6px;color:#333;">
            Compass not enabled
        </div>
    </div>

    <script>
    window.addEventListener("load", function() {{

        const marker = {live_marker.get_name()};
        const button = document.getElementById(
            "akhilam-enable-compass"
        );
        const status = document.getElementById(
            "akhilam-compass-status"
        );

        let absoluteHeadingSeen = false;
        let gotReading = false;
        let started = false;

        function updateHeading(event) {{

            let heading = null;

            const isAbsolute =
                event.absolute === true ||
                event.type === "deviceorientationabsolute" ||
                typeof event.webkitCompassHeading === "number";

            if (absoluteHeadingSeen && !isAbsolute) {{
                return;
            }}

            if (isAbsolute) {{
                absoluteHeadingSeen = true;
            }}

            if (
                typeof event.webkitCompassHeading === "number"
            ) {{
                heading = event.webkitCompassHeading;

            }} else if (
                typeof event.alpha === "number"
            ) {{
                heading = (360 - event.alpha + 360) % 360;
            }}

            if (heading === null) {{
                return;
            }}

            gotReading = true;

            const element = marker.getElement();

            if (!element) {{
                status.textContent = "Compass reading received.";
                return;
            }}

            const arrow = element.querySelector(
                ".akhilam-heading-arrow"
            );

            if (arrow) {{
                arrow.style.transform =
                    "rotate(" + heading + "deg)";
            }}

            status.textContent =
                "Compass: " + Math.round(heading) + "°" +
                (isAbsolute ? " (Absolute)" : " (Relative)");
        }}

        async function enableCompass() {{

            if (started) return;

            try {{

                if (!window.isSecureContext) {{
                    status.textContent =
                        "HTTPS connection required.";
                    return;
                }}

                if (!("DeviceOrientationEvent" in window)) {{
                    status.textContent =
                        "Orientation sensor not supported.";
                    return;
                }}

                if (
                    typeof DeviceOrientationEvent.requestPermission
                    === "function"
                ) {{
                    const permission =
                        await DeviceOrientationEvent.requestPermission();

                    if (permission !== "granted") {{
                        status.textContent =
                            "Compass permission denied.";
                        return;
                    }}
                }}

                started = true;

                window.addEventListener(
                    "deviceorientation",
                    updateHeading,
                    true
                );

                window.addEventListener(
                    "deviceorientationabsolute",
                    updateHeading,
                    true
                );

                status.textContent =
                    "Waiting for compass sensor...";

                button.textContent = "Compass Enabled";

                window.setTimeout(function() {{
                    if (!gotReading) {{
                        status.textContent =
                            "No compass readings received.";
                    }}
                }}, 5000);

            }} catch (error) {{

                status.textContent =
                    "Compass error: " + error.message;

            }}
        }}

        button.addEventListener("click", enableCompass);

    }});
    </script>
    """

    akhilam_map.get_root().html.add_child(
        Element(compass_html)
)

# Show searched destination
if search_location:
    destination = (
        search_location.latitude,
        search_location.longitude
    )

    folium.Marker(
        destination,
        popup=place_name,
        tooltip="Destination",
        icon=folium.Icon(color="red")
    ).add_to(akhilam_map)

# Route calculation function
@st.cache_data(ttl=300)
def get_akhilam_route(start_lat, start_lon, end_lat, end_lon):
    import json
    from urllib.request import Request, urlopen

    route_url = (
        "https://router.project-osrm.org/route/v1/driving/"
        f"{start_lon},{start_lat};{end_lon},{end_lat}"
        "?overview=full&geometries=geojson"
    )

    request = Request(
        route_url,
        headers={"User-Agent": "AKHILAM/1.0"}
    )

    with urlopen(request, timeout=20) as response:
        return json.loads(response.read().decode("utf-8"))

# Draw route
if live_location and search_location:
    try:
        route_data = get_akhilam_route(
            live_location[0],
            live_location[1],
            destination[0],
            destination[1]
        )

        if route_data.get("code") == "Ok" and route_data.get("routes"):
            route = route_data["routes"][0]

            coordinates = route["geometry"]["coordinates"]

            route_points = [
                [lat, lon] for lon, lat in coordinates
            ]

            folium.PolyLine(
                route_points,
                color="blue",
                weight=6,
                tooltip="AKHILAM Driving Route"
            ).add_to(akhilam_map)

            akhilam_map.fit_bounds([
                live_location,
                destination
            ])

            st.success(
                f"Distance: {route['distance'] / 1000:.2f} km"
            )

            st.info(
                f"Estimated travel time: "
                f"{route['duration'] / 60:.0f} minutes"
            )

        else:
            st.warning("No driving route was found.")

    except Exception:
        st.warning("Route service unavailable. Please try again.")

elif not live_location:
    st.info("Tap the location symbol to get your starting point.")
    # AKHILAM Journey Controls

if live_location and search_location:

    if "journey_started" not in st.session_state:
        st.session_state.journey_started = False

    if not st.session_state.journey_started:

        if st.button("▶ Start Journey", type="primary"):
            st.session_state.journey_started = True
            st.rerun()

    else:
        st.success("🟢 Your journey has started!")

        st.write("📍 Destination:", place_name)

        if st.button("⏹ Stop Journey"):
            st.session_state.journey_started = False
            st.rerun()

st_folium(
    akhilam_map,
    width=700,
    height=450
        )
st.subheader("Earth System Trend Detective")
st.caption("Earth Observation & Analysis Platform")

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

st.markdown("### 🌿 Vegetation Health Analysis")

st.write(
    "Analyze vegetation conditions using "
    "NASA MODIS satellite observations."
)

ndvi_min = st.slider(
    "Minimum NDVI",
    min_value=-1.0,
    max_value=1.0,
    value=0.2,
    step=0.1
)

ndvi_max = st.slider(
    "Maximum NDVI",
    min_value=-1.0,
    max_value=1.0,
    value=0.8,
    step=0.1
)

st.write("Selected NDVI Range:", ndvi_min, "to", ndvi_max)

st.info(
    "Upload a processed NASA MODIS vegetation dataset "
    "to begin actual NDVI analysis."
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

# AKHILAM INTERACTIVE REGIONAL MAP

latitude, longitude = region_coordinates[study_area]

# AKHILAM REGIONAL MAP

earth_map = folium.Map(
    location=[latitude, longitude],
    zoom_start=2,
    tiles="OpenStreetMap"
)

if study_area == "Asia":
    earth_map.fit_bounds([
        [-10, 60],
        [65, 150]
    ])

elif study_area == "Africa":
    earth_map.fit_bounds([
        [-40, -20],
        [40, 55]
    ])

elif study_area == "Europe":
    earth_map.fit_bounds([
        [30, -15],
        [75, 45]
    ])

elif study_area == "North America":
    earth_map.fit_bounds([
        [5, -170],
        [85, -50]
    ])

elif study_area == "South America":
    earth_map.fit_bounds([
        [-60, -85],
        [15, -30]
    ])

elif study_area == "Oceania":
    earth_map.fit_bounds([
        [-50, 110],
        [0, 180]
    ])

folium.Marker(
    [latitude, longitude],
    popup=f"AKHILAM - {study_area}"
).add_to(earth_map)

st_folium(
    earth_map,
    width=700,
    height=500,
    key=f"map_{study_area}"
)


# ==================================
# TERRALENS - NASA NETCDF DATA READER
# ==================================

def load_nasa_netcdf(uploaded_file):
    try:
        file_bytes = uploaded_file.getvalue()

        dataset = xr.open_dataset(
            io.BytesIO(file_bytes),
            engine="h5netcdf"
        )

        dataset.load()
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

        st.subheader("NASA Data Variables")

        for variable in nasa_dataset.data_vars:
            st.write(variable)

        st.subheader("NASA Data Preview")

        for variable in nasa_dataset.data_vars:
            st.write(f"Preview of {variable}")
            st.write(nasa_dataset[variable].values[:5])

