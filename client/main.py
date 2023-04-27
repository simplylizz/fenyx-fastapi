import argparse
import json

import requests

BASE_URL = "localhost:8000"


def format_game(fields):
    for i, row in enumerate(fields):
        for j, cell in enumerate(row):
            if cell is None:
                fields[i][j] = " "
                
    return f'''
            {fields[0][0]} | {fields[0][1]} | {fields[0][2]}
            {fields[1][0]} | {fields[1][1]} | {fields[1][2]}
            {fields[2][0]} | {fields[2][1]} | {fields[2][2]}
            '''
    

def check_response(response) -> bool:
    if response.status_code >= 400:
        print(f"Got response {response.status_code}: {response.text}")
        return False
    return True


def parse_args():
    # sys.argv

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "action",
        choices=[
            "list-games",
            "create-game",
            "make-move",
            "register-player",
            "join-game",
        ],
        help="Action to perform",
    )
    return parser.parse_args()


def list_games():
    response = requests.get(
        f"http://{BASE_URL}/list-games/",
    )
    if not check_response(response):
        return

    data = response.json()
    
    for game in data["games"]:
        cells = format_game(game["field"])
        del game["field"]
        print(json.dumps(game, indent=4))
        print(cells)
        print("--------------------------------")
        
        
        


def create_game():
    player_id = input("Player ID: ")
    response = requests.post(f"http://{BASE_URL}/create-game/", json={"player_id": player_id})
    if not check_response(response):
        return

    game = response.json()
    cells = format_game(game["field"])
    del game["field"]
    print(json.dumps(game, indent=4))
    print(cells)
    print("--------------------------------")
    # print(response.json())


def make_move():
    game_id = input("Game ID: ")
    row = int(input("Row: "))
    col = int(input("Col: "))
    player_id = input("Player ID: ")

    response = requests.post(
        f"http://{BASE_URL}/game/{game_id}/move/",
        json={
            "row": row,
            "col": col,
            "player_id": player_id,
        },
    )
    if not check_response(response):
        return

    print(response.json())


def register_player():
    name = input("Name: ")
    response = requests.post(
        f"http://{BASE_URL}/player/",
        json={
            "name": name,
        },
    )
    if not check_response(response):
        return

    print(response.json())


def join_game():
    game_id = input("Game ID: ")
    player_id = input("Player ID: ")
    response = requests.post(
        f"http://{BASE_URL}/join-game/",
        json={
            "game_id": game_id,
            "player_id": player_id
        },
    )
    if not check_response(response):
        return

    print(response.json())

def main():
    args = parse_args()

    if args.action == "list-games":
        list_games()
    elif args.action == "create-game":
        create_game()
    elif args.action == "make-move":
        make_move()
    elif args.action == "register-player":
        register_player()
    elif args.action == "join-game":
        join_game()
    else:
        raise ValueError(f"Unknown action: {args.action}")


if __name__ == "__main__":
    main()
