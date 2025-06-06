import streamlit as st
import plotly.express as plty
from htbuilder import HtmlElement, div, ul, li, br, hr, a, p, img, styles, classes, fonts
from htbuilder.units import percent, px
from htbuilder.funcs import rgba, rgb
from footer import footer
import yaml
from yaml import SafeLoader
import streamlit_authenticator as stauth
import pandas as pd
import os
import sys

#Import config :
st.set_page_config(layout="wide")

# with open('config.yaml') as file:
#     config = yaml.load(file, Loader=SafeLoader)
if 'authentication_status' not in st.session_state:
    st.session_state['authentication_status'] = None

## Welcome message

if st.session_state['authentication_status'] is None or st.session_state['authentication_status'] is False:
    st.title("Welcome to the League of Legends Dashboard")
else : 
    st.title(f"Welcome to the League of Legends Dashboard : *{st.session_state['name']}*")


## Login form yaml locally
# authenticator = stauth.Authenticate(config['credentials'],
#                                     config['cookie']['name'],
#                                     config['cookie']['key'],
#                                     config['cookie']['expiry_days']
#                                     )

## Login form with st secrets
authenticator = stauth.Authenticate(st.secrets['credentials'].to_dict(),
                                    st.secrets['cookie']['name'],
                                    st.secrets['cookie']['key'],
                                    st.secrets['cookie']['expiry_days']
                                    )

try:
    authenticator.login()
except Exception as e:
    st.error(e)

if st.session_state['authentication_status'] is False:
    st.error('Username/password is incorrect')
elif st.session_state['authentication_status'] is None:
    st.warning('Please enter your username and password')
elif st.session_state['authentication_status']:
    authenticator.logout(location='sidebar')

    #Import scrim data
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
    import json_scrim


    connect = json_scrim.connect_database('lol_match_database', host=st.secrets["MONGO_DB"]["RO_connection_string"])
    scrim_matches = json_scrim.get_collection(connect, "scrim_matches")
    data_scrim_matches = json_scrim.read_and_create_dataframe(scrim_matches)

    team_dico = st.secrets["TEAM_SCRIM_ID"]
    team_games = json_scrim.filter_data_on_team(data_scrim_matches, team_dict=team_dico)

    # Winrate by side group by week
    st.header("Winrate by side through time")
    winrate_by_side_time = json_scrim.get_winrate_by_side_every_two_weeks(team_games, True)
    st.plotly_chart(winrate_by_side_time,use_container_width=True)

    # Winrate by side bar
    st.header("Winrate by side")

    winrate_by_side = json_scrim.get_winrate_by_side(team_games, True)
    st.plotly_chart(winrate_by_side, use_container_width=True)



footer()



