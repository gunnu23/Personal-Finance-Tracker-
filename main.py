##########################
import streamlit as st
import pandas as pd
import plotly.express as px
import csv
import datetime

# Create a Streamlit app
st.set_page_config(page_title="Personal Finance Dashboard")


# Create a sidebar for inputting financial details
st.sidebar.header("Financial Details")
income = st.sidebar.number_input("Monthly Income", value=1000)

# Add a section for adding expenses in the sidebar
st.sidebar.header("Add Expenses")
expense_categories = st.sidebar.multiselect("Select expense categories:", ["Rent/Mortgage", "Utilities", "Groceries", "Transportation", "Insurance", "Entertainment"])
expense_amounts = {}
for category in expense_categories:
    expense_amounts[category] = st.sidebar.number_input(f"Enter amount for {category}:")
expenses = sum(expense_amounts.values())

# Add a section for monthly investments and savings
st.sidebar.header("Monthly Investments and Savings")
investments = st.sidebar.number_input("Monthly Investments", value=1000)
savings = st.sidebar.number_input("Monthly Savings", value=1000)

# Create a main page for displaying key financial metrics and visualizations
st.title("Personal Finance Dashboard")
 
# Add a section for filtering data by date ranges
st.header("Filter Data by Date Range")
start_date = st.date_input("Start Date")
end_date = st.date_input("End Date")

# Add a section for key financial metrics
st.header("Key Financial Metrics")
st.write("Total Income: ₹", income)
st.write("Total Expenses: ₹", expenses)
st.write("Net Savings: ₹", savings)
st.write("Investment Growth: ₹", investments)

# Create a bar chart using Plotly Express
st.title("Expenses:")
if expense_amounts:
    expense_data = {'Expenses': list(expense_amounts.keys()), 'Amount': list(expense_amounts.values())}
    expense_df = pd.DataFrame(expense_data)
    expense_df.loc[len(expense_df)] = ['Monthly Investments', investments]
    expense_df.loc[len(expense_df)] = ['Monthly Savings', savings]
    fig = px.bar(expense_df, x='Expenses', y='Amount', title='Expenses Breakdown')
    st.plotly_chart(fig)
else:
    st.write("No expenses added yet!")

# Store the data in a CSV file when the user clicks "Add Expenses"
if st.sidebar.button("Add Expenses"):
    current_date = datetime.date.today().strftime("%Y-%m-%d")
    data_to_store = {
        'Date': [current_date],
        'Income': [income],
        'Expenses': [expenses],
        'Expense Categories': [', '.join(expense_categories)],
        'Expense Amounts': [', '.join(str(amount) for amount in expense_amounts.values())],
        'Investments': [investments],
        'Savings': [savings]
    }
    df = pd.DataFrame(data_to_store)
    if not st.session_state.get('csv_file'):
        st.session_state.csv_file = 'finance_data.csv'
        df.to_csv(st.session_state.csv_file, index=False)
    else:
        df.to_csv(st.session_state.csv_file, mode='a', header=False, index=False)
    st.sidebar.write("Expenses added successfully!")

# Display the stored data
st.title("Stored Data")
if st.session_state.get('csv_file'):
    stored_data = pd.read_csv(st.session_state.csv_file)
    st.write(stored_data)
    st.write("the data is stored in the csv below in your pc")
else:
    st.write("No data stored yet!")
