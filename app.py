import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import json
import os

# Google Sheets setup
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds_dict = json.loads(os.environ["GOOGLE_SHEET_CREDENTIALS"])
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)

sheet_company = client.open("HR Survey Responses").worksheet("Company Info")
sheet_salaries = client.open("HR Survey Responses").worksheet("Salaries")

st.title("HR Benchmarking Survey 2025")

st.header("🏠 Home Information")

# Company Info Fields
home_info = {
    "AdvantAge Ontario Membership ID": st.text_input("AdvantAge Ontario Membership ID"),
    "Home Name": st.text_input("Home Name"),
    "MOH Facility ID (Master #)": st.text_input("MOH Facility ID (Master #)"),
    "Type of Home (CH, NPN, MH)": st.text_input("Type of Home (CH, NPN, MH)"),
    "Home Location (Rural, Urban)": st.text_input("Home Location (Rural, Urban)"),
    "Contact Name": st.text_input("Contact Name"),
    "Title": st.text_input("Title"),
    "Email": st.text_input("Email"),
    "Management Organization (if your home is managed by a third-party management company)": st.text_input("Management Organization (if applicable)"),
    "Total Approved Beds (excluding specialty beds)": st.number_input("Total Approved Beds (excluding specialty beds)", min_value=0)
}

st.markdown("---")
st.header("💼 Salary Data")

# Job titles for the salary table
job_titles = [
    "Chief Executive Officer (CEO)/Executive Director (Permanent Position) - Responsible for LTC Home(s) Only",
    "Chief Executive Officer (CEO)/Executive Director (Contract/Out Sourced Position) - Responsible for LTC Home(s) Only",
    "Chief Executive Officer (CEO)/Executive Director (Permanent Position) - Responsible for LTC Home(s) and/ or Housing and/or Campus and/or Other Operations in addition to LTC",
    "Chief Executive Officer (CEO)/Executive Director (Contract Position) - Responsible for LTC Home and/ or Housing and/or Campus and/or Other Operations in addition to LTC",
    "Chief Operating Officer (COO)",
    "Chief Financial Officer (CFO)",
    "Executive Assistant - CEO/Executive Director",
    "Executive Assistant - COO",
    "Executive Assistant - CFO"
]

# Create editable salary DataFrame
salary_df = pd.DataFrame({
    "Job Title": job_titles,
    "FT Lowest $/Year": [0] * len(job_titles),
    "FT Highest $/Year": [0] * len(job_titles),
    "FT Bonus ($)": [0] * len(job_titles),
})

edited_df = st.data_editor(
    salary_df,
    column_config={
        "Job Title": st.column_config.TextColumn(disabled=True),
        "FT Lowest $/Year": st.column_config.NumberColumn(format="$%d"),
        "FT Highest $/Year": st.column_config.NumberColumn(format="$%d"),
        "FT Bonus ($)": st.column_config.NumberColumn(format="$%d")
    },
    use_container_width=True,
    num_rows="fixed"
)

# Submit Button
if st.button("Submit Survey"):
    # Save company info
    company_row = list(home_info.values())
    sheet_company.append_row(company_row)

    # Save salaries
    for _, row in edited_df.iterrows():
        sheet_salaries.append_row([
            home_info["Home Name"],
            row["Job Title"],
            row["FT Lowest $/Year"],
            row["FT Highest $/Year"],
            row["FT Bonus ($)"]
        ])

    st.success("✅ Survey submitted successfully!")
