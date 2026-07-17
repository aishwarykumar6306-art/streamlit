from pathlib import Path

import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Used Cars EDA",
    layout="wide"
)

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "Cars_cleaned.csv"

df = pd.read_csv(DATA_PATH)

st.title("Used Cars Exploratory Data Analysis")

st.write(
    """
    This project performs Exploratory Data Analysis (EDA) on a used cars dataset.
    The objective is to understand the structure of the dataset, identify data quality
    issues, analyze numerical and categorical features, and generate insights that
    support better decision-making.
    """
)

st.divider()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Records", df.shape[0])
col2.metric("Total Features", df.shape[1])
col3.metric("Missing Values", df.isnull().sum().sum())
col4.metric("Duplicate Records", df.duplicated().sum())

st.divider()

st.header("Project Objectives")

st.markdown("""
- Understand the structure of the dataset.
- Analyze numerical and categorical variables.
- Identify missing and duplicate values.
- Study price distribution and market trends.
- Compare different brands and fuel types.
- Generate business insights from the data.
""")

st.divider()

st.header("Dataset Information")

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

st.header("Feature Details")

feature_info = pd.DataFrame({
    "Feature": df.columns,
    "Data Type": df.dtypes.astype(str),
    "Missing Values": df.isnull().sum().values
})

st.dataframe(feature_info, use_container_width=True)

st.divider()

st.header("Statistical Summary")

st.dataframe(df.describe(), use_container_width=True)

st.divider()

st.header("Sample Data")

st.dataframe(df.head(10), use_container_width=True)

st.divider()

st.markdown(
    "<center><b>Used Cars EDA Project</b><br>Developed using Python, Pandas and Streamlit</center>",
    unsafe_allow_html=True
)