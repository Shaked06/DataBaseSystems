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
    #need to commit?


def insert_values_into_table_from_csv(table_name, number_of_columns):
    df = pd.read_csv(f"./data/{table_name}.csv")
    s = ("%s," * number_of_columns)[:-1]

    for index, row in df.iterrows():
        query = f"INSERT INTO {table_name} VALUES ({s})"
        cursor.execute(query, tuple(row))
        db.commit()




try:
    # create_table("teams", "(id INT PRIMARY KEY,"
    #                       " school VARCHAR(255),"
    #                       " mascot VARCHAR(255),"
    #                       " abbreviation VARCHAR(255))")
    # insert_values_into_table_from_csv("teams", 4)

    # create_table("games", "(id INT PRIMARY KEY,"
    #                       " season INT,"
    #                       " home_id INT,"
    #                       " home_team VARCHAR(255),"
    #                       " away_id INT,"
    #                       " away_team VARCHAR(255),"
    #                       " FOREIGN KEY (home_id) REFERENCES teams(id),"
    #                       " FOREIGN KEY (away_id) REFERENCES teams(id))")
    # insert_values_into_table_from_csv("games", 6)

    # create_table("roster", )

except Exception as e:
    print("Failed to create table: " + str(e))
    db.rollback()

