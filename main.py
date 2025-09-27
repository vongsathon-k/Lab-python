import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="แดชบอร์ดข้อมูลเงินทุนสตาร์ทอัพ",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_data
def load_data():
    df = pd.read_csv('startup_funding.csv')
    df['Amount in USD'] = df['Amount in USD'].astype(str).str.replace(',', '')
    df['Amount in USD'] = pd.to_numeric(df['Amount in USD'], errors='coerce')
    df['Date dd/mm/yyyy'] = pd.to_datetime(df['Date dd/mm/yyyy'], format='%d/%m/%Y', errors='coerce')
    return df

df = load_data()

st.title("แดชบอร์ดข้อมูลเงินทุนสตาร์ทอัพ")
st.markdown("---")

st.sidebar.header("ตัวกรอง")

dates = df['Date dd/mm/yyyy'].dropna()
if not dates.empty:
    min_d, max_d = dates.min().date(), dates.max().date()
    date_range = st.sidebar.date_input(
        "ช่วงวันที่:",
        value=(min_d, max_d),
        min_value=min_d,
        max_value=max_d
    )
else:
    date_range = None

industry_options = sorted(df['Industry Vertical'].dropna().unique().tolist())
default_industries = ["FinTech"] if "FinTech" in industry_options else (industry_options[:1] if industry_options else [])
industries = st.sidebar.multiselect("เลือกอุตสาหกรรม:", options=industry_options, default=default_industries)

filtered_df = df.copy()
if date_range and isinstance(date_range, (list, tuple)) and len(date_range) == 2:
    start_d, end_d = date_range
    filtered_df = filtered_df[
        (filtered_df['Date dd/mm/yyyy'] >= pd.to_datetime(start_d)) &
        (filtered_df['Date dd/mm/yyyy'] <= pd.to_datetime(end_d))
    ]

if industries:
    filtered_df = filtered_df[filtered_df['Industry Vertical'].isin(industries)]

def currency_fmt(v: float) -> str:
    try:
        if pd.isna(v):
            return "N/A"
        return f"${v:,.0f}"
    except Exception:
        return "N/A"


st.header("ตัวชี้วัดแบบง่าย")
col1, col2 = st.columns(2)

total_funding = filtered_df['Amount in USD'].sum()
total_deals = len(filtered_df)

col1.metric("เงินทุนรวม", currency_fmt(total_funding))
col2.metric("จำนวนดีล", f"{total_deals}")

st.markdown("---")

st.subheader("แนวโน้มเงินทุนรายเดือน")
if not filtered_df.empty and not filtered_df['Date dd/mm/yyyy'].isna().all():
    ts = (
        filtered_df.dropna(subset=['Date dd/mm/yyyy'])
        .assign(month=lambda d: d['Date dd/mm/yyyy'].dt.to_period('M').dt.to_timestamp())
        .groupby('month', as_index=False)['Amount in USD'].sum()
    )
    if not ts.empty:
        fig_ts = px.line(ts, x='month', y='Amount in USD')
        st.plotly_chart(fig_ts, use_container_width=True)
    else:
        st.info("ไม่มีข้อมูลสำหรับการวิเคราะห์ไทม์ไลน์")
else:
    st.info("ไม่มีข้อมูลวันที่สำหรับการวิเคราะห์ไทม์ไลน์")

st.subheader("เงินทุนตามอุตสาหกรรม (Top 5)")
by_ind = (
    filtered_df.groupby('Industry Vertical', as_index=False)['Amount in USD'].sum()
    .sort_values('Amount in USD', ascending=False).head(5)
)
if not by_ind.empty:
    fig_ind = px.bar(by_ind, x='Industry Vertical', y='Amount in USD')
    st.plotly_chart(fig_ind, use_container_width=True)
else:
    st.info("ไม่มีข้อมูลสำหรับตัวกรองที่เลือก")

st.subheader("ตารางข้อมูล")
table_df = filtered_df[[
    'Date dd/mm/yyyy', 'Startup Name', 'Industry Vertical', 'Investors Name', 'Amount in USD'
]].copy()
table_df['Amount in USD'] = table_df['Amount in USD'].apply(lambda x: currency_fmt(x) if pd.notnull(x) else "N/A")
st.dataframe(table_df, use_container_width=True, hide_index=True)

st.markdown("---")
st.caption("สร้างด้วย Streamlit | ข้อมูล: startup_funding.csv")