import streamlit as st
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
import base64
from pl_module import handle_pl_form, calculate_pl_summary
from bs_module import handle_bs_form, calculate_bs_summary
from cf_module import handle_cf_form, calculate_cf_summary

# Initialize session state
def initialize_session_state():
    default_data = {
        'pl_data': pd.DataFrame(columns=['Category', 'Particulars', 'Amount']),
        'bs_data': pd.DataFrame(columns=['Category', 'Subcategory', 'Particulars', 'Amount']),
        'cf_data': pd.DataFrame(columns=['Category', 'Particulars', 'Amount']),
    }
    for key, value in default_data.items():
        if key not in st.session_state:
            st.session_state[key] = value

initialize_session_state()

# App title
st.title("3-Statement Financial Model")

# P/L Statement Section
st.header("1. Profit & Loss (P/L) Statement")
if st.checkbox("Add P/L Data"):
    handle_pl_form()
if not st.session_state['pl_data'].empty:
    st.subheader("P/L Data")
    st.dataframe(st.session_state['pl_data'])
    summary = calculate_pl_summary(st.session_state['pl_data'])


# Balance Sheet Section
st.header("2. Balance Sheet")
st.write("Do NOT add a negative sign before the amount for liabilities.")
if st.checkbox("Add Balance Sheet Data"):
    handle_bs_form()
if not st.session_state['bs_data'].empty:
    st.subheader("Balance Sheet Data")
    st.dataframe(st.session_state['bs_data'])
    summary = calculate_bs_summary(st.session_state['bs_data'])

# Cash Flow Statement Section
st.header("3. Cash Flow Statement")
st.write("For cash outflows, add a negative sign before the amount.")
if st.checkbox("Add Cash Flow Data"):
    handle_cf_form()
if not st.session_state['cf_data'].empty:
    st.subheader("Cash Flow Data")
    st.dataframe(st.session_state['cf_data'])
    summary = calculate_cf_summary(st.session_state['cf_data'])

# Report Generation
if st.button("Generate PDF Report"):
    doc = SimpleDocTemplate(
        "financial_report.pdf",
        pagesize=letter,
        leftMargin=35,  
        rightMargin=30,
        topMargin=30,
        bottomMargin=20,
        title="Financial Report"
    )
    styles = getSampleStyleSheet()
    elements = [Paragraph("Your Personalised Financial Statements", styles['Title'])]

    # Add P/L Statement to Report
    if not st.session_state['pl_data'].empty:
        elements.append(Paragraph("Profit & Loss Statement", styles['Heading2']))
        data = st.session_state['pl_data']
        summary = calculate_pl_summary(data)
        organized_data = pd.concat([
            data[data["Category"] == "Income"],
            pd.DataFrame([{"Category": "", "Particulars": "Total Income", "Amount": summary["Total Income"]}]),
            data[data["Category"] == "Expense"],
            pd.DataFrame([{"Category": "", "Particulars": "Total Expense", "Amount": summary["Total Expense"]}]),
            pd.DataFrame([{"Category": "", "Particulars": "Profit Before Tax", "Amount": summary["Profit Before Tax"]}]),
            data[data["Category"] == "Tax"],
            pd.DataFrame([{"Category": "", "Particulars": "Total Tax", "Amount": summary["Total Tax"]}]),
            pd.DataFrame([{"Category": "", "Particulars": "Profit After Tax", "Amount": summary["Profit After Tax"]}])
        ], ignore_index=True)
        elements.append(Table([organized_data.columns.tolist()] + organized_data.values.tolist(), style=TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ])))

    # Add Balance Sheet to Report
    if not st.session_state['bs_data'].empty:
        elements.append(Paragraph("Balance Sheet", styles['Heading2']))
        data = st.session_state['bs_data']
        summary = calculate_bs_summary(data)

        # Organize data in the required format
        organized_data = pd.concat([
            data[data['Subcategory'] == "Non-current assets"],
            pd.DataFrame([{"Category": "", "Subcategory": "", "Particulars": "Total Non-current assets", "Amount": summary["Total Non-current assets"]}]),
            data[data['Subcategory'] == "Current assets"],
            pd.DataFrame([{"Category": "", "Subcategory": "", "Particulars": "Total Current assets", "Amount": summary["Total Current assets"]}]),
            pd.DataFrame([{"Category": "", "Subcategory": "", "Particulars": "Total Assets", "Amount": summary["Total Assets"]}]),
            data[data['Subcategory'] == "Equity"],
            pd.DataFrame([{"Category": "", "Subcategory": "", "Particulars": "Total Equity", "Amount": summary["Total Equity"]}]),
            data[data['Subcategory'] == "Non-current liabilities"],
            pd.DataFrame([{"Category": "", "Subcategory": "", "Particulars": "Total Non-current liabilities", "Amount": summary["Total Non-current liabilities"]}]),
            data[data['Subcategory'] == "Current liabilities"],
            pd.DataFrame([{"Category": "", "Subcategory": "", "Particulars": "Total Current liabilities", "Amount": summary["Total Current liabilities"]}]),
            pd.DataFrame([{"Category": "", "Subcategory": "", "Particulars": "Total Equity and Liabilities", "Amount": summary["Total Equity and Liabilities"]}])
        ], ignore_index=True)

        elements.append(Table([organized_data.columns.tolist()] + organized_data.values.tolist(), style=TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ])))
        elements.append(Spacer(1, 12))

    # Add Cash Flow Statement to Report
    if not st.session_state['cf_data'].empty:
        elements.append(Paragraph("Cash Flow Statement", styles['Heading2']))
        data = st.session_state['cf_data']
        summary = calculate_cf_summary(data)

        # Organize data in the required format
        organized_data = pd.concat([
            data[data['Category'] == "Operational activities"],
            #pd.DataFrame([{"Category": "", "Particulars": "Profit before tax", "Amount": ""}]),
            #pd.DataFrame([{"Category": "", "Particulars": "Operating profit before working capital changes", "Amount": ""}]),
            pd.DataFrame([{"Category": "", "Particulars": "Net cash flow from operating activities", "Amount": summary["Total Operational Activities"]}]),
            data[data['Category'] == "Investing activities"],
            pd.DataFrame([{"Category": "", "Particulars": "Net cash flow used in investing activities", "Amount": summary["Total Investing Activities"]}]),
            data[data['Category'] == "Financing activities"],
            pd.DataFrame([{"Category": "", "Particulars": "Cash flow used in financing activities", "Amount": summary["Total Financing Activities"]}])
        ], ignore_index=True)

        elements.append(Table([organized_data.columns.tolist()] + organized_data.values.tolist(), style=TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ])))
        elements.append(Spacer(1, 12))


    doc.build(elements)
    # Read and encode the PDF file for direct download
    with open("financial_report.pdf", "rb") as pdf:
        pdf_data = pdf.read()
    b64_pdf = base64.b64encode(pdf_data).decode('utf-8')  # Encode to base64

    # Generate the download link
    download_link = f'<a href="data:application/pdf;base64,{b64_pdf}" download="financial_report.pdf">Your report is ready! Click to download.</a>'
    st.markdown(download_link, unsafe_allow_html=True)
