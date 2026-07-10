import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from PIL import Image

st.set_page_config(
    page_title="Adidas Analytics Dashboard",
    page_icon="👟",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ================= CSS ====================

st.markdown("""
<style>

#MainMenu {visibility:hidden;}
footer {visibility:hidden;}

.stApp{
background:linear-gradient(135deg,#050816,#111827,#0f172a);
}

section[data-testid="stSidebar"]{
background:#0b1120;
border-right:1px solid #1e293b;
}

.block-container{
padding-top:1rem;
padding-bottom:1rem;
}

div[data-testid="metric-container"]{
background:rgba(255,255,255,.05);
border:1px solid rgba(255,255,255,.08);
padding:18px;
border-radius:18px;
box-shadow:0 10px 25px rgba(0,0,0,.25);
}

h1,h2,h3,h4{
color:white;
}

label{
color:white !important;
}

</style>
""",unsafe_allow_html=True)

# ================= LOGO ====================

try:
    logo=Image.open("adidas.jpg")
    c1,c2=st.columns([1,5])

    with c1:
        st.image(logo,width=120)

    with c2:
        st.title("Adidas Sales Analytics Dashboard")
        st.caption("Executive Business Intelligence Dashboard")

except:
    st.title("Adidas Sales Analytics Dashboard")

# ================= LOAD DATA ====================

@st.cache_data
def load_data():

    df=pd.read_csv("Adidas_Uzbekcha.csv")

    df["Hisob-faktura sanasi"]=pd.to_datetime(
        df["Hisob-faktura sanasi"],
        errors="coerce"
    )

    return df

df=load_data()

# ================= SIDEBAR ====================

st.sidebar.title("Dashboard Filter")

region=st.sidebar.multiselect(
    "Hudud",
    sorted(df["Hudud"].dropna().unique()),
    default=sorted(df["Hudud"].dropna().unique())
)

city=st.sidebar.multiselect(
    "Shahar",
    sorted(df["Shahar"].dropna().unique()),
    default=sorted(df["Shahar"].dropna().unique())
)

product=st.sidebar.multiselect(
    "Mahsulot",
    sorted(df["Mahsulot"].dropna().unique()),
    default=sorted(df["Mahsulot"].dropna().unique())
)

sales_type=st.sidebar.multiselect(
    "Sotuv usuli",
    sorted(df["Sotuv usuli"].dropna().unique()),
    default=sorted(df["Sotuv usuli"].dropna().unique())
)

filtered=df[
(df["Hudud"].isin(region))
&
(df["Shahar"].isin(city))
&
(df["Mahsulot"].isin(product))
&
(df["Sotuv usuli"].isin(sales_type))
]

# ================= KPI ====================

sales=filtered["Jami savdo (so'm)"].sum()

profit=filtered["Operatsion foyda (so'm)"].sum()

units=filtered["Sotilgan birlik"].sum()

margin=filtered["Operatsion marja"].mean()

retailers=filtered["Chakana sotuvchi"].nunique()

cities=filtered["Shahar"].nunique()

regions=filtered["Hudud"].nunique()

products=filtered["Mahsulot"].nunique()

r1,r2,r3,r4=st.columns(4)

r1.metric(
"Daromad",
f"{sales:,.0f}"
)

r2.metric(
"Foyda",
f"{profit:,.0f}"
)

r3.metric(
"Sotilgan miqdor",
f"{units:,.0f}"
)

r4.metric(
"Marja",
f"{margin:.2%}"
)

r5,r6,r7,r8=st.columns(4)

r5.metric(
"Sotuvchilar",
retailers
)

r6.metric(
"Shaharlar",
cities
)

r7.metric(
"Viloyatlar",
regions
)

r8.metric(
"Mahsulotlar",
products
)


#======================= Dashboard ========================================================================
st.divider()

st.subheader("Oylar va Hududlar bo'yicha sotuv")

left,right=st.columns([2,1])

with left:
  #====================== Oylik sotuvni hisoblash =====================================================
    monthly = filtered.groupby(filtered["Hisob-faktura sanasi"].dt.to_period("M"))["Jami savdo (so'm)"].sum().reset_index()
    monthly["Hisob-faktura sanasi"]=monthly["Hisob-faktura sanasi"].astype(str)
  #Line graph
    line_graph = px.line(
        monthly,
        x="Hisob-faktura sanasi",
        y="Jami savdo (so'm)",
        markers=True,
        template="plotly_dark")

    line_graph.update_layout(
        height=420,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",

    )

    st.plotly_chart(line_graph,use_container_width=True)


with right:

    region_sales=filtered.groupby("Hudud")["Jami savdo (so'm)"].sum().reset_index()

    fig2=px.pie(
        region_sales,
        names="Hudud",
        values="Jami savdo (so'm)",
        hole=.6,
        template="plotly_dark"
    )

    fig2.update_layout(
        height=420,
        paper_bgcolor="rgba(0,0,0,0)"
    )

    st.plotly_chart(fig2,use_container_width=True)

# ================= PRODUCT PERFORMANCE =================

st.divider()
st.subheader("Mahsulot ko'rsatkichlari")

left, right = st.columns(2)

with left:

    product_sales = (
        filtered
        .groupby("Mahsulot")["Jami savdo (so'm)"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )

    fig = px.bar(
        product_sales,
        x="Mahsulot",
        y="Jami savdo (so'm)",
        color="Jami savdo (so'm)",
        text_auto=".2s",
        template="plotly_dark",
        color_continuous_scale="Viridis"
    )

    fig.update_layout(
        height=500,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis_title="",
        yaxis_title="Daromad"
    )

    st.plotly_chart(fig, use_container_width=True)

with right:

    product_profit = (
        filtered
        .groupby("Mahsulot")["Operatsion foyda (so'm)"]
        .sum()
        .reset_index()
    )

    fig = px.pie(
        product_profit,
        names="Mahsulot",
        values="Operatsion foyda (so'm)",
        hole=.55,
        template="plotly_dark"
    )

    fig.update_layout(
        height=500,
        paper_bgcolor="rgba(0,0,0,0)"
    )

    st.plotly_chart(fig, use_container_width=True)

# ================= RETAILER ANALYSIS =================

st.divider()
st.subheader("Savdo ko'rsatkichi")

left, right = st.columns(2)

retailer = (
    filtered
    .groupby("Chakana sotuvchi")
    .agg({
        "Jami savdo (so'm)":"sum",
        "Operatsion foyda (so'm)":"sum"
    })
    .reset_index()
)

with left:

    top10 = retailer.sort_values(
        "Jami savdo (so'm)",
        ascending=False
    ).head(10)

    fig = px.bar(
        top10,
        x="Jami savdo (so'm)",
        y="Chakana sotuvchi",
        orientation="h",
        color="Jami savdo (so'm)",
        template="plotly_dark",
        color_continuous_scale="Turbo"
    )

    fig.update_layout(
        height=500,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )

    st.plotly_chart(fig,use_container_width=True)

with right:

    fig = px.treemap(
        retailer,
        path=["Chakana sotuvchi"],
        values="Jami savdo (so'm)",
        color="Operatsion foyda (so'm)",
        template="plotly_dark",
        color_continuous_scale="RdYlGn"
    )

    fig.update_layout(
        height=500,
        paper_bgcolor="rgba(0,0,0,0)"
    )

    st.plotly_chart(fig,use_container_width=True)



# ==========================
# FINAL SUMMARY
# ==========================

st.divider()

st.markdown(f"""

# Dashboard Xulosasi



""")