import pandas as pd
import streamlit as st

def handle_cf_form():
    with st.form("cash_flow_form"):
        category = st.selectbox("Category", [
            "Operational activities", "Investing activities", "Financing activities"
        ])
        particulars = st.text_input("Particulars")
        amount = st.number_input("Amount", step=1.0)
        submitted = st.form_submit_button("Add Entry")

        if submitted:
            new_entry = {
                "Category": [category],
                "Particulars": [particulars],
                "Amount": [amount],
            }
            st.session_state["cf_data"] = pd.concat(
                [st.session_state["cf_data"], pd.DataFrame(new_entry)], ignore_index=True
            )
            st.success("Entry added successfully to Cash Flow Statement!")

def calculate_cf_summary(data):
    summary = {}

    # Operational activities
    operational_data = data[data["Category"] == "Operational activities"]
    summary["Total Operational Activities"] = operational_data["Amount"].sum()

    # Investing activities
    investing_data = data[data["Category"] == "Investing activities"]
    summary["Total Investing Activities"] = investing_data["Amount"].sum()

    # Financing activities
    financing_data = data[data["Category"] == "Financing activities"]
    summary["Total Financing Activities"] = financing_data["Amount"].sum()

    return summary
