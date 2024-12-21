import pandas as pd
import matplotlib.pyplot as plt
def test_function():
    return "Utils module imported successfully!"

def load_data(path):
    """Load data from a CSV file."""
    return pd.read_csv(path)

def filter_data_by_fund(df, fund_name):
    """Filter the DataFrame by the selected fund."""
    return df[df["Fund Invested In"] == fund_name]

def plot_bar_chart(filtered_data):
    """Plot a bar chart for the filtered data."""
    fig, ax = plt.subplots()
    filtered_data.plot(
        x="Investor Name", 
        y="Amount Invested ($)", 
        kind="bar", 
        ax=ax, 
        title="Amount Invested by Investors"
    )
    return fig

def plot_pie_chart(filtered_data):
    """Plot a pie chart for the filtered data."""
    fig, ax = plt.subplots()
    filtered_data.plot(
        y="Current Value ($)", 
        kind="pie", 
        labels=filtered_data["Investor Name"], 
        autopct='%1.1f%%', 
        ax=ax, 
        title="Portfolio Current Value Distribution"
    )
    return fig

