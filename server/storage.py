import copy

_GAMES_STORAGE = {
    1: {
        "id": 1,
        "status": "new",
        "current_move": "x",
        "field": [
            [None, None, None],
            [None, None, None],
            [None, None, None],
        ],
    },
}


def get_games():
    return list(_GAMES_STORAGE.values())


def create_game():
    id_ = len(_GAMES_STORAGE) + 1

    _GAMES_STORAGE[id_] = {
        "id": id_,
        "status": "new",
        "current_move": "x",
        "field": [
            [None, None, None],
            [None, None, None],
            [None, None, None],
        ],
    }

    return _GAMES_STORAGE[id_]


def get_game(id: int) -> dict | None:
    game = _GAMES_STORAGE.get(id)
    return copy.deepcopy(game)


def update_game(id: int, data: dict):
    if id not in _GAMES_STORAGE:
        raise ValueError(f'No game with id {id}')

    _GAMES_STORAGE[id] = data
