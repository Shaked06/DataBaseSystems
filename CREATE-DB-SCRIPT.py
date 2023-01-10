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
    # create_table("venues", "(id INT PRIMARY KEY,"
    #                        "name VARCHAR(255),"
    #                        "capacity INT,"
    #                        "grass INT,"
    #                        "city VARCHAR(255),"
    #                        "state VARCHAR(255))")
    # insert_values_into_table_from_csv("venues", 6)

    # create_table("teams", "(id INT PRIMARY KEY,"
    #                       " school VARCHAR(255),"
    #                       " mascot VARCHAR(255),"
    #                       " abbreviation VARCHAR(255),"
    #                       " venue_id INT,"
    #                       "FOREIGN KEY (venue_id) REFERENCES venues(id))")
    # insert_values_into_table_from_csv("teams", 5)
    # create_index("teams", "school")

    # create_table("games", "(id INT PRIMARY KEY,"
    #                       " season INT,"
    #                       " home_id INT,"
    #                       " away_id INT,"
    #                       " FOREIGN KEY (home_id) REFERENCES teams(id),"
    #                       " FOREIGN KEY (away_id) REFERENCES teams(id))")
    # insert_values_into_table_from_csv("games", 4)

    # create_table("coaches", "(first_name VARCHAR(255),"
    #                         "second_name VARCHAR(255),"
    #                         "year INT,"
    #                         "wins INT,"
    #                         "losses INT,"
    #                         "ties INT,"
    #                         "school VARCHAR(255))")
    # insert_values_into_table_from_csv("coaches", 7)
    # query = "ALTER TABLE coaches ADD id INT PRIMARY KEY AUTO_INCREMENT"
    # query = "ALTER TABLE coaches ADD FOREIGN KEY (school) REFERENCES teams(school)"
    # cursor.execute(query)

    # create_table("stats", "(team VARCHAR(255),"
    #                       "stat_name VARCHAR(255),"
    #                       "stat_value INT,"
    #                       "season VARCHAR(255))")
    # insert_values_into_table_from_csv("stats", 4)
    # query = "ALTER TABLE stats ADD id INT PRIMARY KEY AUTO_INCREMENT"
    # cursor.execute(query)
    # query = "ALTER TABLE stats ADD FOREIGN KEY (team) REFERENCES teams(school)"
    # cursor.execute(query)


except Exception as e:
    print("Failed to create table due to error: " + str(e))
    db.rollback()
