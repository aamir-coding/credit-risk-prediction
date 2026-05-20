import streamlit as st
from prediction_helper import predict  # Ensure this is correctly linked to your prediction_helper.py

# 1. Page Configuration
st.set_page_config(
    page_title="Classification Project: Credit Risk Modelling", 
    page_icon="📊", 
    layout="wide" # Uses the full width of the screen for a dashboard feel
)

# 2. Header Section
st.title("📊 Lauki Finance: Credit Risk Dashboard")
st.markdown("Evaluate applicant creditworthiness using our advanced risk modeling system. Fill out the details below to generate a real-time risk assessment.")
st.divider()

# 3. Input Sections (Grouped logically into 3 columns)
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("👤 Applicant Profile")
    age = st.number_input('Age', min_value=18, step=1, max_value=100, value=28)
    income = st.number_input('Annual Income (₹)', min_value=0, value=1200000, step=50000)
    residence_type = st.selectbox('Residence Type', ['Owned', 'Rented', 'Mortgage'])

with col2:
    st.subheader("🏦 Loan Details")
    loan_amount = st.number_input('Loan Amount (₹)', min_value=0, value=2560000, step=50000)
    loan_tenure_months = st.number_input('Loan Tenure (months)', min_value=0, step=1, value=36)
    loan_purpose = st.selectbox('Loan Purpose', ['Education', 'Home', 'Auto', 'Personal'])
    loan_type = st.selectbox('Loan Type', ['Unsecured', 'Secured'])

with col3:
    st.subheader("💳 Credit History")
    credit_utilization_ratio = st.number_input('Credit Utilization Ratio (%)', min_value=0, max_value=100, step=1, value=30)
    delinquency_ratio = st.number_input('Delinquency Ratio (%)', min_value=0, max_value=100, step=1, value=30)
    avg_dpd_per_delinquency = st.number_input('Avg DPD (Days Past Due)', min_value=0, value=20)
    num_open_accounts = st.number_input('Open Loan Accounts', min_value=1, max_value=4, step=1, value=2)

st.divider()

# 4. Calculation & Action Section (Removed vertical_alignment to fix the TypeError)
action_col1, action_col2 = st.columns([3, 1])

with action_col1:
    # Calculate Loan to Income Ratio and display it beautifully using st.metric
    loan_to_income_ratio = loan_amount / income if income > 0 else 0
    st.metric(label="Calculated Loan-to-Income (LTI) Ratio", value=f"{loan_to_income_ratio:.2f}")

with action_col2:
    # Adding a blank space to manually push the button down to align with the metric
    st.write("") 
    calculate_btn = st.button('Assess Credit Risk 🚀', type="primary", use_container_width=True)

# 5. Results Section
if calculate_btn:
    st.markdown("---")
    st.subheader("📈 Assessment Results")
    
    # Run the prediction
    probability, credit_score, rating = predict(
        age, income, loan_amount, loan_tenure_months, avg_dpd_per_delinquency,
        delinquency_ratio, credit_utilization_ratio, num_open_accounts,
        residence_type, loan_purpose, loan_type
    )

    # Display the results using metric cards instead of plain text
    res_col1, res_col2, res_col3 = st.columns(3)
    
    with res_col1:
        st.metric(label="Default Probability", value=f"{probability:.2%}")
    with res_col2:
        st.metric(label="Credit Score", value=credit_score)
    with res_col3:
        st.metric(label="Risk Rating", value=rating)
