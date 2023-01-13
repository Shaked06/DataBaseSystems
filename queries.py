import mysql.connector

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

# maximus points minimum effort
query1 = """SELECT p2.first_name, p2.last_name, t.pts_dreb_difference
FROM(
SELECT p.id, AVG((s.pts - s.dreb)) AS pts_dreb_difference  
FROM players p 
JOIN stats s ON p.id = s.player_id
GROUP BY p.id) AS t
JOIN players p2 ON p2.id = t.id
ORDER BY pts_dreb_difference DESC 
LIMIT 20"""

# top overall offence and defense scores
query2 = """SELECT p2.first_name, p2.last_name, te.full_name, t.overall_offense_score, t.overall_defense_score
FROM (
SELECT p.id, SUM(s.pts + s.ast + s.dreb) AS overall_offense_score, SUM(s.reb + s.stl + s.blk) AS overall_defense_score
FROM stats s 
JOIN players p ON s.player_id = p.id 
GROUP BY p.id
HAVING MAX(s.pts + s.ast + s.dreb) > 0 AND 
MAX(s.reb + s.stl + s.blk) > 0) AS t
JOIN players p2 ON p2.id = t.id
JOIN teams te ON p2.team_id = te.id 
ORDER BY overall_offense_score DESC, overall_defense_score DESC
 """

# top 5 teams with avg home score - avg away score
query3 = """SELECT t.full_name, ABS(t1.home_team_avg_score - t2.visitor_team_avg_score) AS home_visitor_difference
FROM (
SELECT AVG(g.home_team_score) AS home_team_avg_score, g.home_team_id 
FROM games g 
WHERE g.season = 2022
GROUP BY g.home_team_id) AS t1
JOIN (
SELECT AVG(g.visitor_team_score) AS visitor_team_avg_score, g.visitor_team_id 
FROM games g 
WHERE g.season = 2022
GROUP BY g.visitor_team_id) AS t2 ON t1.home_team_id = t2.visitor_team_id
JOIN teams t ON t.id = t1.home_team_id
ORDER BY home_visitor_difference ASC 
LIMIT 5
"""

query4 = """
"""


def get_results(query):
    cursor.execute(query)
    return cursor.fetchall()


a = get_results(query1)
x = 1
