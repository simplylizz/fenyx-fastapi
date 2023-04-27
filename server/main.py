import json
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


@app.post("/create-game/")
async def create_game(data: dict):
    return storage.create_game(data["player_id"])

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

    if field[0][2] == field[1][1] == field[2][0] and field[0][2] is not None:
        game["status"] = "finished"
        return field[0][2]

    draw_flag = True
    for row in field:
        for cell in row:
            if cell is None:
                draw_flag = False
    if draw_flag:
        game["status"] = "finished"
        return "draw"
    
    return None


@app.post("/game/{game_id}/move/")
async def make_move(game_id: str, move: schemas.Move):
    game = storage.get_game(game_id)
    
    if game is None:
        raise HTTPException(status_code=404, detail="Game not found")

    # if game["status"] != "new":
    #     raise HTTPException(status_code=400, detail="Game is not new")

    if game["field"][move.row][move.col] is not None:
        raise HTTPException(status_code=400, detail="Cell is not empty")

    if game["last_move_player_id"] == move.player_id:
        raise HTTPException(status_code=400, detail="Wrong player")

    game["last_move_player_id"] = game["player_x"] if move.player_id == game["player_x"] else game["player_o"]
    if move.player_id == game["player_x"]:
        game["field"][move.row][move.col] = "x"
    elif move.player_id == game["player_o"]:
        game["field"][move.row][move.col] = "o"
    else:
        raise HTTPException(status_code=400, detail="Player not in this game.")
    
    

    winner = check_winner(game)

    storage.update_game(game_id, game)

    resp = {"status": "ok"}
    if winner == "x":
        resp["winner"] = "player_x"
        storage.update_wins(game["player_x"], 1)
    elif winner == "o":
        resp["winner"] = "player_o"
        storage.update_wins(game["player_o"], 1)
    elif winner == "draw":
        resp["winner"] = "draw"
        storage.update_wins(game["player_x"], 0.5)
        storage.update_wins(game["player_o"], 0.5)

    return resp


@app.post("/player/")
def register_player(player: schemas.Player):
    storage.register_player(player)
    return player


@app.post("/join-game/")
def join_game(jg: schemas.JoinGame):
    game = storage.get_game(jg.game_id)
    if game is None:
        raise ValueError(f"No game with id {jg.game_id}")
    if game["status"] != "new":
        raise ValueError(f"Game is not new")

    if game["player_x"] != jg.player_id:
        game["player_o"] = jg.player_id
        game["status"] = "started"
        storage.update_game(jg.game_id, game)
        return game


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
