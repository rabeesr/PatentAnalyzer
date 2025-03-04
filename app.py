import streamlit as st
import pandas as pd
import requests
import plotly.express as px
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

BASE_URL = "http://localhost:8000"

st.title("Patent Analyzer App by Rabees R.")

# --- 1. Multi-Select Dropdown ---
options = ["Option A", "Option B", "Option C"]
selected_options = st.multiselect("Select Options", options)

# --- 2. Run/Execute Button ---
if st.button("Run Query"):
    st.success("Query executed!")

# --- 3. Save Copy/Report Button ---
if st.button("Save Report"):
    response = requests.post(f"{BASE_URL}/save_report")
    if response.status_code == 200:
        st.success("Report saved successfully!")

# --- 4. Selectable Table ---
st.subheader("Data Table with Selectable Entry")
response = requests.get(f"{BASE_URL}/data")
if response.status_code == 200:
    data = pd.DataFrame(response.json())
    selected_row = st.selectbox("Select an entry:", data["Name"])
    st.write("Selected Entry:", selected_row)

# --- 5. Heatmap Visualization ---
st.subheader("Heatmap Example")
response = requests.get(f"{BASE_URL}/heatmap")
if response.status_code == 200:
    heatmap_data = np.array(response.json())
    fig, ax = plt.subplots()
    sns.heatmap(heatmap_data, cmap="coolwarm", annot=True, ax=ax)
    st.pyplot(fig)

# --- 6. Line Chart ---
st.subheader("Line Chart Example")
response = requests.get(f"{BASE_URL}/line_chart")
if response.status_code == 200:
    chart_data = response.json()
    fig = px.line(x=chart_data["x"], y=chart_data["y"], labels={"x": "X-axis", "y": "Y-axis"}, title="Line Chart Example")
    st.plotly_chart(fig)
