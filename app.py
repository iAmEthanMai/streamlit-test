# Standard library imports
import math

# Third-party imports
import numpy as np
import pandas as pd
import pydeck as pdk
import streamlit as st
import time

#import osmnx as ox
#import pickle
#import networkx as nx



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

def hex_to_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))



data1 = [['NO1', [-73.597650,45.522920], '#5e29ff'],['NO2',[-73.615480,45.522560], '#5e29ff']]
data2 = pd.DataFrame(data1, columns=['id','position','color'])
data2['color'] = data2['color'].apply(hex_to_rgb)






#def get_node(lat, lon):
#    from osmnx import distance
#    #get node closest to coordinates
#    node = distance.nearest_nodes(G, lon, lat)
#    return node


def get_path(G, source, destination):
    #find the shortest path between the nodeA and nodeB
    path = nx.shortest_path(G, source=source, target=destination, weight='length')
    return path

#def get_elevation_profile(G, path):


node_count = 0
pipe_count = 0





def render_map():

    view_state = pdk.ViewState(
        latitude=45.5019,
        longitude=-73.5674,
        zoom=10
    )



    layer2 = pdk.Layer(
        "ScatterplotLayer",
        data=data2,
        pickable=True,
        #make cursor pointy


        auto_highlight=True,
        get_position='position',
        get_color='color',
        get_radius=200,
    )
    
    r = pdk.Deck(layers=[layer2], initial_view_state=view_state, tooltip={"text": "{id}"})
    
    st.pydeck_chart(r)




hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        .css-1dp5vir {visibility: hidden;}
        .reportview-container {background: #AE8F00}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)








if page == "Montreal":




    render_map()
    
    tab1, tab2, tab3, tab4 = st.tabs(["Add node", "Add pipe", "Delete node", "Delete pipe"])
    data = np.random.randn(10, 1)

    with tab1:

        #st.write(nodes)
        col1, col2, col3 = st.columns(3)
        with col1:
            lat = st.number_input('Latitude', min_value=0.0, max_value=90.0, value=45.522560)
        with col2:
            lon = st.number_input('Longitude', min_value=-180.0, max_value=180.0, value=-73.615480)
        with col3:
            node_id = st.text_input('Node ID', value='NO' + str(node_count), key='tab12')
        st.write(data2)
        #wait for user to press enter
        if st.button('Submit', key='tab1'):
            st.success(f'Node: {node_id} created')
            node_count += 1
            
            







    with tab2:



        col1, col2, col3 = st.columns(3)
        with col1:
            #make dropdown menu with all nodes
            nodeA = st.selectbox('Source', ['NO1', 'NO2', 'NO3'], key='tab21')


        with col2:
            nodeB = st.selectbox('Destination', ['NO2', 'NO3'], key='tab22')
        with col3:
            pipe_id = st.text_input('Pipe ID', value='PI1', key='tab23')

        
        elevations = np.random.randn(1000, 1)
        window_size = 5

        # Create an empty array to store the smoothed elevations
        smoothed_elevations = np.empty(len(elevations))

        # Loop through the elevations and apply the moving average
        for i in range(len(elevations)):
            # Calculate the start and end indices for the window
            start = max(0, i - window_size)
            end = min(len(elevations), i + window_size + 1)

            # Calculate the average of the values in the window
            average = np.mean(elevations[start:end])

            # Store the average in the smoothed_elevations array and make it the absolute value

            smoothed_elevations[i] = abs(average)

        #st.area_chart(smoothed_elevations)
        #area chart with color #AE8F00
        
        
        st.area_chart(smoothed_elevations)
        #display informations about the pipe
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Length", "1000m", delta='+65m')
        with col2:
            st.metric("Elevation", "+60m", delta='+5m')

        data3 = [[pipe_id,'NO1', 'NO2', '1000m',  '+65m']]
        data4 = pd.DataFrame(data3, columns=['ID','source','destination','length','elevation'])
        #make dataframe take the whole width
        st.dataframe(data4.style.set_properties(**{'text-align': 'left'}))

        if st.button('Submit', key='tab24'):
            st.success(f'Pipe: {pipe_id} created') 

    with tab3:
        node_id = st.selectbox('Node ID', ['NO1', 'NO2', 'NO3'], key='tab31')
        #wait for user to press enter
        if st.button('Submit', key='tab33'):
            st.success(f'Node: {node_id} deleted')


    with tab4:
        pipe_id = st.selectbox('Pipe ID', ['PI1','PI2'], key='tab41')

        #wait for user to press enter
        if st.button('Submit', key='tab4'):
            st.success(f'Pipe: {pipe_id} deleted')





elif page == "Austin":
    #st.title('Austin Network')
    view_state_austin = pdk.ViewState(
        latitude=30.2672,
        longitude=-97.7431,
        zoom=10
    )

    r = pdk.Deck(layers=[], initial_view_state=view_state_austin, tooltip={})
    
    st.pydeck_chart(r)
    


#
##G = nx.read_gpickle('montreal_graph.pickle')
#G = ox.graph_from_place('Montreal, Quebec, Canada')
#
#
#print('so far so good')
#
## get the node closest to coordinates
#nodeB = ox.nearest_nodes(G, -73.597650,45.522920)
#nodeA = ox.nearest_nodes(G, -73.615480,45.522560)
#
#
#
#lat_nodeA = G.nodes[nodeA]['y']
#lon_nodeA = G.nodes[nodeA]['x']
#
#
#lat_nodeB = G.nodes[nodeB]['y']
#lon_nodeB = G.nodes[nodeB]['x']
#
#
##find the shortest path between the nodeA and nodeB
#pathAB = nx.shortest_path(G, source=nodeA, target=nodeB, weight='length')
#
#
## Define the list of node IDs
#
## Create an empty list to store the coordinates
#coords = []
#
## Iterate over the node IDs
#for node_id in pathAB:
#    # Get the attributes of the node
#    node_attr = G.nodes[node_id]
#    
#    # Get the latitude and longitude coordinates
#    lat = node_attr['y']
#    lon = node_attr['x']
#    
#    # Append the coordinates to the list
#    coords.append([lon, lat])
#
#data = [['pipe1', '#ed1c24', coords]]
#
#
#
#df = pd.DataFrame(data, columns=['name', 'color', 'path'])
#
#
#
#
#
#st.dataframe(df)
#
#def hex_to_rgb(h):
#    h = h.lstrip('#')
#    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
#
#df['color'] = df['color'].apply(hex_to_rgb)
#
#view_state = pdk.ViewState(
#    latitude=45.5019,
#    longitude=-73.5674,
#    zoom=10
#)
#
#
#
#
#
#data1 = [[[lon_nodeA,lat_nodeA], '#00FF00'],[[lon_nodeB,lat_nodeB], '#00FF00']]
#data2 = pd.DataFrame(data1, columns=['position','color'])
#data2['color'] = data2['color'].apply(hex_to_rgb)
#
#
#
#layer1 = pdk.Layer(
#    type='PathLayer',
#    data=df,
#    pickable=True,
#    get_color='color',
#    width_scale=20,
#    width_min_pixels=2,
#    get_path='path',
#    get_width=5,
#)
#
#layer2 = pdk.Layer(
#    type='ScatterplotLayer',
#    data=data2,
#    get_position='position',
#    get_color='color',
#    get_radius=100,
#    
#)
#
#
#
#
#
##
##
##svg_icon = {
##    "url": "assets/icon.svg",
##    "width": 20,
##    "height": 20
##}
##
##layer2 = pdk.Layer(
##    type='ScatterplotLayer',
##    data=data2,
##    get_position='position',
##    get_color='color',
##    get_radius=100,
##    # Set the icon property with the SVG icon dictionary
##    icon=svg_icon
##)
##
#
#
#r = pdk.Deck(layers=[layer2,layer1], initial_view_state=view_state, tooltip={'text': '{name}'})
#
#st.pydeck_chart(r)
#










