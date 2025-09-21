import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np

# Configure page
st.set_page_config(
    page_title="แดชบอร์ดข้อมูลเงินทุนสตาร์ทอัพ",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('startup_funding.csv')
    # Clean amount column - remove commas and convert to numeric
    df['Amount in USD'] = df['Amount in USD'].astype(str).str.replace(',', '')
    df['Amount in USD'] = pd.to_numeric(df['Amount in USD'], errors='coerce')
    # Convert date column
    df['Date dd/mm/yyyy'] = pd.to_datetime(df['Date dd/mm/yyyy'], format='%d/%m/%Y', errors='coerce')
    return df

df = load_data()

# Dashboard Title
st.title("🚀 แดชบอร์ดข้อมูลเงินทุนสตาร์ทอัพ")
st.markdown("---")

# Sidebar filters
st.sidebar.header("🔍 ตัวกรอง")
industries = st.sidebar.multiselect(
    "เลือกอุตสาหกรรม:",
    options=df['Industry Vertical'].unique(),
    default=["FinTech"] if "FinTech" in df['Industry Vertical'].unique() else [df['Industry Vertical'].unique()[0]]
)

cities = st.sidebar.multiselect(
    "เลือกเมือง:",
    options=df['City  Location'].unique(),
    default=df['City  Location'].unique()[:10]
)

# Filter data
filtered_df = df[
    (df['Industry Vertical'].isin(industries)) & 
    (df['City  Location'].isin(cities))
]

# Key Metrics
st.header("📊 ตัวชี้วัดหลัก")
col1, col2, col3, col4 = st.columns(4)

with col1:
    total_funding = filtered_df['Amount in USD'].sum()
    st.metric(
        label="เงินทุนรวม",
        value=f"${total_funding:,.0f}",
        delta=f"{len(filtered_df)} ดีล"
    )

with col2:
    avg_funding = filtered_df['Amount in USD'].mean()
    st.metric(
        label="เงินทุนเฉลี่ย",
        value=f"${avg_funding:,.0f}",
        delta=f"ต่อสตาร์ทอัพ"
    )

with col3:
    total_startups = len(filtered_df['Startup Name'].unique())
    st.metric(
        label="สตาร์ทอัพทั้งหมด",
        value=f"{total_startups:,}",
        delta=f"บริษัทเฉพาะ"
    )

with col4:
    total_investors = len(filtered_df['Investors Name'].unique())
    st.metric(
        label="นักลงทุนทั้งหมด",
        value=f"{total_investors:,}",
        delta=f"นักลงทุนเฉพาะ"
    )

st.markdown("---")

# Charts Section
st.header("📈 การวิเคราะห์และกราฟ")

# Two columns for charts
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    # Industry-wise funding
    st.subheader("💼 เงินทุนตามอุตสาหกรรม")
    industry_funding = filtered_df.groupby('Industry Vertical')['Amount in USD'].sum().sort_values(ascending=False).head(10)
    
    if not industry_funding.empty:
        fig1 = px.bar(
            x=industry_funding.values,
            y=industry_funding.index,
            orientation='h',
            labels={'x': 'เงินทุนรวม (USD)', 'y': 'อุตสาหกรรม'},
            title="10 อุตสาหกรรมที่ได้เงินทุนสูงสุด"
        )
        fig1.update_layout(height=400)
        st.plotly_chart(fig1, use_container_width=True)
    else:
        st.info("ไม่มีข้อมูลสำหรับตัวกรองที่เลือก")

with chart_col2:
    # Investment type distribution
    st.subheader("🎯 ประเภทการลงทุน")
    investment_types = filtered_df['InvestmentnType'].value_counts().head(8)
    
    if not investment_types.empty:
        fig2 = px.pie(
            values=investment_types.values,
            names=investment_types.index,
            title="การกระจายตัวของประเภทการลงทุน"
        )
        fig2.update_layout(height=400)
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("ไม่มีข้อมูลสำหรับตัวกรองที่เลือก")

# Full width charts
col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    # City-wise funding
    st.subheader("🏙️ เมืองที่ได้เงินทุนสูงสุด")
    city_funding = filtered_df.groupby('City  Location')['Amount in USD'].sum().sort_values(ascending=False).head(10)
    
    if not city_funding.empty:
        fig3 = px.bar(
            x=city_funding.index,
            y=city_funding.values,
            labels={'x': 'เมือง', 'y': 'เงินทุนรวม (USD)'},
            title="10 เมืองที่ได้เงินทุนสูงสุด"
        )
        fig3.update_layout(height=400, xaxis_tickangle=-45)
        st.plotly_chart(fig3, use_container_width=True)
    else:
        st.info("ไม่มีข้อมูลสำหรับตัวกรองที่เลือก")

with col_chart2:
    # Timeline analysis
    st.subheader("📅 แนวโน้มเงินทุนตามเวลา")
    if not filtered_df['Date dd/mm/yyyy'].isna().all() and not filtered_df.empty:
        monthly_funding = filtered_df.groupby(filtered_df['Date dd/mm/yyyy'].dt.to_period('M'))['Amount in USD'].sum()
        
        if not monthly_funding.empty:
            fig4 = px.line(
                x=monthly_funding.index.astype(str),
                y=monthly_funding.values,
                labels={'x': 'เดือน', 'y': 'เงินทุนรวม (USD)'},
                title="แนวโน้มเงินทุนรายเดือน"
            )
            fig4.update_layout(height=400, xaxis_tickangle=-45)
            st.plotly_chart(fig4, use_container_width=True)
        else:
            st.info("ไม่มีข้อมูลสำหรับการวิเคราะห์ไทม์ไลน์")
    else:
        st.info("ไม่มีข้อมูลวันที่สำหรับการวิเคราะห์ไทม์ไลน์")

st.markdown("---")

# Top Startups Table
st.header("🏆 สตาร์ทอัพที่ได้เงินทุนสูงสุด")

# Create top startups dataframe
top_startups = filtered_df.nlargest(20, 'Amount in USD')[
    ['Startup Name', 'Industry Vertical', 'City  Location', 'Investors Name', 'Amount in USD', 'InvestmentnType']
].copy()

top_startups['Amount in USD'] = top_startups['Amount in USD'].apply(lambda x: f"${x:,.0f}")

st.dataframe(
    top_startups,
    use_container_width=True,
    hide_index=True
)

st.markdown("---")

# Detailed Data Table
st.header("📋 ข้อมูลการลงทุนโดยละเอียด")

# Search functionality
search_term = st.text_input("🔍 ค้นหาสตาร์ทอัพ นักลงทุน หรืออุตสาหกรรม:")

if search_term:
    search_df = filtered_df[
        filtered_df['Startup Name'].str.contains(search_term, case=False, na=False) |
        filtered_df['Investors Name'].str.contains(search_term, case=False, na=False) |
        filtered_df['Industry Vertical'].str.contains(search_term, case=False, na=False)
    ]
else:
    search_df = filtered_df

# Display table with formatting
display_df = search_df[
    ['Date dd/mm/yyyy', 'Startup Name', 'Industry Vertical', 'City  Location', 
     'Investors Name', 'InvestmentnType', 'Amount in USD']
].copy()

display_df['Amount in USD'] = display_df['Amount in USD'].apply(lambda x: f"${x:,.0f}" if pd.notnull(x) else "N/A")

st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True
)

# Summary statistics
st.markdown("---")
st.header("📊 สถิติสรุป")

col1, col2 = st.columns(2)

with col1:
    st.subheader("สถิติอุตสาหกรรม")
    industry_stats = filtered_df.groupby('Industry Vertical').agg({
        'Amount in USD': ['count', 'sum', 'mean'],
        'Startup Name': 'nunique'
    }).round(0)
    
    industry_stats.columns = ['จำนวนดีล', 'เงินทุนรวม', 'เงินทุนเฉลี่ย', 'สตาร์ทอัพเฉพาะ']
    industry_stats = industry_stats.sort_values('เงินทุนรวม', ascending=False).head(10)
    st.dataframe(industry_stats, use_container_width=True)

with col2:
    st.subheader("สถิติเมือง")
    city_stats = filtered_df.groupby('City  Location').agg({
        'Amount in USD': ['count', 'sum', 'mean'],
        'Startup Name': 'nunique'
    }).round(0)
    
    city_stats.columns = ['จำนวนดีล', 'เงินทุนรวม', 'เงินทุนเฉลี่ย', 'สตาร์ทอัพเฉพาะ']
    city_stats = city_stats.sort_values('เงินทุนรวม', ascending=False).head(10)
    st.dataframe(city_stats, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("**แดชบอร์ดสร้างด้วย Streamlit** | แหล่งข้อมูล: startup_funding.csv")