import sqlite3
from contextlib import closing
from objects import Player, Position

conn = None

def connect():
    global conn
    if not conn:
        conn = sqlite3.connect("bbmanager.sqlite")
        conn.row_factory = sqlite3.Row

def close():
    if conn:
        conn.close()

# function takes a value and returns an object with corresponding id and position
def make_position(row):
    return Position(row["positionID"], row["position"])

# sqlite command to retrieve all positions and id's and append them to a list
def get_positions():
    query = '''SELECT positionID, position
               FROM Position'''
    with closing(conn.cursor()) as c: # type: ignore
        c.execute(query)
        results = c.fetchall()

    positions = []
    for row in results:
        positions.append(make_position(row))
    return positions
 
def make_player(row):
    return Player(row["playerID"], row["batOrder"], row["firstName"], row["lastName"], row["position"], row["atBats"], row["hits"])

def get_player(index):
    query = '''SELECT playerID, batOrder, firstName, lastName,
                      Player.position, atBats, hits
               FROM Player
               WHERE batOrder = ?'''
    with closing(conn.cursor()) as c: # type: ignore
        c.execute(query, (index,))
        row = c.fetchone()
        if row:
            return make_player(row)
        else:
            return None

def get_players():
    query = '''SELECT playerID, batOrder, firstName, lastName, Player.position, atBats, hits
               FROM Player'''
    with closing(conn.cursor()) as c: # type: ignore
        c.execute(query)
        results = c.fetchall()

    lineup = []
    for row in results:
        lineup.append(make_player(row))
    return lineup

def add_player(player):
    query = '''INSERT INTO Player (batOrder, firstName, lastName, position, atBats, hits)
               VALUES (?, ?, ?, ?, ?, ?)'''
    with closing(conn.cursor()) as c: # type: ignore
        c.execute(query, (player.batOrder, player.fname, player.lname, player.pos, player.ab, player.hits))
        conn.commit() # type: ignore

def delete_player(index):
    query = '''DELETE FROM Player 
               WHERE batOrder = ?'''
    with closing(conn.cursor()) as c: # type: ignore
        c.execute(query, (index,))
        conn.commit() # type: ignore

def update_batting_order():
    query = '''UPDATE Player
               SET batOrder = (
               SELECT COUNT(*)
               FROM Player AS P
               WHERE P.playerID < Player.playerID) +
               (SELECT COUNT(*)
               FROM Player AS P
               WHERE P.playerID = Player.playerID
               AND P.batOrder <= Player.batOrder)'''
    with closing(conn.cursor()) as c: # type: ignore
        c.execute(query)
        conn.commit() # type: ignore
      
def update_player_data(player):
    query = '''UPDATE Player
               SET firstName = ?,
               lastName = ?,
               position = ?,
               atBats = ?,
               hits = ?
               WHERE batOrder = ?'''
    with closing(conn.cursor()) as c: # type: ignore
        c.execute(query, (player.fname, player.lname, player.pos, player.ab, player.hits, player.batOrder))
        conn.commit() # type: ignore
