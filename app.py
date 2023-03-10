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

import math



















CHARGING_COST = 500



NODE_COST = 1000
NODE_RADIUS = 10
NODE_COLOR = '#00FFAA'
NODE_ID_PREFIX = 'NO-'




PIPE_COST = 10 #$/m
PIPE_WIDTH = 10
PIPE_COLOR = '#FF0000'
PIPE_ID_PREFIX = 'PI-'




#data1 = [['Alice', [-73.597650,45.522920], [94, 41, 255],'None', 1000, 100],['Ethan',[-73.615480,45.522560], [94, 41, 255],'None', 1000, 100]]
data1 = [['1', [-84.220701,33.963581], [94, 41, 255],'None', 1000, 10],['2',[-84.219794,33.962877], [94, 41, 255],'None', 1000, 10],['3',[-84.219989,33.962696], [94, 41, 255],'None', 1000, 10],
         ['4',[-84.218144,33.964368], [94, 41, 255],'None', 1000, 10],['5',[-84.218074,33.965858], [94, 41, 255],'None', 1000, 10],['6',[-84.218148,33.966345], [94, 41, 255],'None', 1000, 10],
         ['7',[-84.217471,33.968101], [94, 41, 255],'None', 1000, 10],['8',[-84.219090,33.969256], [94, 41, 255],'None', 1000, 10],['9',[-84.218654,33.969861], [94, 41, 255],'None', 1000, 10]
]



if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if 'username' not in st.session_state:
    st.session_state.username = 'iAmEthanMai'

if 'token' not in st.session_state:
    st.session_state.token = ''

if 'node_df' not in st.session_state:
    st.session_state.node_df = pd.DataFrame(data1, columns=['id','position','color','info', 'cost', 'radius'])

if 'pipe_df' not in st.session_state:
    st.session_state.pipe_df = pd.DataFrame([], columns=['id', 'color', 'path', 'info', 'bidirectional'])


if 'total_length' not in st.session_state:
    st.session_state.total_length = 0

if 'node_id_count' not in st.session_state:
    st.session_state.node_id_count = 0

if 'scatter_layer' not in st.session_state:
    st.session_state.scatter_layer = pdk.Layer(
        "ScatterplotLayer",
        data=st.session_state.node_df,
        pickable=True,
        auto_highlight=True,
        get_position='position',
        get_color='color',
        get_radius='radius',
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



#settings

if 'junction_cost' not in st.session_state:
    st.session_state.junction_cost = NODE_COST

if 'junction_radius' not in st.session_state:
    st.session_state.junction_radius = NODE_RADIUS

if 'junction_id_prefix' not in st.session_state:
    st.session_state.junction_id_prefix = 'JU-'

if 'junction_color' not in st.session_state:
    st.session_state.junction_color = NODE_COLOR



if 'home_portal_cost' not in st.session_state:
    st.session_state.home_portal_cost = NODE_COST

if 'home_portal_radius' not in st.session_state:
    st.session_state.home_portal_radius = NODE_RADIUS

if 'home_portal_id_prefix' not in st.session_state:
    st.session_state.home_portal_id_prefix = 'HP-'

if 'home_portal_color' not in st.session_state:
    st.session_state.home_portal_color = NODE_COLOR



if 'community_portal_cost' not in st.session_state:
    st.session_state.community_portal_cost = NODE_COST

if 'community_portal_radius' not in st.session_state:
    st.session_state.community_portal_radius = NODE_RADIUS

if 'community_portal_id_prefix' not in st.session_state:
    st.session_state.community_portal_id_prefix = 'CP-'

if 'community_portal_color' not in st.session_state:
    st.session_state.community_portal_color = NODE_COLOR





if 'node_type' not in st.session_state:
                st.session_state.node_type = 'Home Portal'

if 'node_color' not in st.session_state:
    st.session_state.node_color = NODE_COLOR

if 'node_radius' not in st.session_state:
    st.session_state.node_radius = NODE_RADIUS

if 'node_cost' not in st.session_state:
    st.session_state.node_cost = NODE_COST

if 'node_id_prefix' not in st.session_state:
    st.session_state.node_id_prefix = st.session_state.home_portal_id_prefix
































#set page config
st.set_page_config(

    page_title="Pipedream Network Editor",
    #page_icon="app/assets/icon.svg",
    #layout="wide",
    initial_sidebar_state="expanded",
)


#make tab menu
st.sidebar.title('Pipedream Networks')
page = st.sidebar.radio("", ["Manual", "Automatic", "Settings", "Account"])







@st.cache(allow_output_mutation=True)
def load_graph():
    #return ox.load_graphml('simplified.graphml') 
    return ox.load_graphml('PeachTreeCorner.graphml') 
    


def display_elevation():
    st.write('Elevation profile')
    #array that looks like a mountain
    elevations = [10,10,10.5,10.5,10.5,10.5,10.5,11,11,11,11,11.5,11.5,11.5,11.5,11.5,11,11,11,11,11,11.5,11.5,11,11,11,11,11,11.5,11.5,11,11,11,11,11,10.5,10,9.5,9,9,9,9,9,9,9,9,9,9.5,9.5,9.5,9.5,9.5,9.5,9.5,9.5]


    st.area_chart(elevations)



def hex_to_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))




def render_map():
    #view_state = pdk.ViewState(
    #    latitude=45.5019,
    #    longitude=-73.5674,
    #    zoom=10
    #)

    view_state = pdk.ViewState(
        latitude=33.962877,
        longitude=-84.219794,
        zoom=15
    )

    #tooltip id and length if you hover over a pipe
    tooltip = {"html": "<b>ID:</b> {id} <br/> <b>info:</b> {info}", "style": {"color": "white"}} 
    r = pdk.Deck(layers=[st.session_state.path_layer, st.session_state.scatter_layer], initial_view_state=view_state, tooltip=tooltip)

    st.pydeck_chart(r)




############## Nodes functions ##############





def add_node(lat, lon, charging=False, node_id=None, intermediate=False):
    type_ = st.session_state.node_type
    if intermediate:
        node_id = f'JU-{st.session_state.node_id_count}'
        type_ = 'Junction'

        #check if node is already in graph by checking lat and lon
        #for node in st.session_state.node_df.iterrows():
        #    if node['x'] == lon and node['y'] == lat:
        #        return




    if type_ == 'Junction':
        node_cost = st.session_state.junction_cost
        node_color = st.session_state.junction_color
        node_radius = st.session_state.junction_radius

    elif type_ == 'Home Portal':
        node_cost = st.session_state.home_portal_cost
        node_color = st.session_state.home_portal_color
        node_radius = st.session_state.home_portal_radius

    elif type_ == 'Community Portal':
        node_cost = st.session_state.community_portal_cost
        node_color = st.session_state.community_portal_color
        node_radius = st.session_state.community_portal_radius

    node_color = hex_to_rgb(node_color)

    st.session_state.node_id_count += 1

    if charging:
        node_cost += CHARGING_COST

    st.session_state.total_cost += node_cost
    st.session_state.node_df = st.session_state.node_df.append({'id': node_id, 'position': [lon, lat], 'color': node_color, 'info': 'None', 'cost': node_cost, 'radius': node_radius}, ignore_index=True)
    
    st.session_state.scatter_layer = pdk.Layer(
        "ScatterplotLayer",
        data=st.session_state.node_df,
        pickable=True,
        auto_highlight=True,
        get_position='position',
        get_color='color',
        get_radius='radius',
    )
    if not intermediate:
        st.experimental_rerun()



def delete_node(node_id):
    node_cost = st.session_state.node_df[st.session_state.node_df['id'] == node_id]['cost'].values[0]
    node_df = st.session_state.node_df[st.session_state.node_df['id'] != node_id]
    st.session_state.node_df = node_df
    st.session_state.total_cost -= node_cost
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






############## Pipe functions ##############






def get_shortest_path(source_x, source_y, destination_x, destination_y):
    source = ox.get_nearest_node(G, (source_y, source_x))
    destination = ox.get_nearest_node(G, (destination_y, destination_x))

    if source == destination:
        distance = math.sqrt((source_x - destination_x)**2 + (source_y - destination_y)**2)
        return [[source_x, source_y], [destination_x, destination_y]], distance

    path = nx.shortest_path(G, source, destination, weight='length')
    length = nx.shortest_path_length(G, source, destination, weight='length')
    return path, length


def get_pipe_stats(source_id, destination_id):
    source_y = st.session_state.node_df[st.session_state.node_df['id'] == source_id]['position'].values[0][1]
    source_x = st.session_state.node_df[st.session_state.node_df['id'] == source_id]['position'].values[0][0]
    destination_y = st.session_state.node_df[st.session_state.node_df['id'] == destination_id]['position'].values[0][1]
    destination_x = st.session_state.node_df[st.session_state.node_df['id'] == destination_id]['position'].values[0][0]
    
    path, length = get_shortest_path(source_x, source_y, destination_x, destination_y)
    elevation_profile = []
    #for coord in path:
    #    elevation_profile.append(G.nodes[coord]['elevation'])

    elevation_gain = round(max(elevation_profile) - min(elevation_profile),2)


    if len(path) > 3:
        number_of_intermediate_junctions = len(path) - 2
    elif len(path) == 3:
        number_of_intermediate_junctions = 1
    else:
        number_of_intermediate_junctions = 0
    
    intermediate_junctions_cost = number_of_intermediate_junctions * st.session_state.junction_cost
    pipe_cost = length * PIPE_COST

    total_cost = pipe_cost + intermediate_junctions_cost








def add_pipe(source_id, destination_id, pipe_id, color, bidirectional):
    source_y = st.session_state.node_df[st.session_state.node_df['id'] == source_id]['position'].values[0][1]
    source_x = st.session_state.node_df[st.session_state.node_df['id'] == source_id]['position'].values[0][0]
    destination_y = st.session_state.node_df[st.session_state.node_df['id'] == destination_id]['position'].values[0][1]
    destination_x = st.session_state.node_df[st.session_state.node_df['id'] == destination_id]['position'].values[0][0]
    
    path, length = get_shortest_path(source_x, source_y, destination_x, destination_y)

    st.session_state.total_cost += length * PIPE_COST
    st.session_state.total_length += length
    #st.write(path)
    
    
    
#    path_coords = []
#    
#    
#
#    for i, point in enumerate(path):
#
#        x, y = G.nodes[point]['x'], G.nodes[point]['y']
#        path_coords.append([x, y])
#        if i != 0 or i != len(path)-1:
#            add_node(y, x, intermediate=True)
#        
#    
#
#    paths = list(zip(path_coords, path_coords[1:]))
#
#    for i, section in enumerate(paths):
#        section_source, section_destination = section
#        _, section_length = get_shortest_path(section_source[0], section_source[1], section_destination[0], section_destination[1])
#        st.session_state.pipe_df = st.session_state.pipe_df.append({'id': pipe_id + '_' + str(i), 'color': color, 'path': section, 'info': "length: " + str(round(section_length,2))+'m', 'bidirectional': bidirectional}, ignore_index=True)
#        st.session_state.path_layer = pdk.Layer(
#            "PathLayer",
#            data=st.session_state.pipe_df,
#            pickable=True,
#            #make cursor pointy
#            auto_highlight=True,
#            get_path='path',
#            get_color='color',
#            get_width=50,
#        )

    path_coords = []
    path_coords.append([source_x, source_y])
    for point in path:
        x, y = G.nodes[point]['x'], G.nodes[point]['y']
        path_coords.append([x, y])
    
    
    path_coords.append([destination_x, destination_y])

    st.session_state.pipe_df = st.session_state.pipe_df.append({'id': pipe_id, 'color': color, 'path': path_coords, 'info': "length: " + str(round(length,2))+'m', 'bidirectional': bidirectional}, ignore_index=True)
    st.session_state.path_layer = pdk.Layer(
        "PathLayer",
        data=st.session_state.pipe_df,
        pickable=True,
        #make cursor pointy
        auto_highlight=True,
        get_path='path',
        get_color='color',
        get_width=10,
    )













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
    if not st.session_state.logged_in:
        st.write("Please log in")
        st.stop()

    G = load_graph()
    
    #if 'G' not in st.session_state:
    #    st.session_state.G = load_graph()

    #st.write(len(G))
    render_map()
    #st.write(st.session_state.node_df)
    st.write(st.session_state.pipe_df)
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Add node", "Add pipe", "Delete node", "Delete pipe", "Load config"])
    data = np.random.randn(10, 1)
































    with tab1:


        with st.form(key='node_form'):

            col1, col2 = st.columns(2)
            with col1:
                
                node_type = st.selectbox('Node type', ['Home Portal', 'Community Portal', 'Junction']) 
            button = st.form_submit_button(label='Update node type')
            if button:
                st.session_state.node_type = node_type


        with st.form(key='tab1'):
            
            if st.session_state.node_type == 'Junction':
                st.session_state.node_id_prefix = st.session_state.junction_id_prefix
            elif st.session_state.node_type == 'Home Portal':   
                st.session_state.node_id_prefix = st.session_state.home_portal_id_prefix
            elif st.session_state.node_type == 'Community Portal':
                st.session_state.node_id_prefix = st.session_state.community_portal_id_prefix
            

            col1, col2, col3 = st.columns(3)
            with col1:
                lat = st.number_input('Latitude', min_value=0.0, max_value=90.0, value=45.532560)
            with col2:
                lon = st.number_input('Longitude', min_value=-180.0, max_value=180.0, value=-73.615480)
            with col3:
                node_id = st.text_input('Node ID', value=st.session_state.node_id_prefix + str(st.session_state.node_id_count))
            
            charging_station = st.checkbox('Charging station')

            if st.form_submit_button('Add node'):
                #check if node is already at this location
                if st.session_state.node_df['position'].isin([[lon, lat]]).any():
                    st.error('A node already exists at this location')
                else:
                    add_node(lat, lon, charging = charging_station, node_id = node_id)
































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
                color = st.color_picker('Color', value='#5E29FF')
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
                    add_pipe(nodeA, nodeB, pipe_id, color, bidirectional) 
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
                delete_node(node_id)
                
        
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

        
        st.markdown('**Junction settings**')
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            junction_cost = st.number_input('Cost', value=st.session_state.junction_cost, step=1000, min_value=0, max_value=1000000, key='junction_cost_input')
        with col2:
            junction_id_prefix = st.text_input('ID prefix', value=st.session_state.junction_id_prefix, key='junction_id_prefix_input')
        with col3:
            junction_radius = st.number_input('Radius', value=st.session_state.junction_radius, step=10, min_value=0, max_value=1000, key='junction_radius_input')
        with col4:
            junction_color = st.color_picker('Color', value=st.session_state.junction_color, key='junction_color_input')


        st.markdown('**Home portal settings**')
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            home_portal_cost = st.number_input('Cost', value=NODE_COST, step=1000, min_value=0, max_value=1000000, key='home_portal_cost_input')
        with col2:
            home_portal_id_prefix = st.text_input('ID prefix', value=st.session_state.home_portal_id_prefix, key='home_portal_id_prefix_input')
        with col3:
            home_portal_radius = st.number_input('Radius', value=st.session_state.home_portal_radius, step=10, min_value=0, max_value=1000, key='home_portal_radius_input')
        with col4:
            home_portal_color = st.color_picker('Color', value='#00FFAA', key='home_portal_color_input')


        st.markdown('**Community portal settings**')
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            community_portal_cost = st.number_input('Cost', value=NODE_COST, step=1000, min_value=0, max_value=1000000, key='community_portal_cost_input')
        with col2:
            community_portal_id_prefix = st.text_input('ID prefix', value=st.session_state.community_portal_id_prefix, key='community_portal_id_prefix_input')
        with col3:
            community_portal_radius = st.number_input('Radius', value=st.session_state.community_portal_radius, step=10, min_value=0, max_value=1000, key='community_portal_radius_input')
        with col4:
            community_portal_color = st.color_picker('Color', value='#00FFAA', key='community_portal_color_input')

        
        if st.form_submit_button('Save'):
            st.session_state.junction_cost = junction_cost
            st.session_state.junction_id_prefix = junction_id_prefix
            st.session_state.junction_radius = junction_radius
            st.session_state.junction_color = junction_color


            st.session_state.home_portal_cost = home_portal_cost
            st.session_state.home_portal_id_prefix = home_portal_id_prefix
            st.session_state.home_portal_radius = home_portal_radius
            st.session_state.home_portal_color = home_portal_color

            st.session_state.community_portal_cost = community_portal_cost
            st.session_state.community_portal_id_prefix = community_portal_id_prefix
            st.session_state.community_portal_radius = community_portal_radius
            st.session_state.community_portal_color = community_portal_color

            st.experimental_rerun()
    
    with st.form(key='pipe_settings'):
        st.subheader('Pipe settings')
        #pipe settings section
        #slider
        #age = st.slider('Pipe width (px)', 50, 200, 75)
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            pipe_width = st.number_input('Width', value=50, step=10, min_value=0, max_value=200, key='pipe_width')
        st.markdown('**Unidirectional pipe settings**')
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            pipe_cost = st.number_input('Cost ($/m)', value=PIPE_COST, step=5, min_value=0, max_value=1000000, key='pipe_cost')

        with col2:
            pipe_id_prefix = st.text_input('ID prefix', value='PI-', key='pipe_id_prefix')
        with col4:
            pipe_color = st.color_picker('Color', value='#00FFAA', key='pipe_color')

        

        st.markdown('**Bidirectional pipe settings**')

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            bipipe_cost = st.number_input('Cost ($/m)', value=PIPE_COST, step=5, min_value=0, max_value=1000000, key='bipipe_cost')
        with col2:
            bipipe_id_prefix = st.text_input('ID prefix', value='PI-', key='bipipe_id_prefix')
        with col4:
            bipipe_color = st.color_picker('Color', value='#00FFAA', key='bipipe_color')

        if st.form_submit_button('Save'):
            st.success('Pipe settings saved')

elif page == "Account":
    with st.form(key='login_form'):
        st.subheader('Login')
        col1, col2 = st.columns(2)
        with col1:
            username = st.text_input('Github username', value=st.session_state.username, key='username_input')
        with col2:
            token = st.text_input('Access token', key='token_input', type='password')

        if st.form_submit_button('Login'):
            st.session_state.username = username
            st.session_state.token = token
            st.success('Logged in as {}'.format(username))
            time.sleep(1)
            if not st.session_state.logged_in:
                st.session_state.logged_in = True
            st.experimental_rerun()
