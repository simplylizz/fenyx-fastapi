from fastapi import FastAPI
from fastapi import HTTPException

import storage
import schemas


app = FastAPI()


@app.get("/list-games/")
async def list_games():
    return {
        "games": storage.get_games(),
    }


@app.post("/register-as-a-player/")
async def register_as_a_player(player_id_1: str, player_id_2: str):
    return storage.register_player(player_id_1, player_id_2)


@app.put("/update-existing-users/{game_id}")
async def update_existing_users(game_id: int):
    return storage.update_existing_users(game_id)


@app.post("/create-game/")
async def create_game():
    return storage.create_game()


def check_winner(game: dict) -> str | None:
    """
    >>> check_winner({
    ...     "field": [
    ...         ["x", "x", "x"],
    ...         [None, None, None],
    ...         [None, None, None],
    ...     ],
    ... })
    'x'
    >>> check_winner({
    ...     "field": [
    ...         [None, None, None],
    ...         ["o", "o", "o"],
    ...         [None, None, None],
    ...     ],
    ... })
    'o'
    """
    field = game["field"]
    for row in field:
        if row[0] == row[1] == row[2] and row[0] is not None:
            game["status"] = "finished"
            return row[0]

    for col in range(3):
        if (
            field[0][col] == field[1][col] == field[2][col]
            and field[0][col] is not None
        ):
            game["status"] = "finished"
            return field[0][col]

    if field[0][0] == field[1][1] == field[2][2] and field[0][0] is not None:
        game["status"] = "finished"
        return field[0][0]

    elif field[0][2] == field[1][1] == field[2][0] and field[0][2] is not None:
        game["status"] = "finished"
        return field[0][2]

    else:
        game["status"] = "DRAW"
        return "x&o"


@app.put("/update-existing-score/{id}")
def update_existing_score(id: int):
    game = storage.get_game(id)
    if check_winner == "x":
        game['player_score_1'] += 1

    elif check_winner == "o":
        game['player_score_2'] += 1

    elif check_winner == "x&o":
        game['player_score_1'] += 0.5
        game['player_score_2'] += 0.5

    else:
        pass


@app.post('/show-scores/')
async def show_scores():
    return storage.show_scores()


@app.put("/update-existing-users/{game_id}")
async def update_existing_users(game_id: int):
    return storage.update_existing_users(game_id)


# no need to mention player id to make a move we will use this function to check if the player id is entered


@app.post("/game/{game_id}/move/")
async def make_move(game_id: int, move: schemas.Move):
    game = storage.get_game(game_id)

    if game is None:
        raise HTTPException(status_code=404, detail="Game not found")

    if game["status"] != "new":
        raise HTTPException(status_code=400, detail="Game is not new")

    if game["player_id_1"] == "":
        raise HTTPException(
            status_code=400, detail="player_1 id has not been entered")

    if game["player_id_2"] != "":
        raise HTTPException(
            status_code=400, detail="player_2 id has not been entered")

    if game["field"][move.row][move.col] is not None:
        raise HTTPException(status_code=400, detail="Cell is not empty")

    if game["current_move"] != move.player:
        raise HTTPException(status_code=400, detail="Wrong player")

    game["current_move"] = "x" if move.player == "o" else "o"
    game["field"][move.row][move.col] = move.player

    winner = check_winner(game)

    storage.update_game(game_id, game)

    resp = {"status": "ok"}
    if winner is not None:
        resp["winner"] = winner

    return resp


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
