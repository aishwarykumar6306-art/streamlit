import streamlit as st
import pandas as pd

# Load dataframe from session state
if "df" in st.session_state:
    df = st.session_state.df
else:
    df = pd.read_csv("Cars_cleaned.csv")
    st.session_state.df = df

st.markdown("""
    <style>
    .explorer-title {
        font-size: 38px;
        color: #0F172A;
        font-weight: 800;
        margin-bottom: 5px;
    }
    .explorer-subtitle {
        font-size: 16px;
        color: #475569;
        margin-bottom: 30px;
    }
    .details-card {
        background-color: #F8FAFC;
        border-radius: 12px;
        border: 1px solid #E2E8F0;
        padding: 20px;
        margin-top: 20px;
    }
    .details-title {
        font-size: 18px;
        font-weight: 700;
        color: #1E293B;
        margin-bottom: 12px;
        border-bottom: 1px solid #E2E8F0;
        padding-bottom: 6px;
    }
    .details-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 15px;
    }
    .details-item {
        background: white;
        padding: 10px;
        border-radius: 6px;
        border: 1px solid #F1F5F9;
    }
    .details-lbl {
        font-size: 11px;
        color: #94A3B8;
        text-transform: uppercase;
        font-weight: 500;
    }
    .details-val {
        font-size: 14px;
        font-weight: 600;
        color: #334155;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='explorer-title'>🔍 Interactive Data Explorer</div>", unsafe_allow_html=True)
st.markdown("<div class='explorer-subtitle'>Browse the complete used car repository, perform searches, apply custom filters, and export results.</div>", unsafe_allow_html=True)

# --------------------------------------------------
# COLLAPSIBLE FILTERS PANEL
# --------------------------------------------------
with st.expander("🛠 Advanced Search & Filter Options", expanded=True):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        search_query = st.text_input("🔍 Search Model / Name", placeholder="e.g. Swift, Scorpio, Audi...")
        
        all_brands = sorted(df['Company_Name'].unique().tolist())
        selected_brands = st.multiselect("Manufacturer Brand", options=all_brands)
        
        all_locations = sorted(df['Location'].unique().tolist())
        selected_locations = st.multiselect("Listing Location", options=all_locations)
        
    with col2:
        all_fuels = sorted(df['Fuel_Type'].unique().tolist())
        selected_fuels = st.multiselect("Fuel Type Option", options=all_fuels)
        
        all_trans = sorted(df['Transmission'].unique().tolist())
        selected_trans = st.multiselect("Transmission Type", options=all_trans)
        
        all_owners = sorted(df['Owner_Type'].unique().tolist())
        selected_owners = st.multiselect("Ownership Type", options=all_owners)
        
    with col3:
        min_p, max_p = float(df['Price'].min()), float(df['Price'].max())
        price_range = st.slider("Price Interval (Lakhs)", min_value=min_p, max_value=max_p, value=(min_p, max_p))
        
        min_y, max_y = int(df['Year'].min()), int(df['Year'].max())
        year_range = st.slider("Year Interval", min_value=min_y, max_value=max_y, value=(min_y, max_y))
        
        seats_options = sorted(df['Seats'].unique().tolist())
        selected_seats = st.multiselect("Seats Configuration", options=seats_options)

# Apply filters
filtered_df = df.copy()

if search_query:
    filtered_df = filtered_df[filtered_df['Name'].str.contains(search_query, case=False, na=False)]

if selected_brands:
    filtered_df = filtered_df[filtered_df['Company_Name'].isin(selected_brands)]

if selected_locations:
    filtered_df = filtered_df[filtered_df['Location'].isin(selected_locations)]

if selected_fuels:
    filtered_df = filtered_df[filtered_df['Fuel_Type'].isin(selected_fuels)]

if selected_trans:
    filtered_df = filtered_df[filtered_df['Transmission'].isin(selected_trans)]

if selected_owners:
    filtered_df = filtered_df[filtered_df['Owner_Type'].isin(selected_owners)]

if selected_seats:
    filtered_df = filtered_df[filtered_df['Seats'].isin(selected_seats)]

# Range filters
filtered_df = filtered_df[
    (filtered_df['Price'] >= price_range[0]) & (filtered_df['Price'] <= price_range[1]) &
    (filtered_df['Year'] >= year_range[0]) & (filtered_df['Year'] <= year_range[1])
]

# Display data size
st.markdown(f"**Found {filtered_df.shape[0]:,} listings** matching your current search parameters.")

if filtered_df.empty:
    st.warning("⚠️ No listings matched your selections. Try loosening the filter parameters.")
else:
    # --------------------------------------------------
    # DATAFRAME VIEW
    # --------------------------------------------------
    # Display clean dataframe columns (drop 'Unnamed: 0' index)
    display_cols = [c for c in filtered_df.columns if c not in ['Unnamed: 0']]
    st.dataframe(filtered_df[display_cols], use_container_width=True)
    
    # --------------------------------------------------
    # EXPORT FEATURE
    # --------------------------------------------------
    csv_data = filtered_df[display_cols].to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Filtered Listings as CSV",
        data=csv_data,
        file_name="filtered_used_cars.csv",
        mime="text/csv",
        use_container_width=True
    )
    
    # --------------------------------------------------
    # VEHICLE DETAIL CARD
    # --------------------------------------------------
    st.write("---")
    st.subheader("🔍 Selected Vehicle Details")
    st.write("Pick a vehicle below to view its full specification profile in detail:")
    
    # Create selectbox values as 'ID - Name (Year)'
    # Limit to first 100 for performance if list is huge
    select_limit_df = filtered_df.head(100)
    car_options = select_limit_df.index.tolist()
    
    def get_car_label(idx):
        row = select_limit_df.loc[idx]
        return f"{row['Company_Name']} {row['Model_Name']} ({row['Year']}) - {row['Price']}L - {row['Location']}"
        
    selected_idx = st.selectbox(
        "Select Car Profile",
        options=car_options,
        format_func=get_car_label
    )
    
    if selected_idx is not None:
        car = filtered_df.loc[selected_idx]
        
        st.markdown(f"""
            <div class='details-card'>
                <div class='details-title'>🚘 {car['Name']} ({car['Year']})</div>
                <div class='details-grid'>
                    <div class='details-item'>
                        <div class='details-lbl'>Manufacturer</div>
                        <div class='details-val'>{car['Company_Name']}</div>
                    </div>
                    <div class='details-item'>
                        <div class='details-lbl'>Model Group</div>
                        <div class='details-val'>{car['Model_Name']}</div>
                    </div>
                    <div class='details-item'>
                        <div class='details-lbl'>Location</div>
                        <div class='details-val'>{car['Location']}</div>
                    </div>
                    <div class='details-item'>
                        <div class='details-lbl'>Asking Price</div>
                        <div class='details-val' style='color:#EF4444;'>₹ {car['Price']} Lakhs</div>
                    </div>
                    <div class='details-item'>
                        <div class='details-lbl'>Kilometers Traveled</div>
                        <div class='details-val'>{car['Kilometers_Driven']:,} km</div>
                    </div>
                    <div class='details-item'>
                        <div class='details-lbl'>Fuel Type</div>
                        <div class='details-val'>{car['Fuel_Type']}</div>
                    </div>
                    <div class='details-item'>
                        <div class='details-lbl'>Transmission</div>
                        <div class='details-val'>{car['Transmission']}</div>
                    </div>
                    <div class='details-item'>
                        <div class='details-lbl'>Owner Level</div>
                        <div class='details-val'>{car['Owner_Type']} Owner</div>
                    </div>
                    <div class='details-item'>
                        <div class='details-lbl'>Seats Capacity</div>
                        <div class='details-val'>{car['Seats']} seats</div>
                    </div>
                    <div class='details-item'>
                        <div class='details-lbl'>Mileage Efficiency</div>
                        <div class='details-val'>{car['Mileage_value']} {car['Mileage_unit']}</div>
                    </div>
                    <div class='details-item'>
                        <div class='details-lbl'>Engine Capacity</div>
                        <div class='details-val'>{car['Engine_value']} {car['Engine_unit']}</div>
                    </div>
                    <div class='details-item'>
                        <div class='details-lbl'>Max Output Power</div>
                        <div class='details-val'>{car['Power_value']} {car['Power_unit']}</div>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
