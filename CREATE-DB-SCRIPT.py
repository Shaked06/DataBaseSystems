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

def create_table_from_csv(file_name, table_name, table_columns):
    query = f"CREATE TABLE {table_name} {table_columns}"
    cursor.execute(query)

    df = pd.read_csv(f"./data/{table_name}.csv")



create_table_from_csv("games.csv", "games", "test()")