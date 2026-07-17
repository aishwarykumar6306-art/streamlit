# Complete corrected app.py

from pathlib import Path
from datetime import datetime
import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Used Car Analytics Dashboard", page_icon="🚗", layout="wide")

st.markdown("""
<style>
.main{background-color:#F5F7FA;}
h1,h2,h3{color:#003366;}
[data-testid="metric-container"]{
background:#fff;border-radius:12px;padding:20px;
box-shadow:0 3px 10px rgba(0,0,0,.15);}
</style>
""", unsafe_allow_html=True)

BASE_DIR = Path(__file__).resolve().parent
df = pd.read_csv(BASE_DIR/"Cars_cleaned.csv")

num_cols=["Price","Kilometers_Driven","Mileage_value","Engine_value","Power_value","Seats","Year"]
for c in num_cols:
    if c in df.columns:
        df[c]=pd.to_numeric(df[c],errors="coerce")

if "Year" in df.columns:
    df["Car Age"]=datetime.now().year-df["Year"]

st.sidebar.title("🔍 Filters")
for col,label in [("Company_Name","Brand"),("Fuel_Type","Fuel Type"),("Transmission","Transmission"),("Location","Location")]:
    if col in df.columns:
        vals=sorted(df[col].dropna().unique())
        sel=st.sidebar.multiselect(label,vals,default=vals)
        df=df[df[col].isin(sel)]

st.title("🚗 Used Car Analytics Dashboard")
c1,c2,c3,c4,c5=st.columns(5)
c1.metric("Total Cars",len(df))
c2.metric("Average Price",f"₹ {df['Price'].mean():,.2f}" if not df.empty else "₹0")
c3.metric("Brands",df["Company_Name"].nunique())
c4.metric("Locations",df["Location"].nunique())
c5.metric("Average Age",f"{df['Car Age'].mean():.1f} Years" if not df.empty else "0")

l,r=st.columns(2)
with l:
    st.plotly_chart(px.histogram(df,x="Price",nbins=30,title="Price Distribution"),use_container_width=True)
with r:
    bc=df["Company_Name"].value_counts().head(10)
    st.plotly_chart(px.bar(x=bc.index,y=bc.values,labels={"x":"Brand","y":"Cars"},title="Top 10 Brands"),use_container_width=True)

l,r=st.columns(2)
with l:
    f=df["Fuel_Type"].value_counts()
    st.plotly_chart(px.pie(values=f.values,names=f.index,hole=.5,title="Fuel Type Distribution"),use_container_width=True)
with r:
    t=df["Transmission"].value_counts()
    st.plotly_chart(px.bar(x=t.index,y=t.values,title="Transmission Distribution"),use_container_width=True)

l,r=st.columns(2)
with l:
    st.plotly_chart(px.scatter(df,x="Kilometers_Driven",y="Price",color="Fuel_Type",size="Engine_value",size_max=35,hover_name="Name",title="Kilometers Driven vs Price"),use_container_width=True)
with r:
    st.plotly_chart(px.scatter(df,x="Car Age",y="Price",color="Transmission",title="Car Age vs Price"),use_container_width=True)

l,r=st.columns(2)
with l:
    avg=df.groupby("Company_Name")["Price"].mean().sort_values(ascending=False).head(10)
    st.plotly_chart(px.bar(x=avg.values,y=avg.index,orientation="h",title="Average Price by Brand"),use_container_width=True)
with r:
    city=df.groupby("Location")["Price"].mean().sort_values()
    st.plotly_chart(px.bar(x=city.index,y=city.values,title="Average Price by Location"),use_container_width=True)

st.subheader("Correlation Heatmap")
num=df.select_dtypes(include="number").dropna(axis=1,how="all")
fig,ax=plt.subplots(figsize=(10,6))
sns.heatmap(num.corr(numeric_only=True),annot=True,cmap="Blues",ax=ax)
st.pyplot(fig)

l,r=st.columns(2)
with l:
    st.plotly_chart(px.box(df,x="Transmission",y="Price",title="Price by Transmission"),use_container_width=True)
with r:
    if "Owner_Type" in df.columns:
        st.plotly_chart(px.box(df,x="Owner_Type",y="Price",title="Price by Owner Type"),use_container_width=True)

st.subheader("Brand Performance")
brand=df.groupby("Company_Name").agg(
Cars=("Company_Name","count"),
Avg_Price=("Price","mean"),
Avg_Mileage=("Mileage_value","mean"),
Avg_Engine=("Engine_value","mean"),
Avg_Power=("Power_value","mean")).round(2)
st.dataframe(brand,use_container_width=True)

st.subheader("Top 15 Most Expensive Cars")
cols=[c for c in ["Name","Company_Name","Price","Location","Fuel_Type","Transmission"] if c in df.columns]
st.dataframe(df.sort_values("Price",ascending=False)[cols].head(15),use_container_width=True)

with st.expander("View Dataset"):
    st.dataframe(df,use_container_width=True)
