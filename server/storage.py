from __future__ import annotations
import copy
from tinydb import TinyDB, Query

db = TinyDB('game_data.json')

# create a new table for storing games
games_table = db.table('games')

# create a new table for storing players
players_table = db.table('players')



def get_games():
    return list(games_table.all())


def get_players():
    return list(players_table.all())


def create_game():
    try:
        id_ = len(games_table) + 1
        players = players_table.all()
        
        player_id = players[0]["player_id"]
        
        games_table.insert({
            "id": id_,
            "player_x": player_id,
            "player_o": None,
            "status": "waiting",
            "current_move": "x",
            "field": [[""]*3 for _ in range(3)],
            "winner": None
        })

        return list(games_table.all())
    
    except (AttributeError, IndexError):
        return "Register player first"


def get_game(id: int) -> dict | None:
    User = Query()
    game = games_table.search(User.id == id)
    return copy.deepcopy(*game)


def add_player():
    player_id = len(players_table) +1
    
    players_table.insert({
        "player_id": player_id,
        "score": 0,
    })
    
    
    return list(players_table.all())


def get_player(id: int) -> dict | None:
    User = Query()
    player = players_table.search(User.player_id == id)
    return copy.deepcopy(*player)
    
  
def update_game(id: int, data: dict):
    User = Query()
    game = games_table.search(User.id == id)
    
    if game[0] not in games_table:
        raise ValueError(f"No game with id {id}")
    
    games_table.update(data, User.id == id)
    
    
def update_player(id: int, data: dict):
    User = Query()
    player = players_table.search(User.player_id == id)
    
    if player[0] not in players_table:
        raise ValueError(f"No player with id {id}")
    
    players_table.update(data, User.player_id == id)
