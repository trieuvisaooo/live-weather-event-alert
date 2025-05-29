import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import os
import plotly.express as px
import plotly.graph_objects as go
from dotenv import load_dotenv

# App config
st.set_page_config(page_title="🌤️ Weather Alert Dashboard", layout="wide")

# DB connection
db_url = f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@db:5432/{os.getenv('POSTGRES_DB')}"
engine = create_engine(db_url)

# Cached data loader
@st.cache_data(ttl=300)
def load_data(limit=1000):
    query = f"""
        SELECT * FROM weather_alerts 
        ORDER BY timestamp DESC 
        LIMIT {limit}
    """
    df = pd.read_sql(query, con=engine)
    # df['datetime'] = pd.to_datetime(df['timestamp'], unit='s')
    df['datetime'] = pd.to_datetime(df['timestamp'], unit='s', utc=True).dt.tz_convert('Asia/Ho_Chi_Minh') # convert to local timezone
    return df

df = load_data()

# Sidebar filters
st.sidebar.header("🔍 Filters")
cities = df['city'].dropna().unique().tolist()
selected_cities = st.sidebar.multiselect("Cities", cities, default=cities)

metrics = ['temperature', 'humidity', 'wind_speed']
selected_metric = st.sidebar.selectbox("Metric to Analyze", metrics, index=0)

date_range = st.sidebar.date_input("Date Range", [])
if len(date_range) == 2:
    start_date, end_date = date_range
    df = df[(df['datetime'].dt.date >= start_date) & (df['datetime'].dt.date <= end_date)]

df = df[df['city'].isin(selected_cities)]

# Main dashboard
st.title("🌤️ Real-Time Weather Alert Dashboard")
st.markdown("Visual insights on recent weather conditions and active alerts.")

# KPI cards
kpi1, kpi2, kpi3 = st.columns(3)
with kpi1:
    st.metric("Total Records", len(df))
with kpi2:
    st.metric("Avg Temperature (°C)", f"{df['temperature'].mean():.2f}")
with kpi3:
    st.metric("Alerts Active", df['is_alert'].sum())

# Chart section
st.markdown(f"## 📈 {selected_metric.replace('_', ' ').title()} Trend Over Time")
if df.empty:
    st.info("No data available for the selected filters.")
else:
    fig = px.line(df.sort_values('datetime'), x='datetime', y=selected_metric, color='city',
                  title=f"{selected_metric.replace('_', ' ').title()} Over Time", markers=True)
    fig.update_layout(xaxis_title="Time", yaxis_title=selected_metric.replace('_', ' °').title())
    st.plotly_chart(fig, use_container_width=True)

# Alert section
st.markdown("## ⚠️ Active Weather Alerts")
alert_df = df[df['is_alert'] == True]
if alert_df.empty:
    st.success("✅ No alerts at this time.")
else:
    st.dataframe(alert_df[['datetime', 'city', 'temperature', 'weather', 'humidity', 'wind_speed']], use_container_width=True)

# Raw data view
with st.expander("📋 View Raw Data"):
    st.dataframe(df[['datetime', 'city', 'temperature', 'humidity', 'wind_speed', 'weather', 'is_alert']], use_container_width=True)
