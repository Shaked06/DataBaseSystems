import mysql.connector

# DB-REGISTRATION INFORMATION
DB_NAME = "shakedcaspi"
DB_PASSWORD = "shake65274"

# GLOBAL CONNECTION TO THE DB
db = mysql.connector.connect(
    host="localhost",
    port=3305,
    user=DB_NAME,
    password=DB_PASSWORD,
    database=DB_NAME
)
# GLOBAL INITIALIZATION - CURSOR
cursor = db.cursor()

# maximus points minimum effort
query1 = """
    SELECT p2.first_name, p2.last_name, t.pts_dreb_difference
    FROM(
        SELECT p.id, AVG((s.pts - s.dreb)) AS pts_dreb_difference  
    FROM players p 
    JOIN stats s ON p.id = s.player_id
    GROUP BY p.id) AS t
    JOIN players p2 ON p2.id = t.id
    ORDER BY pts_dreb_difference DESC 
    LIMIT 20
    """

# top overall offence and defense scores
query2 = """
    SELECT p2.first_name, p2.last_name, te.full_name, t.overall_offense_score, t.overall_defense_score
    FROM (
            SELECT p.id, SUM(s.pts + s.ast + s.dreb) AS overall_offense_score, SUM(s.reb + s.stl + s.blk) AS overall_defense_score
            FROM stats s 
            JOIN players p ON s.player_id = p.id 
            GROUP BY p.id
            HAVING MAX(s.pts + s.ast + s.dreb) > 0 AND MAX(s.reb + s.stl + s.blk) > 0
        ) AS t
    JOIN players p2 ON p2.id = t.id
    JOIN teams te ON p2.team_id = te.id 
    ORDER BY overall_offense_score DESC, overall_defense_score DESC
    """

# top 5 teams with avg home score - avg away score
query3 = """
    SELECT t.full_name, ABS(t1.home_team_avg_score - t2.visitor_team_avg_score) AS home_visitor_difference
    FROM (
        SELECT AVG(g.home_team_score) AS home_team_avg_score, g.home_team_id 
        FROM games g 
        WHERE g.season = 2022
        GROUP BY g.home_team_id
    ) AS t1
    JOIN (
            SELECT AVG(g.visitor_team_score) AS visitor_team_avg_score, g.visitor_team_id 
            FROM games g 
            WHERE g.season = 2022
            GROUP BY g.visitor_team_id
        ) AS t2 ON t1.home_team_id = t2.visitor_team_id
    JOIN teams t ON t.id = t1.home_team_id
    ORDER BY home_visitor_difference ASC 
    LIMIT 5
    """

# הכי הרבה שיפור בכמות סלים בין 2011 ל2021
# the team with the biggest improvement in terms of differences between score as a visitor team vs score as home team
query4 = """
    SELECT t1.full_name, (t1.visitor_team_score_2021 - t2.visitor_team_score_2011) AS decade_improvment
    FROM (
            SELECT g.season, t.id, SUM(g.visitor_team_score) AS visitor_team_score_2021, t.full_name 
            FROM games g
            JOIN teams t  ON t.id = g.visitor_team_id  
            WHERE g.season = 2021 
            GROUP BY g.season, t.id
        ) AS t1
    JOIN (
            SELECT g.season, t.id, SUM(g.visitor_team_score) AS visitor_team_score_2011, t.full_name 
            FROM games g
            JOIN teams t  ON t.id = g.visitor_team_id  
            WHERE g.season = 2011 
            GROUP BY g.season, t.id
        ) AS t2 
        ON t1.id = t2.id
        ORDER BY decade_improvment DESC 
    """


def get_results(query):
    cursor.execute(query)
    return cursor.fetchall()


if __name__ == "__main__":
    a = get_results(query1)

