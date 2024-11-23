import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Load CSV files
def load_data(period):
    file_map = {
        "Monthly": "monthly_bills.csv",
        "Bi-weekly": "biweekly_bills.csv",
        "Weekly": "weekly_bills.csv",
    }
    return pd.read_csv(file_map[period])

# Initialize Streamlit app
st.title(" Kenz & Nate Budgeting Dashboard")

# Pay rate and hours input
st.sidebar.header("Income Details")
pay_rate = st.sidebar.number_input("Hourly Pay Rate ($)", min_value=0.0, value=20.0)
hours_worked = st.sidebar.number_input("Hours Worked", min_value=0.0, value=40.0)

# Tax calculation
gross_income = pay_rate * hours_worked
taxes = gross_income * 0.17
net_income = gross_income - taxes
st.sidebar.metric("Net Income ($)", round(net_income, 2))

# Time period selection
time_period = st.sidebar.radio("Select Budgeting Period", ["Monthly", "Bi-weekly", "Weekly"])
bills_data = load_data(time_period)

# Bills selection
st.header("Select Your Bills")
selected_bills = st.multiselect("Bills", options=bills_data["bills"], default=[])
bill_costs = bills_data[bills_data["bills"].isin(selected_bills)]["cost"].sum()

# Other expenses
st.subheader("Other Expenses")
other_expenses = st.number_input("Enter Other Expenses ($)", min_value=0.0, value=0.0)

# Calculate remaining income
remaining_income = net_income - bill_costs - other_expenses

# Visualization
fig = go.Figure(go.Indicator(
    mode="gauge+number",
    value=remaining_income,
    gauge={
        "axis": {"range": [0, net_income]},
        "bar": {"color": "green"},
        "steps": [
            {"range": [0, net_income * 0.5], "color": "lightgray"},
            {"range": [net_income * 0.5, net_income], "color": "gray"},
        ],
    },
    title={"text": "Remaining Income"}
))
st.plotly_chart(fig)

# Display breakdown
st.subheader("Summary")
st.write(f"**Gross Income:** ${gross_income:.2f}")
st.write(f"**Taxes (17%):** -${taxes:.2f}")
st.write(f"**Net Income:** ${net_income:.2f}")
st.write(f"**Total Bills:** -${bill_costs:.2f}")
st.write(f"**Other Expenses:** -${other_expenses:.2f}")
st.write(f"**Remaining Income:** ${remaining_income:.2f}")