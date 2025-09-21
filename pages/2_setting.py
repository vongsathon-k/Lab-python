import streamlit as st

st.set_page_config(page_title="Settings", layout="wide")

st.title('Settings')
st.write('Adjust the settings below:')

name =  st.text_input('name')
if st.button('Save'):
    st.success(f'Settings saved for {name}!')
    st.session_state['name'] = name