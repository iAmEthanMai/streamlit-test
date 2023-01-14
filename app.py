import streamlit as st
import osmnx as ox


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

node = ox.distance.get_nearest_nodes(G, (37.788022, -122.399797))
st.write(node)

