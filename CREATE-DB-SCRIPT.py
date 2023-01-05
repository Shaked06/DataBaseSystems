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

def create_table_from_csv(table_name, table_columns):
    # query = f"CREATE TABLE {table_name}{table_columns}"
    # cursor.execute(query)

    df = pd.read_csv(f"./data/{table_name}.csv")
    s = ("%s," * 6)[:-1]
    i = 0
    for index, row in df.iterrows():
        if i > 3:
            break
        i += 1


        # row_values = ','.join([str(_) for _ in row])
        # query = f"INSERT INTO {table_name} VALUES ({row_values})"
        sql = f"INSERT INTO {table_name} VALUES ({s})"
        cursor.execute(sql, tuple(row))
        # cursor.execute(query)
        db.commit()

create_table_from_csv("games", "(id VARCHAR(255), season VARCHAR(255), home_id VARCHAR(255), home_team VARCHAR(255), away_id VARCHAR(255), away_tean VARCHAR(255))")