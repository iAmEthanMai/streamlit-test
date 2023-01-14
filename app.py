import streamlit as st


hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        .css-1dp5vir {visibility: hidden;}
        .reportview-container {background: #AE8F00}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)


st.write('hello world')
st.write('this is a test')

