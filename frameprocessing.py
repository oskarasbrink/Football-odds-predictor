from turtle import home
from keras.models import Sequential
from keras.layers import Dense
from keras.utils import np_utils
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder

def getHomeTeam(s):
    return s.replace(" ","").split("-")[0]


def getAwayTeam(s):
    str = s.replace(" ","").split("-")[1]
    length = len(str)
    return str[0:length-3]


def getResult(s):
    str = s.replace(" ","").split("-")[1]
    length = len(str)
    res = str[length-3:length]
    if res[0]>res[2]:
        return 1
    elif res[0] < res[2]:
        return 2
    else:
        return 0

def splitData(df):
    data_team_1 = df[0::2].copy(deep=True)
    data_team_2 = df[1::2].copy(deep=True)

    return data_team_1,data_team_2

def merge():
    pass


def dateSwitcher(s):
    temp = s.split("/")
    return temp[2] + "/" + temp[1] + "/" + temp[0]



def get_away_columns(df):
    columns = df.columns
    ncolumns = len(columns)

    opponentarray = ['away ']*ncolumns

    opponentcolumns = [y+x for x,y in zip(columns,opponentarray)]
    return opponentcolumns



def one_hot(df):
    #print(df['Team'])
    dfcopy = df.copy(deep=True)
    test_df = dfcopy.copy(deep=True)
    one_hot = pd.get_dummies(df["Team"])

    dfcopy["away Team"] = addOpponentString(dfcopy)
    one_hot2 = pd.get_dummies(dfcopy["away Team"])
    #test_df.drop(['opponent Team','Team'], axis=1, inplace=True)
    test_df = test_df.join(one_hot)
    test_df = test_df.join(one_hot2)
    return test_df



def addOpponentString(df):
    temp = ['away '] * len(df['away Team'])
    names = df['away Team']

    current_columns = [y+x for x,y in zip(names,temp)]
    return current_columns

def add_average_stats():
    pass

def avg_lookup(team, data):
    return data.loc[data["Team"] == team]

def teams_to_dataframe(teamList, data):
    result = pd.DataFrame()

    for team in teamList:
        result = pd.concat([result, avg_lookup(team, data)])

    return result
    
def matches_to_dataframe(df, data_avg):

    #home
    #away
    
    home_teams = df.loc[df["Team"] == df["Home"]]
    away_teams = df.loc[df["Team"] != df["Home"]]

    print(home_teams["Team"].unique())
    print(away_teams["Team"].unique())

    home_df = teams_to_dataframe(home_teams, data_avg)
    away_df = teams_to_dataframe(away_teams, data_avg)

    away_columns = away_df.columns
    temp = ["away "]*len(away_columns)
    new_columns = [y+x for x,y in zip(away_columns,temp)]
    away_df.columns=new_columns

    home_df.reset_index(inplace=True, drop=True)
    away_df.reset_index(inplace=True, drop=True)

    dfcopy = df.copy(deep=True)

    dfcopy.iloc[:, 2:106]= home_df.iloc[:, 0:104]
    dfcopy.iloc[:, 106:210] = away_df.iloc[:, 0:104]

    return dfcopy

def return_odds(matches_df, odds_df):
    pass
    
def transformTeam(s):
    transformdict = {
        "Hammarby":"Hammarby",
        "Kalmar":"Kalmar",
        "Sirius":"Sirius",
        "Degerfors":"Degerfors",
        "AIK":"AIK",
        "Helsingborg":"Helsingborg",
        "Halmstad":"Halmstad",
        "Elfsborg":"Elfsborg",
        'Värnamo':"Varnamo",
        "GIF Sundsvall":"Sundsvall",
        "Djurgården":"Djurgarden",
        "IFK Norrköping":"Norrkoping",
        "Malmö FF":"Malmo FF",
        "Örebro":"Orebro",
        "Mjällby":"Mjallby",
        "Falkenberg":"Falkenbergs",
        "IFK Göteborg":"Goteborg",
        "Östersunds FK":"Ostersunds",
        "Häcken":"Hacken",
        "Varberg":"Varbergs"
    }
    return transformdict[s]

def caluclate_error(df):
    error = df["Win %"] - df["AvgH"]


