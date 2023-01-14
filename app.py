import streamlit as st
import osmnx as ox
import pydeck as pdk
import pandas as pd

hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        .viewerBadge_container__1QSob {visibility: hidden;}
        .css-1dp5vir {visibility: hidden;}
        .reportview-container {background: #AE8F00}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)




#set page config
st.set_page_config(

    page_title="Pipedream Network Editor",
    #page_icon="app/assets/icon.svg",
    #layout="wide",
    initial_sidebar_state="expanded",
)


#make tab menu
st.sidebar.title('Pipedream Networks')
page = st.sidebar.radio("", ["Montreal", "Austin"])

