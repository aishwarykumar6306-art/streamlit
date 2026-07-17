import streamlit as st
import pandas as pd

# Load dataframe from session state
if "df" in st.session_state:
    df = st.session_state.df
else:
    df = pd.read_csv("Cars_cleaned.csv")
    st.session_state.df = df

# Page styling
st.markdown("""
    <style>
    .main-title {
        font-size: 42px;
        color: #1E3A8A;
        font-weight: 800;
        margin-bottom: 5px;
        font-family: 'Inter', sans-serif;
    }
    .sub-title {
        font-size: 18px;
        color: #6B7280;
        margin-bottom: 25px;
    }
    .kpi-container {
        display: flex;
        justify-content: space-between;
        gap: 15px;
        margin-bottom: 25px;
    }
    .kpi-card {
        flex: 1;
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 16px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
        border: 1px solid #F3F4F6;
        text-align: center;
        transition: transform 0.2s ease-in-out;
    }
    .kpi-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        border-color: #3B82F6;
    }
    .kpi-value {
        font-size: 32px;
        font-weight: 700;
        color: #2563EB;
        margin-bottom: 5px;
    }
    .kpi-label {
        font-size: 14px;
        color: #4B5563;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .section-header {
        font-size: 24px;
        color: #1F2937;
        font-weight: 700;
        margin-top: 30px;
        margin-bottom: 15px;
        border-left: 5px solid #2563EB;
        padding-left: 12px;
    }
    .objective-card {
        background: #F8FAFC;
        border-left: 4px solid #10B981;
        padding: 15px;
        border-radius: 0 12px 12px 0;
        margin-bottom: 10px;
    }
    .objective-text {
        font-size: 15px;
        color: #334155;
        font-weight: 550;
    }
    .footer {
        text-align: center;
        color: #9CA3AF;
        padding: 30px 0 10px 0;
        font-size: 13px;
        border-top: 1px solid #E5E7EB;
        margin-top: 50px;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("<div class='main-title'>🚗 Used Cars Market Analysis</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>Explore trends, analyze features, and predict prices on secondary car sales market dataset.</div>", unsafe_allow_html=True)

# Banner
st.image("https://images.unsplash.com/photo-1503376780353-7e6692767b70", use_container_width=True, caption="Used Cars Exploration Dashboard")

st.markdown("<div class='section-header'>📊 Market Overview at a Glance</div>", unsafe_allow_html=True)

# KPI Cards using Streamlit columns & custom HTML for styling
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.markdown("""
        <div class='kpi-card'>
            <div class='kpi-value'>{:,.0f}</div>
            <div class='kpi-label'>Total Vehicles</div>
        </div>
    """.format(df.shape[0]), unsafe_allow_html=True)

with kpi2:
    st.markdown("""
        <div class='kpi-card'>
            <div class='kpi-value'>{}</div>
            <div class='kpi-label'>Available Brands</div>
        </div>
    """.format(df['Company_Name'].nunique()), unsafe_allow_html=True)

with kpi3:
    st.markdown("""
        <div class='kpi-card'>
            <div class='kpi-value'>{:,.1f}L</div>
            <div class='kpi-label'>Avg Price (Lakhs)</div>
        </div>
    """.format(df['Price'].mean()), unsafe_allow_html=True)

with kpi4:
    st.markdown("""
        <div class='kpi-card'>
            <div class='kpi-value'>{:,.0f} km</div>
            <div class='kpi-label'>Avg Odometer</div>
        </div>
    """.format(df['Kilometers_Driven'].mean()), unsafe_allow_html=True)

st.write("")

# Layout: About and Objectives
col_left, col_right = st.columns([3, 2])

with col_left:
    st.markdown("<div class='section-header'>📖 About the Dataset</div>", unsafe_allow_html=True)
    st.write("""
        This dataset represents detailed records of second-hand vehicles in major metropolitan areas. 
        It comprises a wealth of information including vehicular technical specifications (Engine power, engine capacity, mileage efficiency, seats), 
        usage details (odometer reading, transmission, age), and the target resale value. 
        
        Analyzing this information helps auto-resellers, individual consumers, and industry analysts understand factors driving car depreciation and demand.
    """)
    
    st.markdown("<div class='section-header'>📋 Features Dictionary Overview</div>", unsafe_allow_html=True)
    
    feature_meta = pd.DataFrame({
        "Feature": ["Name / Brand", "Year / Car Age", "Location", "Kilometers Driven", "Fuel Type", "Transmission", "Engine Value", "Power Value", "Price"],
        "Description": ["Model name & manufacturing brand", "Year of manufacture / years since registration", "City/region of list", "Total kilometers traveled", "Type of fuel used (Diesel, Petrol, CNG, LPG, Electric)", "Gearbox type (Manual, Automatic)", "Engine size in cubic centimeters (CC)", "Max power output in brake horsepower (BHP)", "Resale price (in Lakhs INR / local currency units)"],
        "Data Type": ["Categorical (String)", "Numerical (Integer)", "Categorical (String)", "Numerical (Integer)", "Categorical (String)", "Categorical (String)", "Numerical (Integer)", "Numerical (Float)", "Numerical (Float) (Target)"]
    })
    st.dataframe(feature_meta, use_container_width=True, hide_index=True)

with col_right:
    st.markdown("<div class='section-header'>🎯 Core Objectives</div>", unsafe_allow_html=True)
    
    objectives = [
        "🔍 **Market Valuation Analysis:** Unravel standard pricing levels and distributions across various vehicle age bands.",
        "📊 **Feature Interdependencies:** Visualize the relationship between kilometers driven, age, and residual price.",
        "⚡ **Technical Performance Impact:** Understand how engine displacement (CC) and brake horsepower (BHP) affect market value.",
        "🔮 **Price Predictive Modeling:** Assist buyers and sellers in predicting car prices using standard machine learning.",
        "🌍 **Demographic Segmentation:** Contrast differences in demand patterns across distinct locations."
    ]
    
    for obj in objectives:
        st.markdown(f"""
            <div class='objective-card'>
                <div class='objective-text'>{obj}</div>
            </div>
        """, unsafe_allow_html=True)

st.markdown("<div class='section-header'>📈 Dataset Quick Statistics</div>", unsafe_allow_html=True)
st.dataframe(df.describe().T, use_container_width=True)

st.markdown("<div class='section-header'>🚘 Sample Dataset Explorer Preview</div>", unsafe_allow_html=True)
st.dataframe(df.head(10), use_container_width=True)

# Footer
st.markdown("""
    <div class='footer'>
        🚗 Used Cars Exploratory Data Analysis & Pricing Dashboard • Streamlit Hub<br>
        Developed for Streamlit Cloud deployment
    </div>
""", unsafe_allow_html=True)
