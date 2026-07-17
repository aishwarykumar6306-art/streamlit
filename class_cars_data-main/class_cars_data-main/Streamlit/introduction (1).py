import streamlit as st
import pandas as pd
import numpy as np

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Cars Dataset Analysis",
    page_icon="🚗",
    layout="wide"
)

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

df = pd.read_csv("Cars_cleaned.csv")

# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown("""
<style>

.main{
    background-color:#f5f7fa;
}

.title{
    font-size:50px;
    color:#1f4e79;
    text-align:center;
    font-weight:bold;
}

.subtitle{
    font-size:24px;
    color:gray;
    text-align:center;
}

.card{
    background:white;
    padding:20px;
    border-radius:12px;
    box-shadow:0px 3px 15px rgba(0,0,0,0.15);
    text-align:center;
}

.metric{
    font-size:34px;
    color:#FF4B4B;
    font-weight:bold;
}

.heading{

    font-size:34px;
    color:#003566;
    font-weight:bold;
}

.small{
font-size:18px;
color:#444;
}

.footer{
text-align:center;
color:gray;
padding:20px;
}

</style>

""", unsafe_allow_html=True)

# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.markdown(
"""
<div class='title'>
🚗 Used Cars Exploratory Data Analysis
</div>
""", unsafe_allow_html=True)

st.markdown(
"""
<div class='subtitle'>
Interactive Dashboard using Python • Pandas • Plotly • Streamlit
</div>
""", unsafe_allow_html=True)

st.write("")

# --------------------------------------------------
# HERO IMAGE
# --------------------------------------------------

st.image(
"https://images.unsplash.com/photo-1503376780353-7e6692767b70",
use_container_width=True
)

st.write("")

# --------------------------------------------------
# KPI CARDS
# --------------------------------------------------

col1,col2,col3,col4=st.columns(4)

with col1:

    st.markdown(f"""
    <div class='card'>
    <div class='metric'>{df.shape[0]}</div>
    <div>Total Cars</div>
    </div>
    """,unsafe_allow_html=True)

with col2:

    st.markdown(f"""
    <div class='card'>
    <div class='metric'>{df.shape[1]}</div>
    <div>Features</div>
    </div>
    """,unsafe_allow_html=True)

with col3:

    st.markdown(f"""
    <div class='card'>
    <div class='metric'>{df.select_dtypes(include='object').shape[1]}</div>
    <div>Categorical Features</div>
    </div>
    """,unsafe_allow_html=True)

with col4:

    st.markdown(f"""
    <div class='card'>
    <div class='metric'>{df.select_dtypes(exclude='object').shape[1]}</div>
    <div>Numerical Features</div>
    </div>
    """,unsafe_allow_html=True)

st.write("")

# --------------------------------------------------
# ABOUT DATASET
# --------------------------------------------------

st.markdown("<div class='heading'>📖 About Dataset</div>",unsafe_allow_html=True)

st.write("""

The Used Cars Dataset contains detailed information about second-hand vehicles
listed for sale.

The primary objective of this project is to analyze the dataset,
discover hidden patterns, identify important trends, and understand
the factors affecting used car prices.

This dashboard has been developed using **Python**, **Pandas**, **NumPy**,
**Plotly**, and **Streamlit** to provide an interactive experience for
data exploration.

""")

# --------------------------------------------------
# BUSINESS OBJECTIVE
# --------------------------------------------------

st.markdown("<div class='heading'>🎯 Business Objectives</div>",unsafe_allow_html=True)

st.markdown("""

✔ Understand used car market trends

✔ Analyze price distribution

✔ Compare different brands

✔ Study fuel type popularity

✔ Analyze transmission preferences

✔ Identify factors affecting selling price

✔ Build insights useful for buyers and sellers

""")

st.write("")

# --------------------------------------------------
# DATASET SUMMARY
# --------------------------------------------------

st.markdown("<div class='heading'>📊 Dataset Summary</div>",unsafe_allow_html=True)

summary=pd.DataFrame({

"Property":[

"Rows",
"Columns",
"Duplicate Records",
"Missing Values",
"Memory Usage"

],

"Value":[

df.shape[0],
df.shape[1],
df.duplicated().sum(),
df.isna().sum().sum(),
str(round(df.memory_usage().sum()/1024,2))+" KB"

]

})

st.dataframe(summary,use_container_width=True)

# --------------------------------------------------
# FEATURES
# --------------------------------------------------

st.markdown("<div class='heading'>📋 Dataset Features</div>",unsafe_allow_html=True)

feature=pd.DataFrame({

"Feature Name":df.columns,

"Data Type":df.dtypes.astype(str),

"Missing Values":df.isna().sum().values

})

st.dataframe(feature,use_container_width=True)

# --------------------------------------------------
# NUMERICAL SUMMARY
# --------------------------------------------------

st.markdown("<div class='heading'>📈 Numerical Summary</div>",unsafe_allow_html=True)

st.dataframe(df.describe(),use_container_width=True)

# --------------------------------------------------
# SAMPLE DATA
# --------------------------------------------------

st.markdown("<div class='heading'>🚘 Sample Dataset</div>",unsafe_allow_html=True)

st.dataframe(df.head(15),use_container_width=True)

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.write("")

st.markdown("""

---

### 🛠 Technologies Used

- Python
- Pandas
- NumPy
- Plotly
- Streamlit

---

""")

st.markdown("""
<div class='footer'>
Developed by <b>Mayank Raghuwanshi</b><br>
Data Analytics | Data Science | Aritificial Intelligence
</div>
""",unsafe_allow_html=True)