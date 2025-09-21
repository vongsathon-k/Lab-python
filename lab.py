# from util import print_multiplication_table
import pandas as pd
import streamlit as st

st.title('Product List')
st.write('Here is the list of products:')
st.header('products.csv')
if session_state := st.session_state.get('name'):
    st.write(f'Welcome back, {session_state}!')
else:
    st.switch_page("pages/2_setting.py")


uploaded_file = st.file_uploader("Choose a file", type=["csv", "xlsx"])
if uploaded_file is not None:
    try:
        data = pd.read_csv(uploaded_file)
    except Exception as e:
        data = pd.read_excel(uploaded_file)
    st.write(data)
else:
    data = pd.read_csv('products.csv')

    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Sale", "1200", "400")
    with col2:
        st.metric("Revenue", "1200", "20 %")
    with col3:
        st.metric("User", "John Doe", "")
    name = st.text_input('Enter your name', 'Type here...')
    st.write(f'Hello, {name}!')


    st.line_chart(data['sales'])

    if st.button('Load Data'):
        st.header('Product Data')
        st.subheader('Here is the product data:')
        st.write(data)
