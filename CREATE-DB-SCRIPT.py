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

# sql = "CREATE TABLE rating(id VARCHAR(255) PRIMARY KEY,total_votes INT,mean_vote DECIMAL(2,1))"
# cursor.execute(sql)

x = 1
