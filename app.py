# -*- coding: utf-8 -*-
"""
Created on Wed Jun 22 12:24:11 2022

@author: Raimundo
"""
from statsbombpy import sb
import pandas as pd
import streamlit as st
import numpy as np
from possession_functions import *

username = st.secrets['user']
password = st.secrets['password']
creds = {'user': user, 'passwd': password}
matches = sb.matches(49, 106, creds=creds)
dash_matches = matches[(matches['home_team'] == 'Houston Dash') | (matches['away_team'] == 'Houston Dash')]
dash_matches = dash_matches.sort_values(by = 'match_date', ascending = False).reset_index(drop = True)
last_home_team = dash_matches.iloc[0]['home_team']
last_away_team = dash_matches.iloc[0]['away_team'] 

st.set_page_config(page_title='NWSL 2022 possession viewer')
st.header('NWSL 2022 possession viewer')

home_teams = list(matches['home_team'].unique())
away_teams = list(matches['away_team'].unique())
home_team = st.selectbox("Home team", home_teams, index = home_teams.index(last_home_team))
away_team = st.selectbox("Away team", away_teams, index = away_teams.index(last_away_team))

match = matches[(matches['home_team'] == home_team) & (matches['away_team'] == away_team)]
if len(match) == 0:
    st.write("That match have not been played yet")
else:
    match_id = match.iloc[0]['match_id']
    filter_by_min = st.checkbox("Filter by minutes", value=False)
    match_events = sb.events(match_id=match_id, creds=creds)
    if filter_by_min:
        st.write("Select starting and ending minutes")
        start = st.text_input('Start', '0')
        if start.isnumeric() == False:
            st.write('Start input must be a number')
        end = st.text_input('End', '45')
        if end.isnumeric() == False:
            st.write('End input must be a number')
        if start.isnumeric() and end.isnumeric(): 
            start = int(start)
            end = int(end)
            if start <= end:
                fig = time_filtered_possession(match_events, start,end)
                st.pyplot(fig)
            else:
                st.write("Start can't be lower than End!")
    else:
        fig1, fig2 = possession(match_events)
        st.pyplot(fig1)
        st.pyplot(fig2)