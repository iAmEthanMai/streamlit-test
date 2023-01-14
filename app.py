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

node = ox.get_nearest_node(G, (37.788022, -122.399797))

# get the latitude and longitude of the node
lat, lon = ox.get_node_lat_lon(G, node)

st.write(lat)
st.write(lon)

