# Standard library imports
#import math

# Third-party imports
import numpy as np
import pandas as pd
import pydeck as pdk
import streamlit as st
import time

import osmnx as ox
import pickle
import networkx as nx


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




NODE_COST = 1000
PIPE_COST = 10 #$/m


#@st.cache(suppress_st_warning=True)
#def init_app():
#    #load the graph
#    return nx.read_gpickle('montreal_graph.pickle')


#@st.cache(suppress_st_warning=True)
#def load_graph():
#    return nx.read_gpickle('montreal_graph.pickle')
#
#G = load_graph()
#st.write('Number of nodes: {}'.format(len(G.nodes())))



def display_elevation():
    st.write('Elevation profile')
    #array that looks like a mountain
    elevations = [10,10,10.5,10.5,10.5,10.5,10.5,11,11,11,11,11.5,11.5,11.5,11.5,11.5,11,11,11,11,11,11.5,11.5,11,11,11,11,11,11.5,11.5,11,11,11,11,11,10.5,10,9.5,9,9,9,9,9,9,9,9,9,9.5,9.5,9.5,9.5,9.5,9.5,9.5,9.5]


    st.area_chart(elevations)







def hex_to_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))



data1 = [['Alice', [-73.597650,45.522920], [94, 41, 255]],['Ethan',[-73.615480,45.522560], [94, 41, 255]]]
data2 = pd.DataFrame(data1, columns=['id','position','color'])
#data2['color'] = data2['color'].apply(hex_to_rgb)







path = [221113177, 7017289706, 221113204, 221113274, 1968551667, 1818906521, 221106435, 31701022, 1968519515, 221106437, 867675395, 1825900796, 1818923469, 127962991, 1969845704, 437865929, 1969845669, 438331727, 1969845685, 340240112, 340239570, 3971845889, 3594666108]

path_coords = [[-73.6154152, 45.5228018], [-73.6150456, 45.523219], [-73.614842, 45.5234489], [-73.6142856, 45.524077], [-73.6138297, 45.5238799], [-73.6129038, 45.5234795], [-73.6124261, 45.523269], [-73.6119569, 45.5237979], [-73.611709, 45.5240775], [-73.6114317, 45.5243844], [-73.6111397, 45.5247076], [-73.6108518, 45.5250262], [-73.6105335, 45.5253784], [-73.6101948, 45.5257533], [-73.609889, 45.526103], [-73.6095802, 45.5264562], [-73.6092626, 45.5267345], [-73.6088471, 45.5270204], [-73.6084223, 45.5272486], [-73.6041118, 45.5252418], [-73.6008161, 45.5237722], [-73.5985465, 45.5227497], [-73.5982829, 45.5230282]]




data = [['PI0', '#5e29ff', []]]










def get_path(G, source, destination):
    #find the shortest path between the nodeA and nodeB
    path = nx.shortest_path(G, source=source, target=destination, weight='length')
    return path




if 'pipe_df' not in st.session_state:
    st.session_state.pipe_df = pd.DataFrame(data, columns=['id', 'color', 'path'])
    #st.session_state.pipe_df['color'] = st.session_state.pipe_df['color'].apply(hex_to_rgb)


if 'node_id_count' not in st.session_state:
    st.session_state.node_id_count = 0
if 'node_df' not in st.session_state:
    st.session_state.node_df = pd.DataFrame(data1, columns=['id','position','color'])

if 'scatter_layer' not in st.session_state:
    st.session_state.scatter_layer = pdk.Layer(
        "ScatterplotLayer",
        data=st.session_state.node_df,
        pickable=True,
        #make cursor pointy


        auto_highlight=True,
        get_position='position',
        get_color='color',
        get_radius=200,
    )





layer1 = pdk.Layer(
    type='PathLayer',
    data=st.session_state.pipe_df,
    pickable=True,
    get_color='color',
    width_scale=20,
    width_min_pixels=2,
    get_path='path',
    get_width=5,
    auto_highlight=True,
)

if 'path_layer' not in st.session_state:
    st.session_state.path_layer = layer1

if 'pipe_count' not in st.session_state:
    st.session_state.pipe_count = 0


if 'total_cost' not in st.session_state:
    st.session_state.total_cost = len(st.session_state.node_df) * NODE_COST






def render_map():

    view_state = pdk.ViewState(
        latitude=45.5019,
        longitude=-73.5674,
        zoom=10
    )


    
    r = pdk.Deck(layers=[st.session_state.scatter_layer, st.session_state.path_layer], initial_view_state=view_state, tooltip={"text": "{id}"})
    
    st.pydeck_chart(r)


#MainMenu {visibility: hidden;}

hide_menu_style = """
        <style>
        
        footer {visibility: hidden;}
        .css-1dp5vir {visibility: hidden;}
        .reportview-container {background: #AE8F00}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)








if page == "Montreal":


    
    render_map()
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Add node", "Add pipe", "Delete node", "Delete pipe", "Load config"])
    data = np.random.randn(10, 1)

    with tab1:

        with st.form(key='tab1'):
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                lat = st.number_input('Latitude', min_value=0.0, max_value=90.0, value=45.532560)
            with col2:
                lon = st.number_input('Longitude', min_value=-180.0, max_value=180.0, value=-73.615480)
            with col3:
                node_id = st.text_input('Node ID', value='NO' + str(st.session_state.node_id_count))
            with col4:
                color = st.color_picker('Colour', value='#5E29FF')
                color = hex_to_rgb(color)
            if st.form_submit_button('Add node'):
                
                #check if node is already at this location
                if st.session_state.node_df['position'].isin([[lon, lat]]).any():
                    st.error('A node already exists at this location')
                else:

                    st.session_state.node_id_count += 1
                    st.session_state.total_cost += NODE_COST
                    st.session_state.node_df = st.session_state.node_df.append({'id': node_id, 'position': [lon, lat], 'color': color}, ignore_index=True)
                    st.session_state.scatter_layer = pdk.Layer(
                        "ScatterplotLayer",
                        data=st.session_state.node_df,
                        pickable=True,
                        #make cursor pointy
                        auto_highlight=True,
                        get_position='position',
                        get_color='color',
                        get_radius=200,
                    )
                    st.experimental_rerun()





    with tab2:

        with st.form(key='tab2'):
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                nodeA = st.selectbox('Source', st.session_state.node_df['id'])
            with col2:
                nodeB = st.selectbox('Destination', st.session_state.node_df['id'])
            with col3:
                pipe_id = st.text_input('Pipe ID', value='PI' + str(len(st.session_state.pipe_df)))
            with col4:
                color = st.color_picker('Colour', value='#5E29FF')
                color = hex_to_rgb(color)
            
            
            
            
            with st.expander('Pipe features'):

                #display informations about the pipe
                col1, col2 = st.columns([3,1])
                with col1:
                    display_elevation()
                with col2:
                    st.metric("Length", "1000m", delta='+65m')
                    st.metric("Max velocity", "30m/s")
                    st.metric("Estimatated Cost", "$600")

            data3 = [[pipe_id,'NO1', 'NO2', '1000m',  '+65m']]
            data4 = pd.DataFrame(data3, columns=['ID','source','destination','length','elevation'])
            
            #check if nodeA and nodeB are different
            if nodeA != nodeB:
                if st.form_submit_button('Add pipe'):
                    #latA = st.session_state.node_df[st.session_state.node_df['id'] == nodeA]['position'].values[0][1]
                    #lonA = st.session_state.node_df[st.session_state.node_df['id'] == nodeA]['position'].values[0][0]
                    #latB = st.session_state.node_df[st.session_state.node_df['id'] == nodeB]['position'].values[0][1]
                    #lonB = st.session_state.node_df[st.session_state.node_df['id'] == nodeB]['position'].values[0][0]
#
                    #source = ox.get_nearest_node(G, (lonA, latA))
                    #destination = ox.get_nearest_node(G, (lonB, latB))
                    #path = nx.shortest_path(G, source, destination, weight='length')
                    

                    #update df id color path
                    st.session_state.pipe_df = st.session_state.pipe_df.append({'id': pipe_id, 'color': color, 'path': path_coords}, ignore_index=True)
                    st.session_state.path_layer = pdk.Layer(
                        "PathLayer",
                        data=st.session_state.pipe_df,
                        pickable=True,
                        #make cursor pointy
                        auto_highlight=True,
                        get_path='path',
                        get_color='color',
                        get_width=200,
                    )
                    #st.session_state.total_cost += PIPE_COST
                    st.experimental_rerun()
            else:
                if st.form_submit_button('Add pipe'):
                    st.error('Source and destination are the same')




    with tab3:
        with st.form(key='delete_node'):
            node_id = st.selectbox('Node ID', st.session_state.node_df['id'])
            
        #wait for user to press enter
            if st.form_submit_button('Delete node'):
                #TODO delete pipes contected to node
                st.session_state.node_df = st.session_state.node_df[st.session_state.node_df['id'] != node_id]
                st.session_state.total_cost -= NODE_COST
                st.session_state.scatter_layer = pdk.Layer(
                    "ScatterplotLayer",
                    data=st.session_state.node_df,
                    pickable=True,
                    #make cursor pointy
                    auto_highlight=True,
                    get_position='position',
                    get_color='color',
                    get_radius=200,
                )
                st.experimental_rerun()
        
    with tab4:
        pipe_id = st.selectbox('Pipe ID', ['PI1','PI2'], key='tab41')

        #wait for user to press enter
        if st.button('Delete pipe', key='tab4'):
            st.success(f'Pipe: {pipe_id} deleted')

    with tab5:
        uploaded_file = st.file_uploader("Choose a network config file")
        if uploaded_file is not None:
            st.session_state.node_df = pd.read_csv(uploaded_file)
            st.session_state.node_df['color'] = st.session_state.node_df['color'].apply(lambda x: ast.literal_eval(x))
            st.session_state.node_id_count = len(st.session_state.node_df)
            st.session_state.scatter_layer = pdk.Layer(
                "ScatterplotLayer",
                data=st.session_state.node_df,
                pickable=True,
                #make cursor pointy
                auto_highlight=True,
                get_position='position',
                get_color='color',
                get_radius=200,
            )
            st.experimental_rerun()

    with st.expander('Network features'):
        
        col1, col2, col3 = st.columns(3)
        with col1:
            
            st.metric('Number of nodes: ', len(st.session_state.node_df))
        with col2:
            st.metric("Number of pipes", 0)
        with col3:
            st.metric('Total cost: ', '$' + str(st.session_state.total_cost))
        
        st.download_button('Download network config', st.session_state.node_df.to_csv(), 'network_config.csv', 'text/csv')

    




elif page == "Austin":
    #st.title('Austin Network')
    view_state_austin = pdk.ViewState(
        latitude=30.2672,
        longitude=-97.7431,
        zoom=10
    )

    r = pdk.Deck(layers=[], initial_view_state=view_state_austin, tooltip={})
    
    st.pydeck_chart(r)
    

