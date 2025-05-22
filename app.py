import streamlit as st
import pandas as pd

st.set_page_config(page_title="HR Benchmarking Survey", layout="wide")

st.title("🏢 HR Benchmarking Survey 2025")

# Section 1: Company Info
st.header("1️⃣ Company Information")
company_name = st.text_input("Company Name")
industry = st.selectbox("Industry", ["Finance", "Healthcare", "IT", "Manufacturing", "Other"])
contact_email = st.text_input("Contact Email")

# Section 2: Salary Table Input
st.header("2️⃣ Job Title and Salary Data")

# Create editable table
st.markdown("Enter salary details for each job role below:")
salary_df = pd.DataFrame(columns=["Job Title", "Min Salary", "Max Salary", "Bonus"])

edited_df = st.data_editor(
    salary_df,
    num_rows="dynamic",
    use_container_width=True,
    key="salary_editor"
)

# Section 3: Additional Notes
st.header("3️⃣ Notes or Comments")
comments = st.text_area("Add any notes or questions here...")

# Submit
if st.button("✅ Submit Survey"):
    full_data = {
        "Company Name": company_name,
        "Industry": industry,
        "Email": contact_email,
        "Comments": comments
    }
    
    company_df = pd.DataFrame([full_data])
    
    # Save both tables
    with pd.ExcelWriter("HR_Survey_Submission.xlsx", engine='openpyxl', mode='w') as writer:
        company_df.to_excel(writer, sheet_name='Company Info', index=False)
        edited_df.to_excel(writer, sheet_name='Salaries', index=False)
    
    st.success("✅ Submission saved successfully!")
