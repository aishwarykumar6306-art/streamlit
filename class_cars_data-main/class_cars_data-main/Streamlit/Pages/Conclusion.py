import streamlit as st

st.set_page_config(
    page_title="Conclusion",
    layout="wide"
)

# -----------------------------
# CUSTOM CSS
# -----------------------------

st.markdown("""
<style>

.stApp{
background-image:url("https://images.unsplash.com/photo-1492144534655-ae79c964c9d7?auto=format&fit=crop&w=1600&q=80");
background-size:cover;
background-position:center;
background-attachment:fixed;
}

.main-container{

background:rgba(255,255,255,0.12);
backdrop-filter:blur(12px);
padding:50px;
border-radius:20px;
margin-top:30px;
box-shadow:0px 8px 30px rgba(0,0,0,0.35);

}

.title{

font-size:60px;
font-weight:bold;
text-align:center;
background:linear-gradient(to right,#ffffff,#dbeafe);
-webkit-background-clip:text;
-webkit-text-fill-color:transparent;
margin-bottom:15px;

}

.subtitle{

text-align:center;
font-size:24px;
color:white;
margin-bottom:40px;

}

.section{

background:rgba(255,255,255,0.18);
padding:30px;
border-radius:18px;
margin-bottom:25px;
color:white;
font-size:20px;
line-height:1.9;

}

.heading{

font-size:32px;
font-weight:bold;
margin-bottom:15px;
color:white;

}

.footer{

text-align:center;
font-size:30px;
font-weight:bold;
color:white;
padding:30px;

}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# MAIN PAGE
# -----------------------------

st.markdown("""
<div class="main-container">

<div class="title">
Project Conclusion
</div>

<div class="subtitle">
Used Cars Exploratory Data Analysis
</div>

<div class="section">

<div class="heading">
Conclusion
</div>

The Exploratory Data Analysis successfully revealed important insights from the
used cars dataset. By analyzing various vehicle attributes such as brand,
fuel type, transmission, ownership, manufacturing year, and selling price,
we gained a better understanding of the factors influencing the used car market.

The project demonstrated how data preprocessing, visualization, and statistical
analysis can transform raw data into meaningful business insights. These findings
can support customers in making informed purchasing decisions while helping
dealers understand market demand and pricing trends.

Overall, this analysis highlights the importance of data-driven decision making
and provides a strong foundation for future predictive analytics projects.

</div>

<div class="section">

<div class="heading">
Future Scope
</div>

• Develop Machine Learning models for accurate price prediction.<br>
• Integrate real-time vehicle listing data.<br>
• Build recommendation systems for buyers.<br>
• Deploy the application on cloud platforms.<br>
• Add advanced dashboards with interactive filters and business reports.

</div>

<div class="section">

<div class="heading">
Final Remark
</div>

This project demonstrates the complete workflow of data analysis—from data
cleaning and preprocessing to visualization and insight generation. It serves
as a practical example of applying Python, Pandas, and Streamlit to solve
real-world analytical problems and supports better business decision-making
through meaningful data exploration.

</div>

<div class="footer">

Thank You

</div>

</div>

""", unsafe_allow_html=True)