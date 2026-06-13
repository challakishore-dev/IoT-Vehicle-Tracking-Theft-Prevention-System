
import streamlit as st
import pandas as pd
import math
from datetime import datetime

st.set_page_config(page_title="IoT Vehicle Tracking & Theft Prevention", layout="wide")

SAFE_LAT = 16.5062
SAFE_LON = 80.6480
GEOFENCE_KM = 2

def distance_km(lat1, lon1, lat2, lon2):
    r = 6371
    dlat = math.radians(lat2-lat1)
    dlon = math.radians(lon2-lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1))*math.cos(math.radians(lat2))*math.sin(dlon/2)**2
    return r * (2 * math.atan2(math.sqrt(a), math.sqrt(1-a)))

st.title("IoT Vehicle Tracking & Theft Prevention System")

lat = st.number_input("Latitude", value=16.5062)
lon = st.number_input("Longitude", value=80.6480)
speed = st.slider("Speed (km/h)", 0, 150, 0)

dist = distance_km(lat, lon, SAFE_LAT, SAFE_LON)
status = "SAFE"
if dist > GEOFENCE_KM:
    status = "GEOFENCE ALERT"

if speed > 5 and dist > GEOFENCE_KM:
    status = "THEFT SUSPECTED"

st.metric("Distance From Safe Zone (km)", round(dist, 2))
st.metric("Vehicle Status", status)

maps_url = f"https://maps.google.com/?q={lat},{lon}"
st.write("Google Maps:", maps_url)

data = pd.DataFrame([{
    "timestamp": datetime.now(),
    "latitude": lat,
    "longitude": lon,
    "speed": speed,
    "status": status
}])

st.dataframe(data, use_container_width=True)
st.map(pd.DataFrame({"lat":[lat],"lon":[lon]}))
