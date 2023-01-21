import datetime

import discord
import pandas
import pandas as pd
import httpx
import pickle


def get_props():

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"
    }

    r = httpx.get('https://api.prizepicks.com/projections', headers = headers)


    return r.json()


def parse_json_into_df():


    data = get_props()
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_colwidth', None)
    # dataframe with data
    data_frame = pd.json_normalize(data['data'])
    data_frame = data_frame[['id', 'attributes.board_time', 'attributes.description', 'attributes.line_score',
                                        'attributes.projection_type', 'attributes.stat_type', 'attributes.updated_at',
                                        'relationships.league.data.id', 'relationships.new_player.data.id']]

    # player data
    player_frame = pd.json_normalize(data['included'])
    player_frame = player_frame[['id', 'attributes.image_url', 'attributes.league', 'attributes.league_id', 'attributes.name',
                                 'attributes.position', 'attributes.team', 'attributes.team_name']].dropna(thresh=3)

    #print(player_frame)
    final = pandas.merge(data_frame, player_frame, left_on='relationships.new_player.data.id', right_on='id', how='left' )
    #sanitise
    final.drop('id_y', inplace= True, axis=1)
    final.rename(columns= {'id_x' : 'id'}, inplace = True)
    final['id'] = final['id'].astype(int)

    update_league_list(final)


    try:
        old_df = pandas.read_csv('data.csv')
    except:
        final.to_csv("data.csv", index=False)
        return final

    new_df = old_df.merge(final, how="outer", on="id", indicator=True)
    final.to_csv("data.csv", index= False)
    return new_df


def get_new(data : pandas.DataFrame):

    a = data[data['_merge'] == 'right_only']
    a = a.dropna(axis=1, thresh=1)
    return a

def get_update(data : pandas.DataFrame):
    a = data[data['attributes.updated_at_x'] != data['attributes.updated_at_y']]
    a = a[a['attributes.updated_at_x'].notna()]
    a = a[a['attributes.updated_at_y'].notna()]
    return a

def update_league_list(data :pandas.DataFrame):

    leagues = data['attributes.league'].drop_duplicates().dropna()
    llist  = leagues.values.tolist()
    with open('leaguelist.txt', 'wb') as f:
        pickle.dump(llist, f)


