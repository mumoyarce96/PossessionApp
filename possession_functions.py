# -*- coding: utf-8 -*-
"""
Created on Sun Jun 19 14:14:14 2022

@author: Jay Rowell
"""

from statsbombpy import sb
import pandas as pd
import matplotlib.pyplot as plt

def pie(team_list, possession, title):
    colors = ['palevioletred', '#39ff14']
    hometeam, awayteam = team_list
    fig = plt.figure()
    colors = ['palevioletred', '#39ff14']
    centre_circle = plt.Circle((0, 0), 0.70, fc='#0e1117')
    fig = plt.figure()
    patches, texts, autotexts = plt.pie(possession, colors=colors, labels=team_list,
                                autopct='%1.0f%%', pctdistance=0.85)
    texts[0].set_color('w')
    texts[1].set_color('w')
    fig.set_facecolor('#0e1117')
    fig.gca().add_artist(centre_circle)
    plt.title(title, color = 'w')
    return fig

def possession(data):
    columns = ('home', 'away', 'first_half_home_possession', 'first_half_away_possession',
               'second_half_home_possession', 'second_half_away_possession')
    df = []
    hometeam, awayteam = data.team.unique()
    firsthalfpasses = len(data[(data.period == 1) & (data.type == 'Pass')])
    secondhalfpasses = len(data[(data.period == 2) & (data.type == 'Pass')])
    homeposfirst = round(len(data[(data.period == 1) & (data.type == 'Pass') & (data.team == hometeam)])/firsthalfpasses*100,2)
    awayposfirst = round(len(data[(data.period == 1) & (data.type == 'Pass') & (data.team == awayteam)])/firsthalfpasses*100,2)
    homepossecond = round(len(data[(data.period == 2) & (data.type == 'Pass') & (data.team == hometeam)])/secondhalfpasses*100,2)
    awaypossecond = round(len(data[(data.period == 2) & (data.type == 'Pass') & (data.team == awayteam)])/secondhalfpasses*100,2)
    values = [hometeam,awayteam,homeposfirst,awayposfirst,homepossecond,awaypossecond]
    zipped = zip(columns, values)
    a_dictionary = dict(zipped)
    df.append(a_dictionary)
    df = pd.DataFrame(df, columns=['home', 'away', 'first_half_home_possession',
                  'first_half_away_possession', 'second_half_home_possession', 'second_half_away_possession'])
    teaml = [hometeam, awayteam]
    possession = [homeposfirst, awayposfirst]
    title = f'{hometeam} vs {awayteam}: First half possession'
    fig1 = pie(teaml, possession, title)
    teaml = [hometeam, awayteam]
    possession = [homepossecond, awaypossecond]
    title = f'{hometeam} vs {awayteam}: Second half possession'
    fig2 = pie(teaml, possession, title)
    return (fig1, fig2)

def time_filtered_possession(data, startmin,endmin):
    columns = ('home', 'away', 'home_possession', 'away_possession')
    df = []
    data = data[(data.minute >= startmin)&(data.minute <= endmin)]
    hometeam,awayteam = data.team.unique()
    totalpasses = len(data[(data.type=='Pass')])
    homepossession = round(len(data[(data.type == 'Pass') & (data.team == hometeam)])/totalpasses*100, 2)
    awaypossession = round(len(data[(data.type == 'Pass') & (data.team == awayteam)])/totalpasses*100, 2)
    values = [hometeam, awayteam,homepossession,
              awaypossession]
    zipped = zip(columns, values)
    a_dictionary = dict(zipped)
    df.append(a_dictionary)
    df = pd.DataFrame(df, columns=['home', 'away', 'home_possession','away_possession'])
    teaml = [hometeam,awayteam]
    possession = [homepossession,awaypossession]
    title = f'{hometeam} vs {awayteam}: Possession between minutes {startmin} and {endmin}'
    fig = pie(teaml, possession, title)
    return(fig)

