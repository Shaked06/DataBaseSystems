import requests
import pandas as pd

API_TOKEN = "Bearer n6ltTo7OHNOdFrWhoNnGVM25QQRg3GTwyC7UnBTErHL6oFaIhlaD4OqbW42KMOai"

def get_teams():
	df = pd.DataFrame(columns=['id', 'school', 'abbreviation', 'mascot'])
	url = "https://api.collegefootballdata.com/teams"
	headers = {
		'Authorization' : API_TOKEN
	}

	response = requests.request("GET", url, headers=headers).json()
	for team in response:
		row = list(map(team.get, ['id', 'school', 'abbreviation', 'mascot']))
		tmp_df = pd.DataFrame([row], columns = ['id', 'school', 'abbreviation', 'mascot'])
		df = pd.concat([df, tmp_df], axis=0, ignore_index=True)

	df.to_csv('teams.csv', index=False)


def get_games():
	seasons = [year for year in range(2000, 2023)]
	columns = ['id', 'season', 'home_id', 'home_team', 'away_id', 'away_team']
	df = pd.DataFrame(columns=columns)

	for season in seasons:
		url = f"https://api.collegefootballdata.com/games?year={season}"
		headers = {
			'Authorization' : API_TOKEN
		}

		response = requests.request("GET", url, headers=headers).json()
		for game in response:
			row = list(map(game.get, columns))
			tmp_df = pd.DataFrame([row], columns = columns)
			df = pd.concat([df, tmp_df], axis=0, ignore_index=True)

	df.to_csv('games.csv', index=False)



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    get_games()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
