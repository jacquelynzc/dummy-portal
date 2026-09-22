import streamlit as st
import pandas as pd
import plotly.express as px

# Load the Investor Data
spv_data_path = "app/data/spv-6022-investors-2024-12-21.csv"
spv_data = pd.read_csv(spv_data_path)

# Ensure numeric conversion
columns_to_clean_spv = ["Ownership", "Ownership by commitment", "Committed", "Called", "Called (with fees)", "Commitment remaining", "Cash position"]
for column in columns_to_clean_spv:
    if column in spv_data.columns:
        spv_data[column] = pd.to_numeric(spv_data[column].replace("[^0-9.]+", "", regex=True), errors="coerce")

# Dashboard Title
st.title("Investor Portfolio Page")
st.write("Track the value of your position over time and explore detailed data.")

# Sidebar for Investor Selection
investors = spv_data["Investor"].unique()
selected_investor = st.sidebar.selectbox("Select an Investor", investors)

# Filter Data for Selected Investor
investor_spv_data = spv_data[spv_data["Investor"] == selected_investor]

# Display Metrics
st.header(f"Portfolio Overview: {selected_investor}")
if not investor_spv_data.empty:
    total_committed = investor_spv_data["Committed"].sum()
    total_called = investor_spv_data["Called"].sum()
    total_cash_position = investor_spv_data["Cash position"].sum()
    commitment_remaining = investor_spv_data["Commitment remaining"].sum()

    st.metric("Total Committed", f"${total_committed:,.2f}")
    st.metric("Total Called", f"${total_called:,.2f}")
    st.metric("Cash Position", f"${total_cash_position:,.2f}")
    st.metric("Commitment Remaining", f"${commitment_remaining:,.2f}")

    # Ownership and Commitment Analysis
    st.subheader("Ownership and Commitment Analysis")
    fig1 = px.bar(
        investor_spv_data,
        x="Ownership",
        y="Ownership by commitment",
        title="Ownership vs Commitment",
        labels={"Ownership": "Ownership (%)", "Ownership by commitment": "Commitment (%)"},
        text_auto=True
    )
    st.plotly_chart(fig1, use_container_width=True)

    # Detailed Data Table
    st.subheader("Detailed Portfolio Data")
    st.dataframe(investor_spv_data)
else:
    st.write("No data available for the selected investor.")

