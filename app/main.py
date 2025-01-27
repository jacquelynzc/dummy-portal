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

# Remove entries with extremely high values to normalize the scale
portfolio_data = portfolio_data[portfolio_data["Current value"] < 60]

# Sort funds alphabetically
portfolio_data = portfolio_data.sort_values(by="Investor")

# App Layout
st.title("Meyer Equity Dashboard")
st.write("A detailed view of portfolio growth and fund performance.")

# Tabs for Portfolio and Fund Views
tab1, tab2 = st.tabs(["📊 Portfolio Growth", "👤 Fund Performance"])

# Portfolio Growth Tab
with tab1:
    st.subheader("Portfolio Overview")
    col1, col2 = st.columns(2)

    with col1:
        total_initial_value = portfolio_data["Initial value"].sum()
        total_current_value = portfolio_data["Current value"].sum()
        roi_avg = ((total_current_value - total_initial_value) / total_initial_value) * 100

        st.metric("Total Initial Value", f"${total_initial_value:,.2f}M")
        st.metric("Total Current Value", f"${total_current_value:,.2f}M")
        st.metric("Average ROI", f"{roi_avg:.2f}%")

    with col2:
        st.write("### Growth Breakdown")
        fig_growth = px.sunburst(
            portfolio_data,
            path=["Investor", "Name"],
            values="Current value",
            color="Current value",
            title="Portfolio Value Breakdown",
            color_continuous_scale="viridis",
            labels={"Current value": "Value (Millions $)"}
        )
        fig_growth.update_layout(
            height=700,  # Adjust chart height
            font=dict(size=16),
            margin=dict(t=30, l=0, r=0, b=0),  # Adjust margins to center the circle
            coloraxis_colorbar=dict(
                thickness=15,  # Reduce colorbar thickness
                len=.6,  # Shorten the colorbar length
                orientation="v",
                title="Value (M)",
                title_side="right"
            )
        )
        st.plotly_chart(fig_growth)

    st.write("### ROI Comparison")
    fig_roi = px.bar(
        portfolio_data,
        x="Name",
        y="Roi",
        title="ROI by Portfolio",
        labels={"Roi": "Return on Investment (%)"},
        text="Roi",
        color="Roi",
        color_continuous_scale="viridis"
    )
    fig_roi.update_layout(
        xaxis_title="Investment Name",
        yaxis_title="Return on Investment (%)",
        yaxis=dict(tickformat=".1f%%"),
        font=dict(size=14),
        height=700  # Increase height for better visualization
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
        st.metric(
            "Initial Investment", f"${fund_data['Initial value'].iloc[0]:,.2f}M"
        )
        st.metric(
            "Current Value", f"${fund_data['Current value'].iloc[0]:,.2f}M"
        )
        st.metric(
            "ROI", f"{fund_data['Roi'].iloc[0]:.2f}%"
        )

        st.write("### Value Growth")
        fig_fund_growth = px.line(
            x=["Initial Value", "Current Value"],
            y=[fund_data["Initial value"].iloc[0], fund_data["Current value"].iloc[0]],
            title="Investment Growth Over Time",
            labels={"x": "Stage", "y": "Value (Millions $)"},
        )
        fig_fund_growth.update_traces(mode="lines+markers", line_shape="spline")
        fig_fund_growth.update_layout(height=600)  # Increase height for better visualization
        st.plotly_chart(fig_fund_growth)

    else:
        st.write("No data available for the selected fund.")
