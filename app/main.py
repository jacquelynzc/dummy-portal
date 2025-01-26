import pandas as pd
import streamlit as st
import plotly.express as px

# Load Data
portfolio_data_path = "data/portfolio-2024-12-21.csv"
spv_data_path = "data/spv_investors_with_ids.csv"

# Load Portfolio Data
data = pd.read_csv(portfolio_data_path)
columns_to_clean_portfolio = ["Initial value", "Current value", "Initial price", "Current price"]
for column in columns_to_clean_portfolio:
    data[column] = pd.to_numeric(data[column].replace("[^0-9.]", "", regex=True), errors="coerce")

# Remove SpaceX combined row (if exists)
data = data[data["Name"] != "Space Exploration Technologies Corp. (SpaceX)"]

# Add mock Date column for demonstration
data["Date"] = pd.date_range(start="2023-01-01", periods=len(data), freq="M")

# Load SPV Data
spv_data = pd.read_csv(spv_data_path)
columns_to_clean_spv = [
    "Ownership", "Ownership by commitment", "Committed", "Called",
    "Called (with fees)", "Commitment remaining", "Cash position"
]
for column in columns_to_clean_spv:
    if column in spv_data.columns:
        spv_data[column] = pd.to_numeric(spv_data[column].replace("[^0-9.]+", "", regex=True), errors="coerce")

# App Layout
st.title("Portfolio and Investor Dashboard")
st.write("Analyze portfolio performance or focus on specific investor data.")

# Tabs for Portfolio and Investor Views
tab1, tab2 = st.tabs(["📊 Portfolio View", "👤 Investor View"])

# Portfolio View
with tab1:
    st.subheader("Portfolio Overview")
    col1, col2 = st.columns(2)

    with col1:
        total_initial_value = data["Initial value"].sum()
        total_current_value = data["Current value"].sum()
        difference_value = total_current_value - total_initial_value

        st.metric("Total Initial Value", f"${total_initial_value:,.2f}")
        st.metric("Total Current Value", f"${total_current_value:,.2f}")
        st.metric("Difference", f"${difference_value:,.2f}")

    with col2:
        st.write("### Portfolio Composition")
        fig = px.pie(data, values="Current value", names="Name", title="Portfolio Breakdown")
        st.plotly_chart(fig)

    st.write("### Portfolio Trends")
    fig_trend = px.line(data, x="Date", y="Current value", color="Name", title="Portfolio Value Over Time")
    st.plotly_chart(fig_trend)

# Investor View
with tab2:
    st.subheader("Investor Portfolio")
    investors = spv_data["Investor"].unique()
    selected_investor = st.sidebar.selectbox("Select an Investor", investors)

    # Filter data for the selected investor
    investor_spv_data = spv_data[spv_data["Investor"] == selected_investor]

    st.write(f"### Data for {selected_investor}")
    st.dataframe(investor_spv_data)

    st.write("### Investor Metrics")
    if not investor_spv_data.empty:
        total_commitment = investor_spv_data["Committed"].sum()
        total_called = investor_spv_data["Called"].sum()
        remaining_commitment = investor_spv_data["Commitment remaining"].sum()
        
        st.metric("Total Commitment", f"${total_commitment:,.2f}")
        st.metric("Total Called", f"${total_called:,.2f}")
        st.metric("Commitment Remaining", f"${remaining_commitment:,.2f}")

    st.write("### Investor Cash Position")
    if "Cash position" in investor_spv_data.columns:
        fig_cash = px.bar(
            investor_spv_data, x="Investor", y="Cash position",
            title="Cash Position", text="Cash position"
        )
        st.plotly_chart(fig_cash)