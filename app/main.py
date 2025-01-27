import pandas as pd
import streamlit as st
import plotly.express as px

# Load Data
portfolio_data_path = "data/portfolio-2024-12-21.csv"
portfolio_data = pd.read_csv(portfolio_data_path)

# Ensure numeric conversion
columns_to_clean = ["Initial value", "Current value", "Roi"]
for column in columns_to_clean:
    portfolio_data[column] = pd.to_numeric(portfolio_data[column].replace("[^0-9.]+", "", regex=True), errors="coerce")

# Convert values to millions for readability
portfolio_data["Initial value"] = portfolio_data["Initial value"] / 1_000_000
portfolio_data["Current value"] = portfolio_data["Current value"] / 1_000_000

# Round ROI to the nearest whole number for readability
portfolio_data["Roi"] = portfolio_data["Roi"].round(0).astype(int)

# Filter out entries with values over 60 million
portfolio_data = portfolio_data[portfolio_data["Current value"] <= 60]

# Manually sort funds by Roman numeral order
roman_sorted_order = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "11"]
def custom_sort_key(investor):
    for index, roman in enumerate(roman_sorted_order):
        if isinstance(investor, str) and roman in investor:
            return index
    return len(roman_sorted_order)
portfolio_data = portfolio_data.sort_values(by="Investor", key=lambda col: col.map(custom_sort_key))

# App Layout
st.title("Meyer Equity Dashboard")


# Tabs for Portfolio and Fund Views
tab1, tab2 = st.tabs(["📊 Portfolio Growth", "👤 Fund Performance"])

# Portfolio Growth Tab
with tab1:
    st.subheader("Portfolio Overview")

    total_initial_value = portfolio_data["Initial value"].sum()
    total_current_value = portfolio_data["Current value"].sum()
    roi_avg = ((total_current_value - total_initial_value) / total_initial_value) * 100

    st.metric("Total Initial Value", f"${total_initial_value:,.2f}M")
    st.metric("Total Current Value", f"${total_current_value:,.2f}M")
    st.metric("Average ROI", f"{roi_avg:.0f}%")

    st.divider()

    st.write("### Growth Breakdown")
    fig_growth = px.bar(
        portfolio_data.melt(id_vars="Investor", value_vars=["Initial value", "Current value"], var_name="Type", value_name="Value"),
        x="Investor",
        y="Value",
        color="Type",
        title="Portfolio Value Breakdown",
        labels={"Value": "Value (Millions $)", "Investor": "Fund Name", "Type": "Metric"},
        barmode="group",
        text="Value",
        color_discrete_sequence=["#636EFA", "#EF553B"]  # Different colors for Initial and Current
    )
    fig_growth.update_traces(
        texttemplate="%{y:.2f}M",  # Ensure values display with two decimal places
        textfont_size=18  # Increase font size for readability
    )
    fig_growth.update_layout(
        xaxis_title="Fund Name",
        yaxis_title="Value (Millions $)",
        font=dict(size=18),  # Increase overall font size for better readability
        height=800,  # Increase height for better visualization
        width=1600,  # Set width to numeric value for compatibility
        margin=dict(t=50, l=50, r=50, b=150),  # Adjust bottom margin for more space
        xaxis=dict(tickangle=45)  # Rotate x-axis labels for better visibility
    )
    st.plotly_chart(fig_growth)

    st.divider()

    st.write("### ROI Comparison")
    fig_roi = px.bar(
        portfolio_data,
        x="Investor",
        y="Roi",
        title="ROI by Portfolio",
        labels={"Roi": "Return on Investment (%)", "Investor": "Fund Name"},
        text="Roi",
        color="Roi",
        color_continuous_scale="viridis"
    )
    fig_roi.update_traces(
        texttemplate="%{text}%",
        textposition="outside",
        textfont_size=18  # Increase font size for readability
    )
    fig_roi.update_layout(
        xaxis_title="Fund Name",
        yaxis_title="Return on Investment (%)",
        yaxis=dict(tickformat=".0f%%"),
        font=dict(size=18),  # Increase overall font size for better readability
        height=800,  # Increase height for better visualization
        width=1600,  # Set width to numeric value for compatibility
        xaxis=dict(tickangle=45)  # Rotate x-axis labels for better visibility
    )
    st.plotly_chart(fig_roi)

# Fund Performance Tab
with tab2:
    st.subheader("Fund Portfolio")
    fund_names = portfolio_data["Investor"].unique()
    selected_fund = st.sidebar.selectbox("Select a Fund", fund_names)

    # Filter data for selected fund
    fund_data = portfolio_data[portfolio_data["Investor"] == selected_fund]

    if not fund_data.empty:
        st.write(f"### {selected_fund} Overview")
        initial_value = fund_data["Initial value"].iloc[0]
        current_value = fund_data["Current value"].iloc[0]
        roi = fund_data["Roi"].iloc[0]

        st.metric("Initial Investment", f"${initial_value:,.2f}M")
        st.metric("Current Value", f"${current_value:,.2f}M")
        st.metric("ROI", f"{roi:.0f}%")

        st.divider()

        st.write("### Value Growth")
        fig_fund_growth = px.line(
            x=["Initial Value", "Current Value"],
            y=[initial_value, current_value],
            title="Investment Growth Over Time",
            labels={"x": "Stage", "y": "Value (Millions $)"},
        )
        fig_fund_growth.update_traces(mode="lines+markers", line_shape="spline")
        fig_fund_growth.update_layout(height=600)  # Increase height for better visualization
        st.plotly_chart(fig_fund_growth)

    else:
        st.write("No data available for the selected fund.")
