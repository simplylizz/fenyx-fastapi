import copy
import json
from textwrap import indent
import os

from numpy import double

from schemas import Player

_WORKING_DIR = os.path.dirname(os.path.abspath(__file__))
_GAMES_STORAGE = f"{_WORKING_DIR}\\games.json"
_PLAYERS_STORAGE = f"{_WORKING_DIR}\\players.json"

# games = {
#     1: {
#         "id": 1,
#         "status": "new",
#         "current_move": "x",
#         "field": [
#             [None, None, None],
#             [None, None, None],
#             [None, None, None],
#         ],
#     },
# }


def write_games_to_storage(games):
    with open(_GAMES_STORAGE, "w") as f:
        json.dump(games, f, indent=4)


def read_games_from_storage():
    with open(_GAMES_STORAGE, "r") as f:
        return dict(json.load(f))

def get_games():
    return list(read_games_from_storage().values())

def create_game(player_id):
    games = read_games_from_storage()
    id_ = len(games) + 1

    games[str(id_)] = {
        "id": id_,
        "status": "new",
        "last_move_player_id": None,
        "field": [
            [None, None, None],
            [None, None, None],
            [None, None, None],
        ],
        "player_x": player_id,
        "player_o": None
    }

    write_games_to_storage(games)
    return games[str(id_)]


def get_game(id: int) -> dict | None:
    games = read_games_from_storage()
    game = games.get(id)
    return game


def update_game(id: int, data: dict):
    games = read_games_from_storage()
    if id not in games:
        raise ValueError(f"No game with id {id}")

    games[id] = data
    write_games_to_storage(games)


def read_players_from_storage():
    with open(_PLAYERS_STORAGE, "r") as f:
        return json.load(f)


def write_players_to_storage(players):
    with open(_PLAYERS_STORAGE, "w") as f:
        json.dump(players, f, indent=4)


def register_player(player: Player):
    players = read_players_from_storage()
    player.id = len(players) + 1
    players[player.id] = {
        'name': player.name,
        'id': player.id,
        'wins': 0
    }
    write_players_to_storage(players)


def update_wins(player_id: str, points: double):
    players = read_players_from_storage()
    if player_id not in players:
        raise ValueError(f"No player with id {player_id}")

    players[player_id]['wins'] += points
    