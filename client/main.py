import argparse
import json
import requests


BASE_URL = "localhost:8000"


def check_response(response):
    if response.status_code >= 400:
        print(f"Got response {response.status_code}: {response.text}")
        return False
    return True


def print_field(field):
    for row in field:
        row_str = ""
        for cell in row:
            if cell is None:
                row_str += " "
            else:
                row_str += cell
            row_str += "|"
        print(row_str[:-1])


def list_games():
    response = requests.get(
        f"http://{BASE_URL}/list-games/",
    )
    if not check_response(response):
        return

    data = response.json()
    print(json.dumps(data, indent=4))


def create_game():
    response = requests.post(f"http://{BASE_URL}/create-game/")
    if not check_response(response):
        return

    print(response.json())

def make_move():
    game_id = int(input("Game ID: "))
    player_id = input("Player ID: ")
    player = input("Player: ")
    row = int(input("Row: "))
    col = int(input("Col: "))

    response = requests.post(
        f"http://{BASE_URL}/game/{game_id}/move/?player_id={player_id}",
        json={
            "player": player,
            "row": row,
            "col": col,
        },
    )
    if not check_response(response):
        return

    print(response.json())

def join_game():
    game_id = int(input("Game ID: "))
    player_id = input("Player ID: ")

    response = requests.post(
        f"http://{BASE_URL}/game/{game_id}/join/?player_id={player_id}",
    )
    if not check_response(response):
        return

    print(response.json())


def register_player():
    player_name = input("Player name: ")

    response = requests.post(
        f"http://{BASE_URL}/register-player/",
        json={
            "name": player_name,
        },
    )
    if not check_response(response):
        return

    print(response.json())
def get_players():
    response = requests.get(
        f"http://{BASE_URL}/get-players/",
    )
    if not check_response(response):
        return

    data = response.json()
    print(json.dumps(data, indent=4))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "action",
        choices=[
            "list-games",
            "create-game",
            "join-game",
            "register-player",
            "get-players",
            "make-move",
        ],
        help="Action to perform",
    )
    args = parser.parse_args()

    if args.action == "list-games":
        list_games()
    elif args.action == "create-game":
        create_game()
    elif args.action == "join-game":
        join_game()
    elif args.action == "register-player":
        register_player()
    elif args.action == "get-players":
        get_players()
    elif args.action == "make-move":
        make_move()
    else:
        raise ValueError(f"Unknown action: {args.action}")


if __name__ == "__main__":
    main()