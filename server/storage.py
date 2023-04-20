import copy
import uuid


_GAMES_STORAGE = {
    1: {
        "id": 1,
        "player_id_1": "",
        "player_id_2": "",
        "status": "new",
        "current_move": "x",
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


def update_game(id: int, data: dict):
    if id or player_id_1 or player_id_2 not in _GAMES_STORAGE:
        raise ValueError(f"No game with id {id}")

    _GAMES_STORAGE[id] = data


def join_existing_games(game_id):
    if game_id not in _GAMES_STORAGE:
        raise ValueError(
            f"No game with id {game_id} ")
    elif (player_id_1 != "" and player_id_2 != ""):
        raise ValueError(f"game with id {game_id}  is full")

    else:
        print("you can join this game ")
        if player_id_1:
            player_id_2 = input("pleaser enter the id")
            _GAMES_STORAGE[player_id_2]
        elif player_id_2:
            player_id_2 = input("pleaser enter the id")
            _GAMES_STORAGE[player_id_2]
        else:
            pass
