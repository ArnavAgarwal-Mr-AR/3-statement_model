import pandas as pd
import streamlit as st

def handle_bs_form():
    # Initialize session state for category and subcategory if not already set
    if "selected_category" not in st.session_state:
        st.session_state["selected_category"] = "Assets"
    if "selected_subcategory" not in st.session_state:
        st.session_state["selected_subcategory"] = "Non-current assets"

    # Select Category (outside the form)
    category = st.selectbox(
        "Category",
        ["Assets", "Equity and Liabilities"],
        key="selected_category",
    )

    # Dynamically update subcategory options based on the selected category
    if category == "Assets":
        subcategories = ["Non-current assets", "Current assets"]
    elif category == "Equity and Liabilities":
        subcategories = ["Equity", "Non-current liabilities", "Current liabilities"]
    else:
        subcategories = []

    # Select Subcategory (outside the form)
    subcategory = st.selectbox(
        "Subcategory",
        subcategories,
        key="selected_subcategory",
    )

    # Input fields inside the form
    with st.form("balance_sheet_form"):
        particulars = st.text_input("Particulars")
        amount = st.number_input("Amount", step=1.0)
        submitted = st.form_submit_button("Add Entry")

        if submitted:
            # Add entry to session state
            new_entry = {
                "Category": [category],
                "Subcategory": [subcategory],
                "Particulars": [particulars],
                "Amount": [amount],
            }
            st.session_state["bs_data"] = pd.concat(
                [st.session_state["bs_data"], pd.DataFrame(new_entry)], ignore_index=True
            )
            st.success("Entry added successfully to Balance Sheet!")



def calculate_bs_summary(data):
    summary = {}

    # Assets
    assets_data = data[data['Category'] == 'Assets']
    for subcategory in ["Non-current assets", "Current assets"]:
        sub_data = assets_data[assets_data['Subcategory'] == subcategory]
        summary[f"Total {subcategory}"] = sub_data['Amount'].sum()
    summary["Total Assets"] = sum(summary[f"Total {subcategory}"] for subcategory in ["Non-current assets", "Current assets"])

    # Equity and Liabilities
    eql_data = data[data['Category'] == 'Equity and Liabilities']
    for subcategory in ["Equity", "Non-current liabilities", "Current liabilities"]:
        sub_data = eql_data[eql_data['Subcategory'] == subcategory]
        summary[f"Total {subcategory}"] = sub_data['Amount'].sum()
    summary["Total Equity and Liabilities"] = sum(summary[f"Total {subcategory}"] for subcategory in ["Equity", "Non-current liabilities", "Current liabilities"])

    return summary
