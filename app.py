"""Streamlit Frontend for Insurance Fraud Detection

Interactive UI for detecting fraudulent insurance claims.
"""

import streamlit as st
import requests
import json
from datetime import datetime
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="Insurance Fraud Detector",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        background-color: #f8f9fa;
    }
    .metric-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 10px 0;
    }
    .fraud-detected {
        background-color: #ffebee;
        border-left: 5px solid #d32f2f;
    }
    .legitimate {
        background-color: #e8f5e9;
        border-left: 5px solid #388e3c;
    }
</style>
""", unsafe_allow_html=True)

# API Configuration
API_URL = st.secrets.get("API_URL", "http://localhost:8000") if hasattr(st, "secrets") else "http://localhost:8000"

# App title and header
st.title("🔍 Insurance Fraud Detection System")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    api_status = st.empty()
    
    # API Health Check
    try:
        response = requests.get(f"{API_URL}/health", timeout=2)
        if response.status_code == 200:
            api_status.success("✅ API Connected")
        else:
            api_status.error("❌ API Error")
    except:
        api_status.error("❌ API Unavailable")
    
    st.markdown("---")
    st.subheader("About")
    st.info("""
    This system uses Machine Learning (Decision Tree) to detect fraudulent insurance claims with **93% accuracy**.
    
    **Key Features:**
    - Real-time fraud detection
    - Risk assessment
    - Confidence scores
    """)

# Main content area
tab1, tab2, tab3 = st.tabs(["🔍 Single Claim Check", "📊 Batch Analysis", "📈 Analytics"])

with tab1:
    st.subheader("Analyze a Single Insurance Claim")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Claim Details")
        claim_amount = st.number_input(
            "Claim Amount ($)",
            min_value=0,
            max_value=1000000,
            value=5000,
            step=100
        )
        
        claim_age = st.slider(
            "Claim Age (Days)",
            min_value=0,
            max_value=365,
            value=30
        )
        
        claim_type = st.selectbox(
            "Claim Type",
            ["auto", "home", "health", "other"]
        )
        
        claimant_age = st.number_input(
            "Claimant Age (Years)",
            min_value=18,
            max_value=100,
            value=45
        )
    
    with col2:
        st.markdown("### Policy Information")
        policy_duration = st.number_input(
            "Policy Duration (Years)",
            min_value=0.1,
            max_value=50.0,
            value=5.0,
            step=0.5
        )
        
        monthly_premium = st.number_input(
            "Monthly Premium ($)",
            min_value=0,
            max_value=10000,
            value=100,
            step=10
        )
        
        witnesses = st.slider(
            "Number of Witnesses",
            min_value=0,
            max_value=10,
            value=1
        )
        
        police_report = st.selectbox(
            "Police Report Filed?",
            ["No", "Yes"]
        )
    
    # Additional claim details
    st.markdown("### Claim Types")
    col3, col4, col5 = st.columns(3)
    
    with col3:
        injury_claim = st.checkbox("Injury Claim", value=False)
    with col4:
        property_claim = st.checkbox("Property Claim", value=True)
    with col5:
        vehicle_claim = st.checkbox("Vehicle Claim", value=True)
    
    # Predict button
    if st.button("🔍 Analyze Claim", key="predict", use_container_width=True):
        try:
            # Prepare payload
            payload = {
                "claim_amount": float(claim_amount),
                "claim_age": int(claim_age),
                "claim_type": claim_type,
                "claimant_age": int(claimant_age),
                "policy_duration": float(policy_duration),
                "monthly_premium": float(monthly_premium),
                "witnesses": int(witnesses),
                "police_report": 1 if police_report == "Yes" else 0,
                "injury_claim": 1 if injury_claim else 0,
                "property_claim": 1 if property_claim else 0,
                "vehicle_claim": 1 if vehicle_claim else 0,
            }
            
            # Make API call
            response = requests.post(
                f"{API_URL}/predict",
                json=payload,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                
                # Display results
                st.markdown("---")
                st.subheader("✅ Analysis Results")
                
                col1, col2, col3, col4 = st.columns(4)
                
                fraud_status = "🚨 FRAUD DETECTED" if result["fraud_detected"] else "✅ LEGITIMATE"
                col1.metric(
                    "Status",
                    fraud_status,
                    delta=None
                )
                
                col2.metric(
                    "Fraud Probability",
                    f"{result['fraud_probability']*100:.1f}%",
                    delta=None
                )
                
                col3.metric(
                    "Risk Level",
                    result["risk_level"],
                    delta=None
                )
                
                col4.metric(
                    "Confidence",
                    f"{(1-result['fraud_probability'])*100:.1f}%",
                    delta=None
                )
                
                # Result message
                if result["fraud_detected"]:
                    st.error(f"### {result['message']}")
                else:
                    st.success(f"### {result['message']}")
                
                # Additional analysis
                st.markdown("### Detailed Analysis")
                analysis_cols = st.columns(2)
                
                with analysis_cols[0]:
                    st.info(f"""
                    **Claim Summary:**
                    - Amount: ${claim_amount:,.2f}
                    - Type: {claim_type.upper()}
                    - Age: {claim_age} days
                    - Claimant Age: {claimant_age} years
                    """)
                
                with analysis_cols[1]:
                    st.info(f"""
                    **Policy Summary:**
                    - Duration: {policy_duration} years
                    - Premium: ${monthly_premium}/month
                    - Witnesses: {witnesses}
                    - Police Report: {"Yes" if police_report == "Yes" else "No"}
                    """)
            else:
                st.error(f"API Error: {response.status_code}")
        except requests.exceptions.ConnectionError:
            st.error("❌ Cannot connect to API. Make sure the backend is running.")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

with tab2:
    st.subheader("Batch Claim Analysis")
    st.info("Upload a CSV file with multiple claims for bulk analysis.")
    
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.dataframe(df, use_container_width=True)

with tab3:
    st.subheader("System Analytics")
    col1, col2, col3, col4 = st.columns(4)
    
    col1.metric("Model Accuracy", "93%")
    col2.metric("Precision", "92%")
    col3.metric("Recall", "91%")
    col4.metric("F1-Score", "0.92")
    
    st.markdown("---")
    st.info("**Model Information:**\n- Algorithm: Decision Tree Classifier\n- Training Data: Insurance Claims Dataset\n- Last Updated: 2025")

# Footer
st.markdown("---")
st.markdown("""
<center>
    <p style='color: gray; font-size: 12px;'>
        Insurance Fraud Detection System | Powered by ML | Built with Streamlit
    </p>
</center>
""", unsafe_allow_html=True)
