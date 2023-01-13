import mysql.connector
import pandas as pd
import numpy as np

DB_NAME = "DbMysql11"

# init connection
db = mysql.connector.connect(
    host="localhost",
    port=3305,
    user=DB_NAME,
    password=DB_NAME,
    database=DB_NAME
    )

cursor = db.cursor()

# create table from csv
def create_table(create_sql, table_name, cols):
    s = ("%s,"*cols)[:-1]
    df = pd.read_csv(f"./data/{table_name}.csv", index_col=False, delimiter = ',')
    df = df.where(df.notnull(), None)
    cursor.execute(create_sql)
    for i, row in df.iterrows():
        # some rows doesn't match foreign key constraint
        try:
            sql = f"INSERT INTO {table_name} VALUES ({s})"
            cursor.execute(sql, tuple(row))
            db.commit()
        except:
            pass


def create_table_movie():
    sql = "CREATE TABLE movie(id VARCHAR(255) PRIMARY KEY,title VARCHAR(255),year INT,usa_gross_income INT)"
    create_table(sql, "movie", 4)

def create_table_rating():
    sql = "CREATE TABLE rating(id VARCHAR(255) PRIMARY KEY,total_votes INT,mean_vote DECIMAL(2,1))"
    create_table(sql, "rating", 3)

def create_table_person():
    sql = "CREATE TABLE person(id VARCHAR(255) PRIMARY KEY,name VARCHAR(255),birthplace VARCHAR(255), children INT)"
    create_table(sql, "person", 4)


def create_table_principal():
    sql = "CREATE TABLE principal(movie_id VARCHAR(255),person_id VARCHAR(255),category VARCHAR(255),FOREIGN KEY (movie_id) REFERENCES movie(id), FOREIGN KEY (person_id) REFERENCES person(id))"
    create_table(sql, "principal", 3)
    cursor.execute("ALTER TABLE principal ADD id INT PRIMARY KEY AUTO_INCREMENT")
    db.commit()

# special case - create genre table (split csv data)
def create_table_genre():
    sql = "CREATE TABLE genre(movie_id VARCHAR(255),genre VARCHAR(255), FOREIGN KEY (movie_id) REFERENCES movie(id))"
    df = pd.read_csv(f"./data/genre.csv", index_col=False, delimiter = ',')
    df = df.where(df.notnull(), None)
    cursor.execute(sql)
    for i, row in df.iterrows():
        sql = f"INSERT INTO genre VALUES (%s,%s)"
        genres = row[1].split(',')
        for genre in genres:
            cursor.execute(sql, (row[0],genre.strip()))
        db.commit()
    cursor.execute("ALTER TABLE genre ADD id INT PRIMARY KEY AUTO_INCREMENT")
    db.commit()

# create index sql command generator
def get_index_sql(name, table, field):
    return f"CREATE INDEX {name} ON {table}({field})"

# create all indices
def create_indicies():
    try:
        cursor.execute(get_index_sql('yearIndex', 'movie', 'year'))
        cursor.execute(get_index_sql('grossIndex', 'movie', 'usa_gross_income'))
        cursor.execute(get_index_sql('childrenIndex', 'person', 'children'))
        cursor.execute(get_index_sql('totalVotesIndex', 'rating', 'total_votes'))
        cursor.execute(get_index_sql('meanVoteIndex', 'rating', 'mean_vote'))
        cursor.execute(get_index_sql('genreIndex', 'genre', 'genre'))
        cursor.execute(get_index_sql('principalIndex', 'principal', 'category'))
        cursor.execute(get_index_sql('birthplace', 'person', 'birthplace'))
        cursor.execute("CREATE FULLTEXT INDEX personFullTextIndex ON person(name)")
        db.commit()
    except: 
        print("an error occurred")
        db.rollback()


# create all db tables
def init_db():
    try:
        create_table_movie()
        create_table_person()
        create_table_rating()
        create_table_principal()
        create_table_genre()
    except: 
        print("an error occurred")
        db.rollback()

# add 'not null' restrictions - added after we created the tables
def alter_not_null():
    try:
        cursor.execute("ALTER TABLE movie MODIFY title VARCHAR(255) NOT NULL")
        cursor.execute("ALTER TABLE movie MODIFY year INT NOT NULL")
        cursor.execute("ALTER TABLE person MODIFY name VARCHAR(255) NOT NULL")
        cursor.execute("ALTER TABLE person MODIFY children INT NOT NULL DEFAULT 0")
        cursor.execute("ALTER TABLE principal MODIFY category VARCHAR(255) NOT NULL")
        cursor.execute("ALTER TABLE rating MODIFY total_votes INT NOT NULL")
        cursor.execute("ALTER TABLE rating MODIFY mean_vote DECIMAL(2,1) NOT NULL")
        cursor.execute("ALTER TABLE genre MODIFY genre VARCHAR(255) NOT NULL")
        db.commit()
    except:
        print("an error occurred")
        db.rollback()


init_db()
alter_not_null()
create_indicies()

cursor.close()
db.close()