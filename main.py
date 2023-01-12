import requests
import pandas as pd
import os

API_TOKEN = "Bearer n6ltTo7OHNOdFrWhoNnGVM25QQRg3GTwyC7UnBTErHL6oFaIhlaD4OqbW42KMOai"
BASE_URL = "https://api.collegefootballdata.com"
HEADERS = {
    'Authorization': API_TOKEN
}
SEASONS = [_ for _ in range(2020, 2023)]


def get_teams():
    columns = ['id', 'school', 'abbreviation', 'mascot', 'venue_id']
    df = pd.DataFrame(columns=columns)
    url = BASE_URL + "/teams"

    response = requests.request("GET", url, headers=HEADERS).json()
    for team in response:
        tmp_columns = ['id', 'school', 'abbreviation', 'mascot']
        row = list(map(team.get, tmp_columns))
        row.append(team["location"]["venue_id"])
        tmp_df = pd.DataFrame([row], columns=columns)
        df = pd.concat([df, tmp_df], axis=0, ignore_index=True)

    df.to_csv('data/teams.csv', index=False)


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
    df.to_csv('data/games_20_22.csv', index=False)


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
    df.to_csv('data/coaches.csv', index=False)


def get_stats():
    df_columns = ['team', 'stat_name', 'stat_value', 'season']
    api_columns = ['team', 'statName', 'statValue', 'season']
    df = pd.DataFrame(columns=df_columns)

    for season in SEASONS:
        url = BASE_URL + f"/stats/season?year={season}"
        response = requests.request("GET", url, headers=HEADERS).json()
        for row in response:
            row = list(map(row.get, api_columns))
            tmp_df = pd.DataFrame([row], columns=df_columns)
            df = pd.concat([df, tmp_df], axis=0, ignore_index=True)
        print(f"DONE - {season}")
    df.to_csv('data/stats_20_22.csv', index=False)


def get_plays_per_season():
    weeks = [_ for _ in range(1, 16)]  # TODO:: CHECK THAT THIS IS TRUE

    columns = ['id', 'home', 'away', 'game_id', 'drive_id', 'drive_number', 'play_number',
               'yard_line', 'yards_to_goal', 'scoring', 'play_type']

    for season in SEASONS:
        df = pd.DataFrame(columns=columns)
        df['scoring'] = df['scoring'].astype('boolean')
        for week in weeks:
            url = BASE_URL + f"/plays?year={season}&week={week}"
            responses = requests.request("GET", url, headers=HEADERS).json()
            for response in responses:
                row = list(map(response.get, columns))
                tmp_df = pd.DataFrame([row], columns=columns)
                tmp_df['scoring'] = tmp_df['scoring'].astype('boolean')
                df = pd.concat([df, tmp_df], axis=0, ignore_index=True)

        df.to_csv(f'data/plays_per_season/plays_{season}.csv', index=False)
        print(f"DONE - {season}")


def get_plays():
    base_url = "data/plays_per_season"
    columns = ['id', 'home', 'away', 'game_id', 'drive_id', 'drive_number', 'play_number',
               'yard_line', 'yards_to_goal', 'scoring', 'play_type']

    get_plays_per_season()

    file_list = os.listdir(base_url)
    df = pd.DataFrame(columns=columns)
    df['scoring'] = df['scoring'].astype('boolean')
    for file in file_list:
        tmp_df = pd.read_csv(f'{base_url}/{file}')
        tmp_df['scoring'] = tmp_df['scoring'].astype('boolean')
        df = pd.concat([df, tmp_df], ignore_index=True)

    df.to_csv("data/plays.csv")
    print("DONE")


def get_plays_20_22():
    base_url = "data/plays_per_season"
    columns = ['id', 'home', 'away', 'game_id', 'drive_id', 'drive_number', 'play_number',
               'yard_line', 'yards_to_goal', 'scoring', 'play_type']

    # get_plays_per_season()

    file_list = os.listdir(base_url)
    df = pd.DataFrame(columns=columns)
    df['scoring'] = df['scoring'].astype('boolean')
    for file in file_list:
        if file in [f"plays_{season}.csv" for season in range(2020, 2023)]:
            tmp_df = pd.read_csv(f'{base_url}/{file}')
            tmp_df['scoring'] = tmp_df['scoring'].astype('boolean')
            df = pd.concat([df, tmp_df], ignore_index=True)

    df.to_csv("data/plays_20_22.csv")
    print("DONE")


def get_venues():
    columns = ['id', 'name', 'capacity', 'grass', 'city', 'state']
    df = pd.DataFrame(columns=columns)
    url = BASE_URL + "/venues"

    response = requests.request("GET", url, headers=HEADERS).json()
    for team in response:
        row = list(map(team.get, columns))
        tmp_df = pd.DataFrame([row], columns=columns)
        df = pd.concat([df, tmp_df], axis=0, ignore_index=True)

    df.to_csv('data/venues.csv', index=False)


def get_stats_per_play():
    df_columns = ['play_id', 'game_id', 'week', 'season', 'team', 'opponent', 'team_score', 'opponent_score',
                  'yards_to_goal', 'down', 'distance', 'stat_type', 'stat']
    df = pd.DataFrame(columns=df_columns)

    for season in SEASONS:
        url = BASE_URL + f"/play/stats?year={season}"
        response = requests.request("GET", url, headers=HEADERS).json()
        for row in response:
            tmp_df = pd.DataFrame([row], columns=df_columns)
            df = pd.concat([df, tmp_df], axis=0, ignore_index=True)
        print(f"DONE - {season}")

    df.to_csv('data/stats_per_play.csv', index=False)


if __name__ == '__main__':
    # get_teams()
    # get_games()
    # get_coaches()
    # get_venues()
    get_stats_per_play()