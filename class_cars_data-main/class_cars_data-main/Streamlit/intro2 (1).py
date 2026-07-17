import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Cars EDA",
    page_icon="🚗",
    layout="wide"
)

df = pd.read_csv("Cars_cleaned.csv")

# Title
st.title("🚗 Used Cars Exploratory Data Analysis")

st.subheader("Interactive Dashboard using Streamlit")

st.divider()

# KPI Cards

col1, col2, col3, col4 = st.columns(4)

col1.metric("🚘 Total Cars", df.shape[0])
col2.metric("📋 Features", df.shape[1])
col3.metric("❌ Missing Values", df.isnull().sum().sum())
col4.metric("📑 Duplicates", df.duplicated().sum())

st.divider()

# About Dataset

st.header("📖 About Dataset")

st.write("""
The Used Cars dataset contains detailed information about second-hand
vehicles available for sale.

This dashboard has been developed to perform an Exploratory Data Analysis (EDA)
to understand pricing patterns, brand popularity, fuel preferences,
vehicle specifications, and market trends.

The project is completely developed using:

- Python
- Pandas
- NumPy
- Plotly
- Streamlit
""")

st.divider()

# Business Objectives

st.header("🎯 Business Objectives")

col1, col2 = st.columns(2)

with col1:
    st.success("Understand car price distribution")
    st.success("Compare different brands")
    st.success("Study fuel type popularity")
    st.success("Analyze transmission")

with col2:
    st.success("Find price influencing factors")
    st.success("Study ownership patterns")
    st.success("Discover market trends")
    st.success("Generate business insights")

st.divider()

# Dataset Summary

st.header("📊 Dataset Summary")

summary = pd.DataFrame({
    "Property": [
        "Rows",
        "Columns",
        "Missing Values",
        "Duplicate Records"
    ],
    "Value": [
        df.shape[0],
        df.shape[1],
        df.isnull().sum().sum(),
        df.duplicated().sum()
    ]
})

st.dataframe(summary, use_container_width=True)

st.divider()

# Feature Information

st.header("📋 Dataset Features")

feature_info = pd.DataFrame({
    "Feature": df.columns,
    "Data Type": df.dtypes.astype(str),
    "Missing Values": df.isnull().sum().values
})

st.dataframe(feature_info, use_container_width=True)

st.divider()

# Numerical Summary

st.header("📈 Numerical Summary")

st.dataframe(df.describe(), use_container_width=True)

st.divider()

# Sample Dataset

st.header("🚗 Sample Dataset")

st.dataframe(df.head(10), use_container_width=True)

st.divider()

# Footer

st.caption("Developed by Mayank Raghuwanshi | Data Analytics Project")