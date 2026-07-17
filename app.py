import streamlit as st
import pandas as pd

# --------------------------------------------------
# GLOBAL PAGE CONFIGURATION
# --------------------------------------------------
st.set_page_config(
    page_title="Used Cars Valuation & Analytics",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------
# GLOBAL CUSTOM STYLING (THEME OVERRIDES)
# --------------------------------------------------
# Custom styles to unify typography, clean up borders, and modernise the sidebar
st.markdown("""
    <style>
    /* Global Background and Typography font styles */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Sidebar premium modifications */
    [data-testid="stSidebar"] {
        background-color: #F8FAFC;
        border-right: 1px solid #E2E8F0;
    }
    
    [data-testid="stSidebar"] .st-emotion-cache-1644tr7 {
        font-size: 15px;
        font-weight: 600;
        color: #334155;
    }
    
    /* Center the title/brand element inside the sidebar */
    .sidebar-brand {
        padding: 15px 0px;
        text-align: center;
        border-bottom: 2px solid #E2E8F0;
        margin-bottom: 20px;
    }
    .sidebar-brand-title {
        font-size: 20px;
        font-weight: 800;
        color: #1E3A8A;
        letter-spacing: 0.5px;
    }
    
    /* Clean up button hover states */
    .stButton>button {
        background-color: #2563EB;
        color: white;
        border-radius: 8px;
        font-weight: 600;
        padding: 10px 24px;
        border: none;
        transition: all 0.2s ease;
    }
    .stButton>button:hover {
        background-color: #1D4ED8;
        box-shadow: 0 4px 6px -1px rgba(37, 99, 235, 0.2);
    }
    
    /* Custom metric value stylings */
    [data-testid="stMetricValue"] {
        font-size: 30px;
        font-weight: 700;
        color: #1E3A8A;
    }
    
    /* Modern border and shadow rules for plots */
    .plot-container {
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid #E2E8F0;
    }
    </style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# DATA INGESTION & CACHING
# --------------------------------------------------
@st.cache_data
def load_dataset():
    # Read the pre-cleaned cars dataset
    data = pd.read_csv("Cars_cleaned.csv")
    
    # Simple cleanups just in case: make sure price has no zeroes or negative values
    data = data[data['Price'] > 0]
    
    return data

# Initialize the global dataframe in Session State if not already loaded
if "df" not in st.session_state:
    with st.spinner("⏳ Loading vehicle repository..."):
        st.session_state.df = load_dataset()

# --------------------------------------------------
# NAVIGATION DEFINITION
# --------------------------------------------------
# We set up a clean, structured directory matching our views
pages = {
    "Dashboard": [
        st.Page("pages/home.py", title="🏠 Market Overview", default=True)
    ],
    "Analytics": [
        st.Page("pages/analytics.py", title="📊 Interactive EDA")
    ],
    "AI Prediction": [
        st.Page("pages/predictor.py", title="🔮 Price Predictor")
    ],
    "Database Explorer": [
        st.Page("pages/explorer.py", title="🔍 Data Search & Export")
    ]
}

# Render sidebar header
st.sidebar.markdown("""
    <div class='sidebar-brand'>
        <div class='sidebar-brand-title'>🚗 AutoMarket AI</div>
        <div style='font-size: 11px; color: #64748B;'>Market Intelligence Hub</div>
    </div>
""", unsafe_allow_html=True)

# Run navigation routing
pg = st.navigation(pages)
pg.run()