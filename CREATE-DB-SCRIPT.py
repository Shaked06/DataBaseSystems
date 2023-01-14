import mysql.connector
import pandas as pd

DB_NAME = "shakedcaspi"
DB_PASSWORD = "shake65274"

db = mysql.connector.connect(
    host="localhost",
    port=3305,
    user=DB_NAME,
    password=DB_PASSWORD,
    database=DB_NAME
)
cursor = db.cursor()


def create_table(table_name, table_columns):
    query = f"CREATE TABLE {table_name}{table_columns}"
    cursor.execute(query)
    # need to commit?


def insert_values_into_table_from_csv(table_name, number_of_columns):
    df = pd.read_csv(f"./data/{table_name}.csv")
    s = ("%s," * number_of_columns)[:-1]

    for index, row in df.iterrows():
        query = f"INSERT INTO {table_name} VALUES ({s})"
        cursor.execute(query, tuple(row))
        db.commit()


def create_index(table_name, column_name):
    query = f"CREATE INDEX {column_name}Index ON {table_name}({column_name})"
    cursor.execute(query)


try:
    # create_table("teams", "(id INT PRIMARY KEY,"
    #                       "abbreviation VARCHAR(255),"
    #                       "city VARCHAR(255),"
    #                       "conference VARCHAR(255),"
    #                       "full_name VARCHAR(255),"
    #                       "name VARCHAR(255))")
    # insert_values_into_table_from_csv("teams", 6)

    # create_table("players", "(id INT PRIMARY KEY,"
    #                         " first_name VARCHAR(255),"
    #                         " last_name VARCHAR(255),"
    #                         " position VARCHAR(255),"
    #                         " team_id INT,"
    #                         "FOREIGN KEY (team_id) REFERENCES teams(id))")
    # insert_values_into_table_from_csv("players", 5)
    # create_index("players", "position")

    # create_table("games", "(id INT PRIMARY KEY,"
    #                       " season INT,"
    #                       " status VARCHAR(255),"
    #                       " home_team_id INT,"
    #                       " home_team_score INT,"
    #                       " visitor_team_id INT,"
    #                       " visitor_team_score INT,"
    #                       " FOREIGN KEY (home_team_id) REFERENCES teams(id),"
    #                       " FOREIGN KEY (visitor_team_id) REFERENCES teams(id))")
    # insert_values_into_table_from_csv("games", 7)
    # create_index("games", "home_team_id")
    # create_index("games", "visitor_team_id")
    # create_index("games", "season")

    # create_table("stats", "(ast INT,"
    #              "blk INT,"
    #              "dreb INT,"
    #              "game_id INT,"
    #              "player_id INT,"
    #              "pts INT,"
    #              "reb INT,"
    #              "stl INT,"
    #              "team_id INT,"
    #              "turnover INT,"
    #              "FOREIGN KEY (game_id) REFERENCES games(id),"
    #              "FOREIGN KEY (player_id) REFERENCES players(id),"
    #              "FOREIGN KEY (team_id) REFERENCES teams(id))")
    # insert_values_into_table_from_csv("stats", 10)
    # query = "ALTER TABLE stats ADD id INT PRIMARY KEY AUTO_INCREMENT"
    # cursor.execute(query)

    create_table("arenas", "(id INT PRIMARY KEY,"
                           "team_id INT,"
                           "city VARCHAR(255),"
                           "arena VARCHAR(255),"
                           "capacity VARCHAR(255),"
                           "coordinates VARCHAR(255),"
                           "year_of_construction INT, "
                           "FOREIGN KEY (team_id) REFERENCES teams(id))"
                 )
    insert_values_into_table_from_csv("arenas", 7)


except Exception as e:
    print("Failed to create table due to error: " + str(e))
    db.rollback()
