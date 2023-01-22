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
page = st.sidebar.radio("", ["Manual", "Automatic", "Settings"])







NODE_COST = 1000
PIPE_COST = 10 #$/m



@st.cache(allow_output_mutation=True)
def load_graph():
    return ox.load_graphml('simplified.graphml') 
    


def display_elevation():
    st.write('Elevation profile')
    #array that looks like a mountain
    elevations = [10,10,10.5,10.5,10.5,10.5,10.5,11,11,11,11,11.5,11.5,11.5,11.5,11.5,11,11,11,11,11,11.5,11.5,11,11,11,11,11,11.5,11.5,11,11,11,11,11,10.5,10,9.5,9,9,9,9,9,9,9,9,9,9.5,9.5,9.5,9.5,9.5,9.5,9.5,9.5]


    st.area_chart(elevations)







def hex_to_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))



data1 = [['Alice', [-73.597650,45.522920], [94, 41, 255],'None'],['Ethan',[-73.615480,45.522560], [94, 41, 255],'None']]









if 'pipe_df' not in st.session_state:
    st.session_state.pipe_df = pd.DataFrame([], columns=['id', 'color', 'path', 'length', 'bidirectional'])
    #st.session_state.pipe_df['color'] = st.session_state.pipe_df['color'].apply(hex_to_rgb)


if 'total_length' not in st.session_state:
    st.session_state.total_length = 0

if 'node_id_count' not in st.session_state:
    st.session_state.node_id_count = 0
if 'node_df' not in st.session_state:
    st.session_state.node_df = pd.DataFrame(data1, columns=['id','position','color','length'])

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


    #tooltip id and length if you hover over a pipe
    tooltip = {"html": "<b>ID:</b> {id} <br/> <b>Length:</b> {length}", "style": {"color": "white"}} 
    
    r = pdk.Deck(layers=[st.session_state.scatter_layer, st.session_state.path_layer], initial_view_state=view_state, tooltip=tooltip)


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






if page == "Manual":

    G = load_graph()
    
    #if 'G' not in st.session_state:
    #    st.session_state.G = load_graph()

    #st.write(len(G))
    render_map()
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Add node", "Add pipe", "Delete node", "Delete pipe", "Load config"])
    data = np.random.randn(10, 1)

    with tab1:

        with st.form(key='tab1'):
            col1, col2, col3 = st.columns(3)
            with col1:
                lat = st.number_input('Latitude', min_value=0.0, max_value=90.0, value=45.532560)
            with col2:
                lon = st.number_input('Longitude', min_value=-180.0, max_value=180.0, value=-73.615480)
            with col3:
                node_id = st.text_input('Node ID', value='NO' + str(st.session_state.node_id_count))
            
            col4, col5 = st.columns(2)
            with col4:
                node_type = st.selectbox('Node type', ['Home Portal', 'Comunity Portal', 'Junction']) 
            with col5: 
                color = st.color_picker('Colour', value='#5E29FF')
                color = hex_to_rgb(color)

            if st.form_submit_button('Add node'):
                
                #check if node is already at this location
                if st.session_state.node_df['position'].isin([[lon, lat]]).any():
                    st.error('A node already exists at this location')
                else:

                    st.session_state.node_id_count += 1
                    st.session_state.total_cost += NODE_COST
                    st.session_state.node_df = st.session_state.node_df.append({'id': node_id, 'position': [lon, lat], 'color': color, 'length': 'None'}, ignore_index=True)
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
            
            
            bidirectional = st.checkbox('Bidirectional')
            
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
                    lonA = st.session_state.node_df[st.session_state.node_df['id'] == nodeA]['position'].values[0][1]
                    latA = st.session_state.node_df[st.session_state.node_df['id'] == nodeA]['position'].values[0][0]
                    lonB = st.session_state.node_df[st.session_state.node_df['id'] == nodeB]['position'].values[0][1]
                    latB = st.session_state.node_df[st.session_state.node_df['id'] == nodeB]['position'].values[0][0]


                    source = ox.get_nearest_node(G, (lonA, latA))
                    
                    destination = ox.get_nearest_node(G, (lonB, latB))
                    
                    
                    path = nx.shortest_path(G, source, destination, weight='length')
                    length = nx.shortest_path_length(G, source, destination, weight='length')
                    st.session_state.total_cost += length * PIPE_COST
                    st.session_state.total_length += length
                    #st.write(path)
                    path_coords = []
                    for point in path:
                        x, y = G.nodes[point]['x'], G.nodes[point]['y']
                        path_coords.append([x, y])
                    
                    #update df id color path
                    st.session_state.pipe_df = st.session_state.pipe_df.append({'id': pipe_id, 'color': color, 'path': path_coords, 'length': str(round(length,2))+'m', 'bidirectional': bidirectional}, ignore_index=True)
                    st.session_state.path_layer = pdk.Layer(
                        "PathLayer",
                        data=st.session_state.pipe_df,
                        pickable=True,
                        #make cursor pointy
                        auto_highlight=True,
                        get_path='path',
                        get_color='color',
                        get_width=50,
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
        pipe_id = st.selectbox('Pipe ID', st.session_state.pipe_df['id'], key='tab41')

        #wait for user to press enter
        if st.button('Delete pipe', key='tab4'):
            
            #TODO delete pipes contected to node
            st.session_state.pipe_df = st.session_state.pipe_df[st.session_state.pipe_df['id'] != pipe_id]
            st.session_state.total_cost -= PIPE_COST
            st.session_state.path_layer = pdk.Layer(
                "PathLayer",
                data=st.session_state.pipe_df,
                pickable=True,
                #make cursor pointy
                auto_highlight=True,
                get_path='path',
                get_color='color',
                get_width=50,
            )
            st.experimental_rerun()

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
            st.metric("Number of pipes", len(st.session_state.pipe_df))
        #with col3:
        #    st.metric("Total length", str(round(st.session_state.total_length,0))+'m')
        with col3:
            #cost with commas
            st.metric("Total cost", f"${st.session_state.total_cost:,.2f}")
        
        st.download_button('Download network config', st.session_state.node_df.to_csv(), 'network_config.csv', 'text/csv')





elif page == "Automatic":
    #st.title('Austin Network')
    view_state_austin = pdk.ViewState(
        latitude=30.2672,
        longitude=-97.7431,
        zoom=10
    )

    r = pdk.Deck(layers=[], initial_view_state=view_state_austin, tooltip={})
    
    st.pydeck_chart(r)


elif page == "Settings":
    with st.form(key='node_settings'):
        st.subheader('Node settings')
        #node settings section

        st.markdown('**Junction settings**')
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            junction_cost = st.number_input('Cost', value=NODE_COST, step=1000, min_value=0, max_value=1000000, key='junction_cost')
        with col2:
            junction_radius = st.number_input('Radius', value=200, step=10, min_value=0, max_value=1000, key='junction_radius')
        with col3:
            junction_id_prefix = st.text_input('ID prefix', value='JU', key='junction_id_prefix')
        with col4:
            junction_color = st.color_picker('Colour', value='#00FFAA', key='junction_color')


        st.markdown('**Home portal settings**')
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            home_portal_cost = st.number_input('Cost', value=NODE_COST, step=1000, min_value=0, max_value=1000000, key='home_portal_cost')
        with col2:
            home_portal_radius = st.number_input('Radius', value=200, step=10, min_value=0, max_value=1000, key='home_portal_radius')
        with col3:
            home_portal_id_prefix = st.text_input('ID prefix', value='HP', key='home_portal_id_prefix')
        with col4:
            home_portal_color = st.color_picker('Colour', value='#00FFAA', key='home_portal_color')


        st.markdown('**Community portal settings**')
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            community_portal_cost = st.number_input('Cost', value=NODE_COST, step=1000, min_value=0, max_value=1000000, key='community_portal_cost')
        with col2:
            community_portal_radius = st.number_input('Radius', value=200, step=10, min_value=0, max_value=1000, key='community_portal_radius')
        with col3:
            community_portal_id_prefix = st.text_input('ID prefix', value='CP', key='community_portal_id_prefix')
        with col4:
            community_portal_color = st.color_picker('Colour', value='#00FFAA', key='community_portal_color')

        
        if st.form_submit_button('Save'):
            st.write('Settings saved')
    
    with st.form(key='pipe_settings'):
        st.subheader('Pipe settings')
        #pipe settings section
        st.markdown('**Unidirectional pipe settings**')
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            pipe_cost = st.number_input('Cost ($/m)', value=PIPE_COST, step=1000, min_value=0, max_value=1000000, key='pipe_cost')
        with col2:
            pipe_width = st.number_input('Width', value=50, step=10, min_value=0, max_value=1000, key='pipe_width')
        with col3:
            pipe_id_prefix = st.text_input('ID prefix', value='PI', key='pipe_id_prefix')
        with col4:
            pipe_color = st.color_picker('Colour', value='#00FFAA', key='pipe_color')

        

        st.markdown('**Bidirectional pipe settings**')

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            bipipe_cost = st.number_input('Cost ($/m)', value=PIPE_COST, step=1000, min_value=0, max_value=1000000, key='bipipe_cost')
        with col2:
            bipipe_width = st.number_input('Width', value=50, step=10, min_value=0, max_value=1000, key='bipipe_width')
        with col3:
            bipipe_id_prefix = st.text_input('ID prefix', value='PI', key='bipipe_id_prefix')
        with col4:
            bipipe_color = st.color_picker('Colour', value='#00FFAA', key='bipipe_color')

        if st.form_submit_button('Save'):
            st.write('Settings saved')

    
        st.markdown('**Export settings**')
        st.button('Download settings', key='download_settings')

        st.markdown('**Import settings**')
        uploaded_file = st.file_uploader("Choose a file")
    

