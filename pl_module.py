import pandas as pd
import streamlit as st

def handle_pl_form():
    with st.form("pl_form"):
        category = st.selectbox("Category", ["Income", "Expense", "Tax"])
        particulars = st.text_input("Particulars")
        amount = st.number_input("Amount", step=1.0)
        submitted = st.form_submit_button("Add Entry")

        if submitted:
            new_entry = {"Category": [category], "Particulars": [particulars], "Amount": [amount]}
            st.session_state['pl_data'] = pd.concat([st.session_state['pl_data'], pd.DataFrame(new_entry)], ignore_index=True)
            st.success("Entry added successfully to Profit & Loss statement!")

def calculate_pl_summary(data):
    totals = data.groupby("Category")["Amount"].sum().to_dict()
    income = totals.get("Income", 0.0)
    expense = totals.get("Expense", 0.0)
    tax = totals.get("Tax", 0.0)

    profit = income - expense
    profit_before_tax = profit
    profit_after_tax = profit_before_tax - tax

    return {
        "Total Income": income,
        "Total Expense": expense,
        "Total Tax": tax,
        "Profit Before Tax": profit_before_tax,
        "Profit After Tax": profit_after_tax,
    }
