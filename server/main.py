from fastapi import FastAPI
from fastapi import HTTPException
import uvicorn
from typing import Optional
from pydantic import BaseModel
import storage
import schemas


app = FastAPI()


# @app.post("/register-as-a-player/")
# async def register_as_a_player(player_id_1: str, player_id_2: str):
#     return storage.register_player(player_id_1, player_id_2)
###########################################################
###########################################################
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


class new_games(BaseModel):

    id: int
    player_id_1: (str) = ""
    player_id_2: (str) = ""
    status: str = "new"
    current_move: str = "x"
    player_score_1: float = 0
    player_score_2: float = 0
    field = [
        ["", "", ""],
        ["", "", ""],
        ["", "", ""],
    ]


@app.post('/create-item/{game_id}')
def add_new_item(game_id: int, new_games: new_games):
    if game_id in _GAMES_STORAGE:
        raise HTTPException(
            status_code=404, detail=f"the id {game_id} already exists")

    _GAMES_STORAGE[game_id] = new_games
    return _GAMES_STORAGE[game_id]


@app.get("/get-game/{game_id}")  # item_id is called path parameter
# path gives a description of the path parameter
# gt  lt ge and le :make restrictions on the path parameter to be in a specific interval gives 422 error
def get_game(game_id: int):
    if game_id in _GAMES_STORAGE:
        return _GAMES_STORAGE[game_id]
    raise HTTPException(
        status_code=404, detail=f"no game with  id {game_id} ")


class update_item(BaseModel):
    player_id_1: Optional[str] = None
    player_id_2: Optional[str] = None


@app.put("/update-existing-users/{game_id}")
def update_existing_users(game_id: int, update_item: update_item):

    if game_id not in _GAMES_STORAGE:
        raise ValueError(f"No game with game_id {game_id}")
    elif (_GAMES_STORAGE[game_id].player_id_1 != "" and _GAMES_STORAGE[game_id].player_id_2 != ""):
        raise ValueError(f"game with game_id {game_id}  is full")

    else:
        if update_item.player_id_1 != None:
            _GAMES_STORAGE[game_id].player_id_1 = update_item.player_id_1
        if update_item.player_id_2 != None:
            _GAMES_STORAGE[game_id].player_id_2 = update_item.player_id_2
        return _GAMES_STORAGE[game_id]


def check_winner(game_id, game: dict) -> str | None:
    """ 
    >>> check_winner({
    ...     "field": [
    ...         ["x", "x", "x"],
    ...         [", ", "],
    ...         [", ", "],
    ...     ],
    ... })
    'x'
    >>> check_winner({
    ...     "field": [
    ...         ["", "", ""],
    ...         ["o", "o", "o"],
    ...         ["", "", ""],
    ...     ],
    ... })
    'o'
    """
    game = get_game(game_id)
    field = game.field
    for row in field:
        if row[0] == row[1] == row[2] and row[0] != "":
            game.status = "finished"
            return row[0]

    for col in range(3):
        if (
            field[0][col] == field[1][col] == field[2][col]
            and field[0][col] != ""
        ):
            game.status = "finished"
            return field[0][col]

    if field[0][0] == field[1][1] == field[2][2] and field[0][0] != "":
        game.status = "finished"
        return field[0][0]

    elif field[0][2] == field[1][1] == field[2][0] and field[0][2] != "":
        game.status = "finished"
        return field[0][2]
    elif all(flag != "" for (_, _, flag) in field) and game.status != "finished":
        game.status = "DRAW"
        return "x&o"
    else:
        game.status = "Ongoing"


@app.get('show-scores')
def show_scores():
    score_list = []
    last_list = []
    for game_id in _GAMES_STORAGE:
        for game_id.player_score_1 in _GAMES_STORAGE and game_id.player_score_2 in _GAMES_STORAGE:
            score_list.append(game_id.player_score_1, game_id.player_score_2)
            score_list.sort(reverse=True)
            n = 0
            for n in range(len(score_list)):

                if score_list[n] == game_id.player_score_1:
                    last_list.append({game_id.player_score_1: score_list[n]})
                    print({game_id.player_score_1: score_list[n]})

                elif score_list[n] == game_id.player_score_2:
                    last_list.append({game_id.player_score_1: score_list[n]})

                    print({game_id.player_score_2: score_list[n]})
                else:
                    pass
                n += 1
            return last_list.json.dumps()


def update_existing_score(game_id: int):
    game = get_game(game_id)
    if check_winner(game_id, game) == "x":
        game.player_score_1 += 1
        return game.player_score_1

    elif check_winner(game_id, game) == "o":
        game.player_score_2 += 1
        return game.player_score_2

    elif check_winner(game_id, game) == "x&o":
        game.player_score_1 += 0.5
        game.player_score_2 += 0.5
        return game.player_score_1, game.player_score_2

    else:
        pass


def update_game(game_id: int, data: dict):
    if game_id not in _GAMES_STORAGE:
        raise ValueError(
            f"No game with id {game_id}")

    _GAMES_STORAGE[game_id] = data


@app.post('/show-scores/')
async def show_scores():
    return storage.show_scores()


class update_items(BaseModel):
    player_id_1: Optional[str] = None
    player_id_2: Optional[str] = None


# @app.put("/update-existing-users/{game_id}")
# def update_existing_users(game_id: int, update_items: update_items):

#     if id not in _GAMES_STORAGE:
#         raise ValueError(f"No game with id {game_id}")
#     elif (_GAMES_STORAGE[game_id].player_game_id_1 != "" and _GAMES_STORAGE[game_id].player_game_id_2 != ""):
#         raise ValueError(f"game with game_id {game_id}  is full")

#     else:
#         if update_items.player_game_id_1 != None:
#             _GAMES_STORAGE[game_id].player_game_id_1 = update_items.player_game_id_1
#         if update_items.player_game_id_2 != None:
#             _GAMES_STORAGE[game_id].player_game_id_2 = update_items.player_id_2
#         return _GAMES_STORAGE[game_id]


# no need to mention player id to make a move we will use this function to check if the player id is entered


@app.post("/game/{game_id}/move/")
async def make_move(game_id: int, move: schemas.Move):
    game = get_game(game_id)

    if game is None:
        raise HTTPException(status_code=404, detail="Game not found")

    # if game.status != "new":
    #     raise HTTPException(status_code=400, detail="Game is not new")

    if game.player_id_1 == "":
        raise ValueError(f" please enter player id_1 first")

    if game.player_id_2 == "":
        raise ValueError(f" please enter player id_2 first")

    if game.field[move.row][move.col] == "x" or game.field[move.row][move.col] == "o":
        raise HTTPException(status_code=400, detail="Cell is not empty")

    if game.current_move != move.player:
        raise HTTPException(status_code=400, detail="Wrong player")

    game.current_move = "x" if move.player == "o" else "o"
    game.field[move.row][move.col] = move.player

    winner = check_winner(game_id, game)

    update_game(game_id, game)
    update_existing_score(game_id)

    resp = {"status": "ok"}
    if winner is not None:
        resp["winner"] = winner

    return resp


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
