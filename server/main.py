from typing import Union
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
@app.post("/register-player/")
async def register_player(player_name: str) -> dict:
    player_id = storage.register_player(player_name)
    return {"player_id": player_id}

@app.post("/create-game/")
def create_game(player_id: int) -> dict:
    game = storage.create_game(player_id)
    game["score_x"] = 0
    game["score_o"] = 0
    storage.update_game(game["id"], game)
    return game


@app.post("/join-game/")
def join_game(game_id: int, player_id: int) -> dict:
    game = storage.get_game(game_id)
    if not game:
        return {"error": "Game not found"}
    
    if game["status"] == "started":
        return {"error": "Game has already started"}
    
    if game["status"] == "finished":
        return {"error": "Game has already finished"}
    
    if game.get("player_o"):
        return {"error": "Game is full"}
    
    game["player_o"] = player_id
    game["status"] = "started"
    storage.update_game(game_id, game)
    
    return game

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

    return None


@app.post("/game/{game_id}/move/")
async def make_move(game_id: int, move: schemas.Move, player_id: int) -> dict:
    game = storage.get_game(game_id)

    if game is None:
        raise HTTPException(status_code=404, detail="Game not found")

    if game["status"] != "started":
        raise HTTPException(status_code=400, detail="Game is not started")

    if game["field"][move.row][move.col] is not None:
        raise HTTPException(status_code=400, detail="Cell is not empty")

    if game["current_move"] != move.player:
        raise HTTPException(status_code=400, detail="Wrong player")

    game["current_move"] = "x" if move.player == "o" else "o"
    game["field"][move.row][move.col] = move.player

    winner = check_winner(game)

    if winner is not None:
        game["status"] = "finished"
        if winner == "x":
            game["score_x"] += 1
        elif winner == "o":
            game["score_o"] += 1
        elif winner == "draft":
            game["score_x"] += 0.5
            game["score_o"] += 0.5

    storage.update_game(game_id, game)

    resp = {"status": "ok"}
    if winner is not None:
        resp["winner"] = winner
    return resp

@app.get("/scores/")
async def get_scores():
    players = storage.get_players()
    sorted_players = sorted(players, key=lambda p: p["score"], reverse=True)
    return {"players": sorted_players}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)