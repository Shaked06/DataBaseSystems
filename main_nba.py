import requests
import pandas as pd

BASE_URL = "https://www.balldontlie.io/api/v1"

PER_PAGE = 100


def get_players():
    df_columns = ['id', 'first_name', 'last_name', 'position', 'team_id']
    df = pd.DataFrame(columns=df_columns)

    pages = range(1, 40)
    url = BASE_URL + "/players"

    for page in pages:
        params = {'per_page': PER_PAGE, 'page': page}
        response = requests.get(url=url, params=params).json()['data']
        for r in response:
            tmp_columns = ['id', 'first_name', 'last_name', 'position']
            data = list(map(r.get, tmp_columns))
            data.append(r['team']['id'])
            tmp_df = pd.DataFrame([data], columns=df_columns)
            df = pd.concat([df, tmp_df], axis=0, ignore_index=True)

        print(f"DONE - PAGE {page}")

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

    pages = range(1, 526)
    url = BASE_URL + "/games"

    for page in pages:
        params = {'per_page': PER_PAGE, 'page': page}
        response = requests.get(url=url, params=params).json()['data']
        for r in response:
            tmp_columns = ['id', 'season', 'status']
            data = list(map(r.get, tmp_columns))
            data.append(r['home_team']['id'])
            data.append(r['home_team_score'])
            data.append(r['visitor_team']['id'])
            data.append(r['visitor_team_score'])

            tmp_df = pd.DataFrame([data], columns=df_columns)
            df = pd.concat([df, tmp_df], axis=0, ignore_index=True)
        if page % 100 == 1:
            print(f"DONE - PAGE {page}")

    df.to_csv('data/games.csv', index=False)
    print("DONE")


def get_stats():
    df_columns = ['id', 'ast', 'blk', 'dreb', 'game_id',
                  'player_id', 'pts', 'reb', 'stl', 'team_id', 'turnover']
    df = pd.DataFrame(columns=df_columns)

    pages = range(1, 212)
    url = BASE_URL + "/stats"

    for page in pages:
        params = {'per_page': PER_PAGE, 'page': page, 'seasons[]': 2022}
        response = requests.get(url=url, params=params).json()['data']
        for r in response:
            if (r['game'] is None) or (r['player'] is None) or (r['team'] is None):
                continue
            tmp_columns = ['id', 'ast', 'blk', 'dreb']
            data = list(map(r.get, tmp_columns))
            data.append(r['game']['id'])
            data.append(r['player']['id'])
            data.append(r['pts'])
            data.append(r['reb'])
            data.append(r['stl'])
            data.append(r['team']['id'])
            data.append(r['turnover'])

            tmp_df = pd.DataFrame([data], columns=df_columns)
            df = pd.concat([df, tmp_df], axis=0, ignore_index=True)

        if page % 50 == 1:
            print(f"DONE - PAGE {page}")

    df.to_csv('data/stats.csv', index=False)
    print("DONE")


def get_avg_stats():
    df_columns = ['games_played', 'player_id', 'season', 'min',
                  'fgm', 'fg3m', 'fg3a', 'ftm', 'fta', 'oreb', 'dreb',
                  'reb', 'ast', 'stl', 'blk', 'turnover', 'pf', 'pts',
                  'fg_pct', 'fg3_pct', 'ft_pct']
    df = pd.DataFrame(columns=df_columns)

    url = BASE_URL + "/season_averages"
    players = pd.read_csv('data/players.csv')
    players_id = players['id'].values.tolist()[:100]

    params = {'per_page': PER_PAGE, 'page': page, 'season': 2022, 'player_ids[]': [1,2]}
    response = requests.get(url=url, params=params).json()['data']
    while True:
        response = requests.get(url=url, params=params).json()['data']
        if not response:
            break
        for r in response:
            data = list(map(r.get, df_columns))
            tmp_df = pd.DataFrame([data], columns=df_columns)
            df = pd.concat([df, tmp_df], axis=0, ignore_index=True)

        page += 1
        params = {'per_page': PER_PAGE, 'page': page, 'seasons[]': season, 'player_ids[]': players_id}

        if page % 50 == 1:
            print(f"DONE - PAGE {page}")

    df.to_csv('data/season_avg_stats.csv', index=False)
    print("DONE")


if __name__ == '__main__':
    # get_players()
    # get_teams()
    get_games()
    # get_stats()
    # get_avg_stats()
