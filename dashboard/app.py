import sys
import streamlit as st
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

import pandas as pd
import streamlit as st
import plotly.express as px
import folium
from streamlit_folium import st_folium
from config import DATA_PATH, MODEL_PATH
from preprocess import load_data, clean_events, build_target
from predict import predict_event

st.set_page_config(page_title="EventIQ Traffic Intelligence", layout="wide")
st.title("EventIQ: Event-Driven Congestion Forecasting")

@st.cache_data
def get_data():
    df = clean_events(load_data(DATA_PATH))
    df["congestion_proxy"] = build_target(df)
    return df

df = get_data()

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Events", len(df))
c2.metric("Planned", int((df.event_type.str.lower()=="planned").sum()))
c3.metric("Unplanned", int((df.event_type.str.lower()=="unplanned").sum()))
c4.metric("Avg Impact", round(df["congestion_proxy"].mean(), 1))

left, right = st.columns([1,1])
with left:
    st.subheader("Historical event hot spots")
    sample = df.dropna(subset=["latitude", "longitude"]).sample(min(1000, len(df)), random_state=42)
    m = folium.Map(location=[sample.latitude.mean(), sample.longitude.mean()], zoom_start=11)
    for _, r in sample.iterrows():
        folium.CircleMarker([r.latitude, r.longitude], radius=3, popup=f"{r.event_cause} | {r.priority}", fill=True).add_to(m)
    st.components.v1.html(m._repr_html_(), height=520)
with right:
    st.subheader("Event cause distribution")
    vc = df["event_cause"].value_counts().head(12).reset_index()
    vc.columns = ["event_cause", "count"]
    st.plotly_chart(px.bar(vc, x="event_cause", y="count"), use_container_width=True)

st.divider()
st.subheader("Predict New Event Impact")
with st.form("predict"):
    a,b,c = st.columns(3)
    event_type = a.selectbox("Event Type", sorted(df.event_type.dropna().unique()), index=0)
    event_cause = b.selectbox("Event Cause", sorted(df.event_cause.dropna().unique()), index=0)
    priority = c.selectbox("Priority", ["Low", "Medium", "High", "Critical"], index=2)
    a,b,c = st.columns(3)
    lat = a.number_input("Latitude", value=float(df.latitude.mean()))
    lon = b.number_input("Longitude", value=float(df.longitude.mean()))
    closure = c.checkbox("Requires Road Closure")
    a,b = st.columns(2)
    start = a.text_input("Start Datetime", "2026-06-20 17:00:00")
    end = b.text_input("End Datetime", "2026-06-20 21:00:00")
    submitted = st.form_submit_button("Forecast")

if submitted:
    if not MODEL_PATH.exists():
        st.error("Model not trained. Run: python src/train_model.py")
    else:
        event = {"event_type": event_type, "event_cause": event_cause, "latitude": lat, "longitude": lon,
                 "requires_road_closure": closure, "start_datetime": start, "end_datetime": end,
                 "priority": priority, "corridor": "unknown", "zone": "unknown", "junction": "unknown",
                 "police_station": "unknown", "veh_type": "unknown", "status": "open"}
        result = predict_event(event)
        st.json(result)
