import requests
import pandas as pd

API_TOKEN = "Bearer n6ltTo7OHNOdFrWhoNnGVM25QQRg3GTwyC7UnBTErHL6oFaIhlaD4OqbW42KMOai"
BASE_URL = "https://api.collegefootballdata.com"
HEADERS = {
    'Authorization': API_TOKEN
}
SEASONS = [_ for _ in range(2000, 2023)]


def get_teams():
    columns = ['id', 'school', 'abbreviation', 'mascot']
    df = pd.DataFrame(columns=columns)
    url = BASE_URL + "/teams"

    response = requests.request("GET", url, headers=HEADERS).json()
    for team in response:
        row = list(map(team.get, columns))
        tmp_df = pd.DataFrame([row], columns=columns)
        df = pd.concat([df, tmp_df], axis=0, ignore_index=True)

    df.to_csv('teams.csv', index=False)


def get_games():
    columns = ['id', 'season', 'home_id', 'home_team', 'away_id', 'away_team']

    df = pd.DataFrame(columns=columns)

    for season in SEASONS:
        url = BASE_URL + f"/games?year={season}"
        response = requests.request("GET", url, headers=HEADERS).json()
        for game in response:
            row = list(map(game.get, columns))
            tmp_df = pd.DataFrame([row], columns=columns)
            df = pd.concat([df, tmp_df], axis=0, ignore_index=True)
        print(f"DONE - {season}")
    df.to_csv('games.csv', index=False)


def get_coaches():
    columns = ['first_name', 'last_name', 'year', 'wins', 'losses', 'ties', 'school']
    df = pd.DataFrame(columns=columns)
    start_year = 2000
    end_year = 2022
    url = BASE_URL + f"/coaches?minYear={start_year}&maxYear={end_year}"
    responses = requests.request("GET", url, headers=HEADERS).json()
    for response in responses:
        metadata_columns = ['first_name', 'last_name']
        metadata_values = list(map(response.get, metadata_columns))
        seasons = response["seasons"]
        for season in seasons:
            per_season_column = ['year', 'wins', 'losses', 'ties', 'school']
            per_season_values = list(map(season.get, per_season_column))
            tmp_df = pd.DataFrame([metadata_values + per_season_values], columns=columns)
            df = pd.concat([df, tmp_df], axis=0, ignore_index=True)
            print(tmp_df)
    df.to_csv('coaches.csv', index=False)


def get_stats():
    columns = ['team', 'stat_name', 'stat_value', 'season']
    df = pd.DataFrame(columns=columns)

    for season in SEASONS:
        url = BASE_URL + f"/stats/season?year={season}"
        response = requests.request("GET", url, headers=HEADERS).json()
        for game in response:
            row = list(map(game.get, columns))
            tmp_df = pd.DataFrame([row], columns=columns)
            df = pd.concat([df, tmp_df], axis=0, ignore_index=True)
        print(f"DONE - {season}")
    df.to_csv('stats.csv', index=False)


if __name__ == '__main__':
    # get_games()
    # get_coaches()
    get_stats()
