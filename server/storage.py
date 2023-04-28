import copy
from typing import Dict, List, Optional

from tinydb import TinyDB, Query

db = TinyDB('database.json')

games_table = db.table('games')
players_table = db.table('players')

def get_games() -> List[Dict]:
    return games_table.all()


def create_game(player_id: int) -> Dict:
    game_data = {
        "status": "new",
        "current_move": "x",
        "player_x": player_id,
        "player_o": None,
        "field": [
            [None, None, None],
            [None, None, None],
            [None, None, None],
        ],
    }
    game_id = games_table.insert(game_data)
    game_data['id'] = game_id
    games_table.update(game_data, doc_ids=[game_id])
    return game_data


def get_game(id: int) -> Optional[Dict]:
    game = games_table.get(doc_id=id)
    return copy.deepcopy(game)


def update_game(id: int, data: Dict):
    games_table.update(data, doc_ids=[id])

def create_player(name: str) -> Dict:
    player_data = {
        "name": name,
    }
    player_id = players_table.insert(player_data)
    player_data['id'] = player_id
    players_table.update(player_data, doc_ids=[player_id])
    return player_data


def get_player(id: int) -> Optional[Dict]:
    Player = Query()
    player = players_table.get(Player.id == id)
    return copy.deepcopy(player) if player else None



def update_player(id: int, data: Dict):
    players_table.update(data, doc_ids=[id])
    
def register_player(name: str) -> Dict:
    player_data = create_player(name)
    return player_data