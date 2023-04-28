from __future__ import annotations
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
async def create_game():
    return {
        "games": storage.create_game()
    }


@app.post('/register-player/')
def register_player():
    return {
        "players": storage.add_player()
    }


def update_score(game):
    if game["winner"] == "o":
        player = storage.get_player(game["player_o"])
        player["score"] += 1
        storage.update_player(player["player_id"], player)    
    elif game["winner"] == "x":
        player = storage.get_player(game["player_x"])
        player["score"] += 1
        storage.update_player(player["player_id"], player)
    elif game["winner"] == "tied":
        player1 = storage.get_player(game["player_x"])
        player2 = storage.get_player(game["player_o"])
        player1["score"] += 0.5
        player2["score"] += 0.5     
        

def check_winner(game: dict) -> str | None:
    """
    >>> check_winner({
    ...     "field": [
    ...         ["x", "x", "x"],
    ...         ["", "", ""],
    ...         ["", "", ""],
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
    field = game["field"]
    for row in field:
        if row[0] == row[1] == row[2] and row[0] != "":
            game["status"] = "finished"
            game["winner"] = "tied"
            return row[0]

    for col in range(3):
        if (
            field[0][col] == field[1][col] == field[2][col]
            and field[0][col] != ""
        ):
            game["status"] = "finished"
            game["winner"] = field[0][col]
            update_score(game)
            return field[0][col]

    if field[0][0] == field[1][1] == field[2][2] and field[0][0] != "":
        game["status"] = "finished"
        game["winner"] = field[0][0]
        update_score(game)
        return field[0][0]

    if field[0][2] == field[1][1] == field[2][0] and field[0][2] != "":
        game["status"] = "finished"
        game["winner"] = field[0][2]
        update_score(game)
        return field[0][2]

    return None


@app.post('/game/{game_id}/join-game/')
async def join_game(game_id: int, player: schemas.Player):
    game = storage.get_game(game_id)
    players = storage.get_player(player.player_id)
    print(players)
    
    player_id = player.player_id
    # val = players.get("player_id")
        
    if player_id == players["player_id"] and player_id != game["player_x"]:
        if game["id"] != game_id:
            raise HTTPException(status_code=404, detail="game not found")
            
        if game["status"] == "waiting":
            game["player_o"] = player_id
            game["status"] = "started"
            storage.update_game(game_id, game)
            return("You are joined to the game! Go to make-move command to start.")
        return {"game": "This game is not available"}
    return {"status": "This player id is not valid!"}
    

@app.post("/game/{game_id}/move/")
async def make_move(game_id: int, move: schemas.Move):
    game = storage.get_game(game_id)
    
    player = storage.get_player(move.player_id)
    
    if move.player_id != game['player_x'] and move.player_id != game['player_o']:
        raise HTTPException(status_code=500, detail="message': 'Invalid player id")
    
    
    if move.player_id == game["player_o"] and move.player_side == 'o':
        game["player_o"] = move.player_id
    elif move.player_id == game["player_o"] and move.player_side == 'x':
        game["player_o"] = game["player_x"]
        game["player_x"] = move.player_id
    elif move.player_id == game["player_x"] and move.player_side == 'x':
        game["player_x"] = move.player_id
    elif move.player_id == game["player_x"] and move.player_side == 'o':
        game["player_x"] = game["player_o"]
        game["player_o"] = move.player_id
    else:
        raise HTTPException(status_code=500, detail="player id mismatch")

    if game is None:
        raise HTTPException(status_code=404, detail="Game not found")
    
    
    if player is None:
        raise HTTPException(status_code=404, detail="player not found")
    
    if player["player_id"] != move.player_id:
        raise HTTPException(status_code=500, detail="player id is wrong!")

    if game["status"] != "started":
        raise HTTPException(status_code=400, detail="Game is not new")

    if game["field"][move.row][move.col] != "":
        raise HTTPException(status_code=400, detail="Cell is not empty")

    if game["current_move"] != move.player:
        raise HTTPException(status_code=400, detail="Wrong player")

    game["current_move"] = "x" if move.player == "o" else "o"
    game["field"][move.row][move.col] = move.player
    # game["player_id"] = move.player_id

    check_winner(game)

    storage.update_game(game_id, game)

    # resp = {"status": "ok"}
    # if winner is not None:
    #     resp["winner"] = winner

    return game


@app.get('/player-scores')
async def player_score():
    players = storage.get_players()
    sorted_players = sorted(players, key=lambda p: p['score'], reverse=True)
    return sorted_players


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
