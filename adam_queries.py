import mysql.connector

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


def query_1(min_votes, year):
    return f"""
    SELECT ranks.title, ranks.genre, ranks.rate
    FROM 	(
            SELECT      M.title AS title, G.genre AS genre, R.mean_vote AS rate,
                            ROW_NUMBER() OVER (PARTITION BY G.genre ORDER BY R.mean_vote DESC) AS movieRank
            FROM        (SELECT *
                        FROM movie
                        WHERE YEAR = {year}) M
            JOIN        genre G ON M.id = G.movie_id
            JOIN        rating R ON M.id = R.id
            WHERE       R.total_votes >= {min_votes}
            ) AS ranks
    WHERE ranks.movieRank = 1
    """


def query_2(min_rating):
    return f"""
    SELECT      PE.children, COUNT(person_id)
    FROM        principal PR
    JOIN        person PE ON PR.person_id = PE.id
    JOIN        rating R ON PR.movie_id = R.id
    WHERE       R.mean_vote >= {min_rating} AND
                (PR.category = 'actor' OR PR.category = 'actress')
    GROUP BY    PE.children
    """

def query_3():
    return """
    SELECT      PE.name AS name, COUNT(DISTINCT G.genre) AS genres
    FROM        principal PR
    JOIN        person PE ON PR.person_id = PE.id
    JOIN        genre G ON G.movie_id = PR.movie_id
    WHERE       PR.category = 'writer'
    GROUP BY    PR.person_id
    ORDER BY    COUNT(DISTINCT G.genre) DESC
    LIMIT       10
    """

def query_4(role):
    return f"""
    select person.name,count(movie_id) as numberOfBestPictureWinningMovieByHim
    from principal,person
    where category={role} and principal.person_id=person.id and exists (select * from best_picture_winners where best_picture_winners.id=principal.movie_id)
    group by principal.person_id
    order by count(movie_id) desc
    limit 1;
    """

def query_5(income,vote,actors):
    return f"""
    select movie.title
    from principal, movie,rating 
    where movie.id=rating.id and rating.mean_vote>={vote} and principal.movie_id=movie.id and movie.usa_gross_income>={income} and (principal.category="actor" or principal.category="actress")
    group by principal.movie_id
    having count(principal.id)>={actors};
    """

def query_6(name):
    return f"""
    select movie.title,count(if(match(person.name) against ({name}),1, NULL)) as numOf
    from person, movie,principal
    where person.id=principal.person_id and movie.id=principal.movie_id and principal.category="actor"
    group by movie.id
    order by numOf desc;
    """

def query_7(country):
    return f"""
    select birthplace, count(id)
    from person
    where birthplace like '%{country}'
    group by birthplace
    having count(id)>0
    order by count(id) desc;
    """


def get_query_result(sql):
    cursor.execute(sql)
    return cursor.fetchall()
    

cursor.close()
db.close()
