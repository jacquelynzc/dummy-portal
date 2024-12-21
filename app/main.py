import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from app.utils import load_data, filter_data_by_fund, plot_bar_chart, plot_pie_chart
import sys
from pathlib import Path
from app.utils import test_function
import os

# Set working directory explicitly
os.chdir(Path(__file__).resolve().parent.parent)
sys.path.append(os.getcwd())

print("Working Directory:", os.getcwd())

# Print sys.path for debugging
print("Python Path:", sys.path)

# Ensure the root directory is added to sys.path
current_dir = Path(__file__).resolve().parent
root_dir = current_dir.parent
sys.path.append(str(root_dir))
print("Updated Python Path:", sys.path)
print(test_function())

# Debug Python module search paths
print("Python Path:", sys.path)
print("Current Working Directory:", Path(__file__).resolve().parent)

# Add the parent directory of app/ to the Python path (if not already set)
sys.path.append(str(Path(__file__).resolve().parent.parent))

# Load the dataset
data_path = "app/data/mock_investor_portal_data.csv"
df = load_data(data_path)

# Streamlit App
st.title("Investor Portal Dashboard")
st.write("Explore portfolio data interactively!")

# Display the DataFrame
st.subheader("Investor Data")
st.dataframe(df)

# Filter by Fund
funds = df["Fund Invested In"].unique()
selected_fund = st.selectbox("Select a Fund", options=funds)

# Filter data by selected fund
filtered_data = filter_data_by_fund(df, selected_fund)

# Display filtered data
st.subheader(f"Data for {selected_fund}")
st.dataframe(filtered_data)

# Visualize the data
st.subheader("Investment Analysis")

# Bar chart of Amount Invested
st.pyplot(plot_bar_chart(filtered_data))

# Pie chart of Current Value
st.pyplot(plot_pie_chart(filtered_data))

