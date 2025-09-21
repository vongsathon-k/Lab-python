import streamlit as st

st.set_page_config(page_title="Rectangle Area Calculator", layout="centered")   

st.title('Rectangle Area Calculator')
width = st.slider('Select a width', 0, 100, 25)
height = st.slider('Select a height', 0, 100, 25)

# Area calculation updates automatically when sliders change
area = width * height
st.write(f'Current area: {area}')

if st.button('Submit'):
    st.success(f'Submitted! Final area: {area}')
