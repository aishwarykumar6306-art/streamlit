import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import r2_score, mean_absolute_error

# Load dataframe from session state
if "df" in st.session_state:
    df = st.session_state.df
else:
    df = pd.read_csv("Cars_cleaned.csv")
    st.session_state.df = df

st.markdown("""
    <style>
    .predictor-title {
        font-size: 38px;
        color: #0F172A;
        font-weight: 800;
        margin-bottom: 5px;
    }
    .predictor-subtitle {
        font-size: 16px;
        color: #475569;
        margin-bottom: 30px;
    }
    .model-card {
        background-color: #F8FAFC;
        padding: 20px;
        border-radius: 16px;
        border: 1px dashed #CBD5E1;
        margin-bottom: 25px;
    }
    .stat-container {
        display: flex;
        gap: 30px;
        margin-top: 10px;
    }
    .stat-box {
        flex: 1;
        background: white;
        padding: 12px;
        border-radius: 8px;
        border: 1px solid #E2E8F0;
        text-align: center;
    }
    .stat-val {
        font-size: 22px;
        font-weight: 700;
        color: #0F766E;
    }
    .stat-lbl {
        font-size: 12px;
        color: #64748B;
        text-transform: uppercase;
    }
    .prediction-container {
        background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%);
        color: white;
        padding: 25px;
        border-radius: 16px;
        text-align: center;
        margin-top: 25px;
        box-shadow: 0 10px 15px -3px rgba(59, 130, 246, 0.3);
    }
    .prediction-val {
        font-size: 40px;
        font-weight: 800;
        margin: 10px 0;
    }
    .prediction-lbl {
        font-size: 15px;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        opacity: 0.9;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='predictor-title'>🔮 Used Cars Price Predictor</div>", unsafe_allow_html=True)
st.markdown("<div class='predictor-subtitle'>Input technical specifications and usage history below to estimate the current market value of a vehicle.</div>", unsafe_allow_html=True)

# --------------------------------------------------
# MODEL TRAINING (CACHED)
# --------------------------------------------------
@st.cache_resource
def train_model(data):
    # Select features & target
    features = [
        "Company_Name", "Year", "Kilometers_Driven", "Fuel_Type", 
        "Transmission", "Owner_Type", "Seats", "Mileage_value", 
        "Engine_value", "Power_value"
    ]
    target = "Price"
    
    X = data[features]
    y = data[target]
    
    # Train-test split (80-20)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Preprocessing pipelines
    num_cols = ["Year", "Kilometers_Driven", "Seats", "Mileage_value", "Engine_value", "Power_value"]
    cat_cols = ["Company_Name", "Fuel_Type", "Transmission", "Owner_Type"]
    
    preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), num_cols),
            ("cat", OneHotEncoder(handle_unknown="ignore"), cat_cols)
        ]
    )
    
    # Build complete model pipeline
    model_pipeline = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("regressor", RandomForestRegressor(n_estimators=80, random_state=42, n_jobs=-1))
        ]
    )
    
    # Train model
    model_pipeline.fit(X_train, y_train)
    
    # Evaluate
    y_pred = model_pipeline.predict(X_test)
    r2 = r2_score(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    
    return model_pipeline, r2, mae

# Show loader while training the first time
with st.spinner("🧠 Initializing AI Engine... Training Random Forest Model..."):
    model, r2_score_val, mae_val = train_model(df)

# Display model info
st.markdown(f"""
    <div class='model-card'>
        <strong>🤖 Machine Learning Model Status:</strong> Ready
        <div class='stat-container'>
            <div class='stat-box'>
                <div class='stat-val'>{r2_score_val*100:.1f}%</div>
                <div class='stat-lbl'>R² Score (Accuracy)</div>
            </div>
            <div class='stat-box'>
                <div class='stat-val'>₹ {mae_val:.2f} L</div>
                <div class='stat-lbl'>Mean Absolute Error</div>
            </div>
            <div class='stat-box'>
                <div class='stat-val'>{df.shape[0]:,}</div>
                <div class='stat-lbl'>Training Records</div>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

# --------------------------------------------------
# INPUT WIDGETS
# --------------------------------------------------
st.write("### 🛠 Vehicle Specifications")

col_a, col_b = st.columns(2)

with col_a:
    brand = st.selectbox("Manufacturer / Brand", sorted(df['Company_Name'].unique().tolist()))
    
    # Get typical values for this brand to serve as smart defaults
    brand_df = df[df['Company_Name'] == brand]
    default_year = int(brand_df['Year'].median())
    default_kms = int(brand_df['Kilometers_Driven'].median())
    default_seats = int(brand_df['Seats'].median()) if not brand_df['Seats'].empty else 5
    default_mileage = float(brand_df['Mileage_value'].median()) if not brand_df['Mileage_value'].empty else 18.0
    default_engine = int(brand_df['Engine_value'].median()) if not brand_df['Engine_value'].empty else 1200
    default_power = float(brand_df['Power_value'].median()) if not brand_df['Power_value'].empty else 90.0
    
    year = st.slider("Model Year", 
                     min_value=int(df['Year'].min()), 
                     max_value=int(df['Year'].max()), 
                     value=default_year)
    
    km_driven = st.number_input("Kilometers Driven (Odometer)", 
                                min_value=0, 
                                max_value=1000000, 
                                value=default_kms, 
                                step=1000)
    
    fuel_type = st.selectbox("Fuel Type", sorted(df['Fuel_Type'].unique().tolist()), 
                             index=sorted(df['Fuel_Type'].unique().tolist()).index('Diesel') if 'Diesel' in df['Fuel_Type'].unique() else 0)
    
    transmission = st.radio("Transmission Gearbox", sorted(df['Transmission'].unique().tolist()), horizontal=True)

with col_b:
    owner_type = st.selectbox("Owner Sequence", sorted(df['Owner_Type'].unique().tolist()))
    
    seats = st.selectbox("Number of Seats", sorted(df['Seats'].unique().tolist()), 
                         index=sorted(df['Seats'].unique().tolist()).index(default_seats) if default_seats in df['Seats'].unique() else 0)
    
    mileage = st.slider("Mileage Efficiency (kmpl / km/kg)", 
                        min_value=float(df['Mileage_value'].min()), 
                        max_value=float(df['Mileage_value'].max()), 
                        value=default_mileage, 
                        step=0.1)
    
    engine_cc = st.slider("Engine Capacity (CC Displacement)", 
                          min_value=int(df['Engine_value'].min()), 
                          max_value=int(df['Engine_value'].max()), 
                          value=default_engine, 
                          step=10)
    
    power_bhp = st.slider("Max Engine Power output (BHP)", 
                          min_value=float(df['Power_value'].min()), 
                          max_value=float(df['Power_value'].max()), 
                          value=default_power, 
                          step=1.0)

# Create record for prediction
input_data = pd.DataFrame([{
    "Company_Name": brand,
    "Year": year,
    "Kilometers_Driven": km_driven,
    "Fuel_Type": fuel_type,
    "Transmission": transmission,
    "Owner_Type": owner_type,
    "Seats": seats,
    "Mileage_value": mileage,
    "Engine_value": engine_cc,
    "Power_value": power_bhp
}])

st.write("")
st.divider()

# Predict and display
if st.button("🔮 Calculate Market Valuation Estimate", use_container_width=True):
    predicted_val = model.predict(input_data)[0]
    
    # Ensure prediction is positive
    predicted_val = max(predicted_val, 0.5)
    
    st.markdown(f"""
        <div class='prediction-container'>
            <div class='prediction-lbl'>Estimated Resale Market Value</div>
            <div class='prediction-val'>₹ {predicted_val:.2f} Lakhs</div>
            <div class='prediction-lbl'>Approx. ₹ {predicted_val * 100000:,.0f} INR</div>
            <div style='margin-top: 10px; font-size: 12px; opacity: 0.8;'>
                *Estimates are calculated using a Random Forest regression model on similar market listings.
            </div>
        </div>
    """, unsafe_allow_html=True)
else:
    st.info("ℹ️ Adjust specifications above and click 'Calculate Market Valuation Estimate' to generate values.")
