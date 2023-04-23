import copy
import uuid
from typing import Optional
from pydantic import BaseModel


_GAMES_STORAGE = {
    1: {
        "id": 1,
        "player_id_1": "",
        "player_id_2": "",
        "status": "new",
        "current_move": "x",
        "player_score_1": 0,
        "player_score_2": 0,
        "field": [
            ["", "", ""],
            ["", "", ""],
            ["", "", ""],
        ],
    },
}


def register_player():
    global player_id_1, player_id_2

    player_id_1 = uuid.uuid4()
    player_id_2 = uuid.uuid4()

 #   return _GAMES_STORAGE[player_id]


def get_games():
    return list(_GAMES_STORAGE.values)


# def create_game():
#     id_ = len(_GAMES_STORAGE) + 1

#     _GAMES_STORAGE[id_, player_id_1, player_id_2] = {
#         "id": id_,
#         "player_id_1": player_id_1,
#         "player_id_2": player_id_2,
#         "status": "new",
#         "current_move": "x",
#         "field": [
#             [None, None, None],
#             [None, None, None],
#             [None, None, None],
#         ],
#     }

    return _GAMES_STORAGE[id_, player_id_1, player_id_2]


def get_game(id: int) -> dict | None:
    game = _GAMES_STORAGE.get(id)
    return copy.deepcopy(game)

# player_id_1 and player_id_2 always exist and they are always part of _games_storage


# def update_game(id: int, data: dict):
#     if id in _GAMES_STORAGE:
#         raise ValueError(f"No game with id {id}")

#     _GAMES_STORAGE[id] = data
