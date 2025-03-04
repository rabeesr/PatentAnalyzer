from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import numpy as np

app = FastAPI()

# Enable CORS for Streamlit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Example dataset
df = pd.DataFrame({
    "ID": range(1, 6),
    "Name": ["Alice", "Bob", "Charlie", "David", "Eve"],
    "Value": [10, 20, 30, 40, 50]
})

# Endpoint to fetch table data
@app.get("/data")
async def get_data():
    return df.to_dict(orient="records")

# Endpoint to save a report (mock function)
@app.post("/save_report")
async def save_report():
    return {"message": "Report saved successfully"}

# Endpoint to generate heatmap data
@app.get("/heatmap")
async def get_heatmap():
    matrix = np.random.rand(5, 5) * 100  # Generate random heatmap values
    return matrix.tolist()

# Endpoint for line chart data
@app.get("/line_chart")
async def get_line_chart():
    x = list(range(10))
    y = [val**2 for val in x]  # Example quadratic function
    return {"x": x, "y": y}
