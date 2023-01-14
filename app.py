import streamlit as st
import osmnx as ox
import pydeck as pdk

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


st.write('hello world')
st.write('this is a test')

view_state_austin = pdk.ViewState(
        latitude=30.2672,
        longitude=-97.7431,
        zoom=10
    )
r = pdk.Deck(layers=[], initial_view_state=view_state_austin, tooltip={})
    


st.pydeck_chart(r)
