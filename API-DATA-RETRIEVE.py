import numpy as np
import requests
import pandas as pd

BASE_URL = "https://www.balldontlie.io/api/v1"
PER_PAGE = 100


def get_players():
    df_columns = ['id', 'first_name', 'last_name', 'position', 'team_id']
    df = pd.DataFrame(columns=df_columns)

    url = BASE_URL + "/players"
    next_page = 1
    while True:
        params = {'per_page': PER_PAGE, 'page': next_page}
        response = requests.get(url=url, params=params).json()
        data = response['data']
        for r in data:
            tmp_columns = ['id', 'first_name', 'last_name', 'position']
            values = list(map(r.get, tmp_columns))
            values.append(r['team']['id'])
            tmp_df = pd.DataFrame([values], columns=df_columns)
            df = pd.concat([df, tmp_df], axis=0, ignore_index=True)

        next_page = response['meta']['next_page']
        if next_page is None:
            break
        print(f"DONE - PAGE {next_page-1}")

    df.replace("", None, inplace=True)
    df.to_csv('data/players.csv', index=False)
    print("DONE")


def get_teams():
    df_columns = ['id', 'abbreviation', 'city', 'conference', 'full_name', 'name']

    df = pd.DataFrame(columns=df_columns)
    url = BASE_URL + "/teams"
    params = {'per_page': PER_PAGE}
    response = requests.get(url=url, params=params).json()['data']
    for r in response:
        data = list(map(r.get, df_columns))
        tmp_df = pd.DataFrame([data], columns=df_columns)
        df = pd.concat([df, tmp_df], axis=0, ignore_index=True)

    df.to_csv('data/teams.csv', index=False)
    print("DONE")


def get_games():
    df_columns = ['id', 'season', 'status',
                  'home_team_id', 'home_team_score',
                  'visitor_team_id', 'visitor_team_score',
                  ]

    df = pd.DataFrame(columns=df_columns)

    next_page = 1
    url = BASE_URL + "/games"

    while True:
        params = {'per_page': PER_PAGE, 'page': next_page}
        response = requests.get(url=url, params=params).json()
        data = response['data']
        for r in data:
            tmp_columns = ['id', 'season', 'status']
            values = list(map(r.get, tmp_columns))
            values.append(r['home_team']['id'])
            values.append(r['home_team_score'])
            values.append(r['visitor_team']['id'])
            values.append(r['visitor_team_score'])

            tmp_df = pd.DataFrame([values], columns=df_columns)
            df = pd.concat([df, tmp_df], axis=0, ignore_index=True)

        if next_page is None:
            break
        next_page = response['meta']['next_page']
        if next_page % 100 == 1:
            print(f"DONE - PAGE {next_page}")

    df.to_csv('data/games.csv', index=False)
    print("DONE")


def get_stats():
    df_columns = ['ast', 'blk', 'dreb', 'game_id', 'player_id', 'pts', 'reb', 'stl', 'team_id', 'turnover']
    df = pd.DataFrame(columns=df_columns)

    url = BASE_URL + '/stats'
    next_page = 1
    while True:
        params = {'page': next_page, 'per_page': PER_PAGE, 'seasons[]': [2022], 'postseason': False}
        response = requests.get(url=url, params=params).json()
        data = response['data']
        for r in data:
            tmp_columns = ['ast', 'blk', 'dreb']
            values = list(map(r.get, tmp_columns))
            values.append(r['game']['id'])
            values.append(r['player']['id'])
            values.append(r['pts'])
            values.append(r['reb'])
            values.append(r['stl'])
            values.append(r['team']['id'])
            values.append(r['turnover'])

            tmp_df = pd.DataFrame([values], columns=df_columns)
            df = pd.concat([df, tmp_df], axis=0, ignore_index=True)
        next_page = response['meta']['next_page']
        print(f"DONE - PAGE {next_page}")
        if next_page is None:
            break

    df.to_csv('data/stats.csv', index=False)
    print("DONE")


if __name__ == '__main__':
    pass
    # print("START COLLECTING DATA ...")
    get_players()
    # get_teams()
    # get_games()
    # get_stats()
    # print("DONE")
