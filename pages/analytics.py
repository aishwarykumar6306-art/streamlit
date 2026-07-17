import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go

# Load dataframe from session state
if "df" in st.session_state:
    df = st.session_state.df
else:
    df = pd.read_csv("Cars_cleaned.csv")
    st.session_state.df = df

st.markdown("""
    <style>
    .analytics-title {
        font-size: 38px;
        color: #0F172A;
        font-weight: 800;
        margin-bottom: 5px;
    }
    .analytics-subtitle {
        font-size: 16px;
        color: #475569;
        margin-bottom: 30px;
    }
    .chart-container {
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 16px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
        border: 1px solid #E2E8F0;
        margin-bottom: 25px;
    }
    .section-title {
        font-size: 20px;
        font-weight: 700;
        color: #1E293B;
        margin-bottom: 15px;
        border-bottom: 2px solid #E2E8F0;
        padding-bottom: 8px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='analytics-title'>📊 Interactive Exploratory Data Analysis</div>", unsafe_allow_html=True)
st.markdown("<div class='analytics-subtitle'>Slice and dice the used cars market data using the sidebar filters to explore key distributions and patterns.</div>", unsafe_allow_html=True)

# --------------------------------------------------
# SIDEBAR FILTERS
# --------------------------------------------------
st.sidebar.header("🎯 Data Filters")

# Year filter
min_year, max_year = int(df['Year'].min()), int(df['Year'].max())
selected_years = st.sidebar.slider(
    "📅 Model Year Range",
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year)
)

# Price filter
min_price, max_price = float(df['Price'].min()), float(df['Price'].max())
selected_prices = st.sidebar.slider(
    "💰 Price Range (Lakhs)",
    min_value=min_price,
    max_value=max_price,
    value=(min_price, max_price)
)

# Brands multiselect
all_brands = sorted(df['Company_Name'].unique().tolist())
selected_brands = st.sidebar.multiselect(
    "🚘 Select Brands",
    options=all_brands,
    default=all_brands[:8] # Default to top 8 brands for a clean view initially
)

# Fuel Type multiselect
all_fuels = sorted(df['Fuel_Type'].unique().tolist())
selected_fuels = st.sidebar.multiselect(
    "⛽ Fuel Type",
    options=all_fuels,
    default=all_fuels
)

# Transmission multiselect
all_trans = sorted(df['Transmission'].unique().tolist())
selected_trans = st.sidebar.multiselect(
    "⚙️ Transmission Type",
    options=all_trans,
    default=all_trans
)

# Apply filters
filtered_df = df[
    (df['Year'] >= selected_years[0]) & (df['Year'] <= selected_years[1]) &
    (df['Price'] >= selected_prices[0]) & (df['Price'] <= selected_prices[1])
]

# Filter list conditions
if selected_brands:
    filtered_df = filtered_df[filtered_df['Company_Name'].isin(selected_brands)]
if selected_fuels:
    filtered_df = filtered_df[filtered_df['Fuel_Type'].isin(selected_fuels)]
if selected_trans:
    filtered_df = filtered_df[filtered_df['Transmission'].isin(selected_trans)]

# Check if filtered data is empty
if filtered_df.empty:
    st.warning("⚠️ No cars match the selected filters. Please adjust your filters in the sidebar!")
else:
    # --------------------------------------------------
    # ROW 1: Key Summary Stats of filtered data
    # --------------------------------------------------
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Cars Selected", f"{filtered_df.shape[0]:,}")
    with col2:
        st.metric("Avg Filtered Price", f"{filtered_df['Price'].mean():.2f} Lakhs")
    with col3:
        st.metric("Avg Odometer", f"{filtered_df['Kilometers_Driven'].mean():,.0f} km")
    
    st.write("")

    # --------------------------------------------------
    # ROW 2: Price Distribution & Brand Market Share
    # --------------------------------------------------
    r2_col1, r2_col2 = st.columns(2)
    
    with r2_col1:
        st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
        st.markdown("<div class='section-title'>💰 Price Distribution</div>", unsafe_allow_html=True)
        fig_price = px.histogram(
            filtered_df,
            x="Price",
            color="Transmission",
            nbins=30,
            marginal="box",
            opacity=0.75,
            color_discrete_map={"Manual": "#3B82F6", "Automatic": "#EF4444"},
            labels={"Price": "Price (Lakhs INR)"},
            barmode="overlay"
        )
        fig_price.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(showgrid=True, gridcolor="#F1F5F9"),
            yaxis=dict(showgrid=True, gridcolor="#F1F5F9"),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(t=5, l=5, r=5, b=5)
        )
        st.plotly_chart(fig_price, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with r2_col2:
        st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
        st.markdown("<div class='section-title'>🚘 Brand Market Distribution</div>", unsafe_allow_html=True)
        brand_counts = filtered_df['Company_Name'].value_counts().reset_index()
        brand_counts.columns = ['Brand', 'Count']
        fig_brand = px.bar(
            brand_counts.head(15),
            x='Count',
            y='Brand',
            orientation='h',
            color='Count',
            color_continuous_scale=px.colors.sequential.Blues,
            labels={'Count': 'Number of Listings', 'Brand': 'Brand'}
        )
        fig_brand.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(showgrid=True, gridcolor="#F1F5F9"),
            yaxis=dict(autorange="reversed"),
            coloraxis_showscale=False,
            margin=dict(t=5, l=5, r=5, b=5)
        )
        st.plotly_chart(fig_brand, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # --------------------------------------------------
    # ROW 3: Kilometers Driven vs Price & Fuel Type Breakdown
    # --------------------------------------------------
    r3_col1, r3_col2 = st.columns([3, 2])
    
    with r3_col1:
        st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
        st.markdown("<div class='section-title'>🚗 Kilometers Driven vs Price</div>", unsafe_allow_html=True)
        # Cap kilometers to remove extreme outliers for standard visual exploration
        cap_kms = st.checkbox("Cap Odometer view at 200,000 km for visibility", value=True)
        scatter_df = filtered_df.copy()
        if cap_kms:
            scatter_df = scatter_df[scatter_df['Kilometers_Driven'] <= 200000]
            
        fig_scatter = px.scatter(
            scatter_df,
            x="Kilometers_Driven",
            y="Price",
            color="Fuel_Type",
            size="Car_Age",
            hover_data=["Name", "Year"],
            opacity=0.6,
            labels={"Kilometers_Driven": "Odometer (km)", "Price": "Price (Lakhs)"},
            color_discrete_sequence=px.colors.qualitative.Safe
        )
        fig_scatter.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(showgrid=True, gridcolor="#F1F5F9"),
            yaxis=dict(showgrid=True, gridcolor="#F1F5F9"),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
            margin=dict(t=5, l=5, r=5, b=5)
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with r3_col2:
        st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
        st.markdown("<div class='section-title'>⛽ Fuel Type Split</div>", unsafe_allow_html=True)
        fuel_counts = filtered_df['Fuel_Type'].value_counts().reset_index()
        fuel_counts.columns = ['Fuel Type', 'Count']
        fig_fuel = px.pie(
            fuel_counts,
            values="Count",
            names="Fuel Type",
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig_fuel.update_layout(
            margin=dict(t=5, l=5, r=5, b=5),
            legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5)
        )
        st.plotly_chart(fig_fuel, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # --------------------------------------------------
    # ROW 4: Engine vs Power & Correlation Matrix
    # --------------------------------------------------
    r4_col1, r4_col2 = st.columns(2)
    
    with r4_col1:
        st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
        st.markdown("<div class='section-title'>⚡ Engine Displacement (CC) vs Power (BHP)</div>", unsafe_allow_html=True)
        fig_engine_power = px.scatter(
            filtered_df,
            x="Engine_value",
            y="Power_value",
            color="Price",
            size="Seats",
            hover_data=["Name"],
            color_continuous_scale="Plasma",
            labels={"Engine_value": "Engine displacement (CC)", "Power_value": "Max Power (BHP)"}
        )
        fig_engine_power.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(showgrid=True, gridcolor="#F1F5F9"),
            yaxis=dict(showgrid=True, gridcolor="#F1F5F9"),
            margin=dict(t=5, l=5, r=5, b=5)
        )
        st.plotly_chart(fig_engine_power, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
    with r4_col2:
        st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
        st.markdown("<div class='section-title'>🔗 Numeric Feature Correlation</div>", unsafe_allow_html=True)
        # Select numeric features
        num_cols = ["Year", "Kilometers_Driven", "Seats", "Price", "Mileage_value", "Engine_value", "Power_value", "Car_Age"]
        corr_matrix = filtered_df[num_cols].corr()
        
        fig_corr = go.Figure(data=go.Heatmap(
            z=corr_matrix.values,
            x=corr_matrix.columns,
            y=corr_matrix.index,
            colorscale='RdBu',
            zmin=-1, zmax=1,
            text=np.round(corr_matrix.values, 2),
            texttemplate="%{text}",
            hoverongaps = False
        ))
        fig_corr.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            margin=dict(t=5, l=5, r=5, b=5)
        )
        st.plotly_chart(fig_corr, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
