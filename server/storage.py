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
            [None, None, None],
            [None, None, None],
            [None, None, None],
        ],
    },
}


def register_player():
    global player_id_1, player_id_2

    player_id_1 = uuid.uuid4()
    player_id_2 = uuid.uuid4()

 #   return _GAMES_STORAGE[player_id]


def show_scores():
    score_list = []
    last_list = []
    for id in _GAMES_STORAGE:
        for id.player_score_1 in _GAMES_STORAGE and id.player_score_2 in _GAMES_STORAGE:
            score_list.append(id.player_score_1, id.player_score_2)
            score_list.sort(reverse=True)
            n = 0
            for n in range(len(score_list)):

                if score_list[n] == id.player_score_1:
                    last_list.append({id.player_score_1: score_list[n]})
                    print({id.player_score_1: score_list[n]})

                elif score_list[n] == id.player_score_2:
                    last_list.append({id.player_score_1: score_list[n]})

                    print({id.player_score_2: score_list[n]})
                else:
                    pass
                n += 1
            return last_list.json.dumps()


def get_games():
    return list(_GAMES_STORAGE.values())


def create_game():
    id_ = len(_GAMES_STORAGE) + 1

    _GAMES_STORAGE[id_, player_id_1, player_id_2] = {
        "id": id_,
        "player_id_1": player_id_1,
        "player_id_2": player_id_2,
        "status": "new",
        "current_move": "x",
        "field": [
            [None, None, None],
            [None, None, None],
            [None, None, None],
        ],
    }

    return _GAMES_STORAGE[id_, player_id_1, player_id_2]


def get_game(id: int) -> dict | None:
    game = _GAMES_STORAGE.get(id)
    return copy.deepcopy(game)

# player_id_1 and player_id_2 always exist and they are always part of _games_storage


def update_game(id: int, data: dict):
    if id in _GAMES_STORAGE:
        raise ValueError(f"No game with id {id}")

    _GAMES_STORAGE[id] = data


class update_items(BaseModel):
    player_id_1: Optional[str] = None
    player_id_2: Optional[str] = None


def update_existing_users(id: int, update_items: update_items):

    if id not in _GAMES_STORAGE:
        raise ValueError(f"No game with id {id}")
    elif (_GAMES_STORAGE[id].player_id_1 != "" and _GAMES_STORAGE[id].player_id_2 != ""):
        raise ValueError(f"game with id {id}  is full")

    else:
        if update_items.player_id_1 != None:
            _GAMES_STORAGE[id].player_id_1 = update_items.player_id_1
        if update_items.player_id_2 != None:
            _GAMES_STORAGE[id].player_id_2 = update_items.player_id_2
        return _GAMES_STORAGE[id]
