
import plotly.express as ple
import streamlit as st

from NP import calculate_amount, total_balance
from SQL import (
    actual_month_data,
    add_transaction,
    create_table,
    get_transactions,
    load_transactions,
)

#This will create the database and the table if they don't exist
create_table()

#This copy the db in the session_state of st. If you want to know more about this we recommend read the streamlit documentation
if 'spendmanager' not in st.session_state:
    st.session_state.spendmanager = load_transactions()


st.title("SpendManager")
st.subheader("Track your expenses and income easily")


#Here the user can add a new transaction in the database.
with st.expander(label="Add an transaction"):  # noqa: SIM117
    with st.form("Add Transaction", clear_on_submit=True):
        type = st.selectbox("Transaction Type", ["Income", "Expense"])
        date = st.date_input("Date")
        method = st.selectbox("Payment Method", ["Cash", "Credit Card", "Bank Transfer", "Other"])
        amount = st.number_input("Amount", min_value=0.0, format="%.2f", step=1.0, placeholder="Enter the amount", value= None )
        category = st.selectbox("Category", ["Food", "Transportation", "Entertainment", "Health", "Education", "Other"]) #Here you can add new categories
        notes = st.text_input("Notes", placeholder="Optional",)

 
        submit = st.form_submit_button("Add Transaction")


#This section will start only if the sumbit button was pressed
if submit:
    signed_amount = calculate_amount(type, amount)
    add_transaction(
        type =  type,
        amount = signed_amount,
        notes = notes,
        category = category,
        date = date
                       )
    st.success("Transaction added successfully.")

#This creates the df based on the transactions in the database
df = get_transactions()

st.divider()

#This shows the actual balance based on the database 
st.metric(label="Total balance",
          value=f"${total_balance(df):,.2f}",
          border=True,
          width=True)
#This shows the total income based on the database 
st.metric(label= "Total Income",
          value=f"${df[df['Type'] == 'Income']['Amount'].sum():,.2f}",
          border=True,
          width=True)
#This shows the total expenses based on the databse
st.metric(label= "Total Expenses",
          value=f"${df[df['Type'] == 'Expense']['Amount'].sum():,.2f}",
          border=True,
          width=True,


          )
st.divider()

expense_df = df[df["Type"] == "Expense"].copy()
expense_df["Amount"] = expense_df["Amount"].abs()

tab1 ,tab2 = st.tabs(["Charts", "Monthly Summary"])
with tab1:
    st.subheader("Charts")
    if st.session_state.spendmanager.empty:
        st.info("Add transactions to show charts")
    def pl_pie_chart(expense_df):
        fig = ple.pie(
            data_frame=expense_df,
            values='Amount',
            names='Category',
            title='Expenses by Category',
            hole=0.3,
        )
        return fig 


with tab2:
    st.subheader("Monthly Summary")
    total_i = st.session_state.spendmanager.index #Complete so it would show if there its 10 or less columns
    if st.session_state.spendmanager.empty:
        st.info("Add transactions to show your monthly summary")
    else:
        st.dataframe(actual_month_data(), hide_index=True) 
    


st.divider()
with st.expander(label="Transactions"):
    if st.session_state.spendmanager.empty:
       st.info("Add an transaction to start")
    else:
        st.subheader("Transactions")
        st.text("Here you can see your last 10 transactions")
        st.dataframe(df.head(10))
