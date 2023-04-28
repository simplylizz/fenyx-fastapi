import argparse
import json

import requests

BASE_URL = "localhost:8000"


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
            "players"
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
    print(json.dumps(data, indent=4))


def list_players():
    response = requests.get(
        f"http://{BASE_URL}/player-scores/",
    )
    if not check_response(response):
        return

    data = response.json()
    print(json.dumps(data, indent=4))


def create_game():
    response = requests.post(f"http://{BASE_URL}/create-game/")
    if not check_response(response):
        return

    data = response.json()
    print(json.dumps(data, indent=4))


def register_player():
    response = requests.post(f"http://{BASE_URL}/register-player/")
    if not check_response(response):
        return
    
    data = response.json()
    print(json.dumps(data, indent=4))


def print_game_field(game_field):
    print(f"{game_field[0][0]}|{game_field[0][1]}|{game_field[0][2]}")
    print("-+-+-")
    print(f"{game_field[1][0]}|{game_field[1][1]}|{game_field[1][2]}")
    print("-+-+-")
    print(f"{game_field[2][0]}|{game_field[2][1]}|{game_field[2][2]}")


def make_move():
    game_id = int(input("Game ID: "))
    player_id = int(input("Player ID: "))
    player_side = input("Choose your side (x|o): ")
    
    while True:
        try:
            player = input("Player (x|o): ")
            row = int(input("Row: "))
            col = int(input("Col: "))
            
            response = requests.post(
                f"http://{BASE_URL}/game/{game_id}/move/",
                json={
                    "row": row,
                    "col": col,
                    "player": player,
                    "player_id": player_id,
                    "player_side": player_side
                },
            )
            
            
            if not check_response(response):
                return

            print(response.json())
            
            # # Check the response from the server
            if check_response(response) is True:
                result = response.json()
                print_game_field(result["field"])

                if result['status'] == 'finished' and result['winner'] is not None:
                    print(f"Player {result['winner']} wins!")
                    break
                elif result['status'] == 'finished' and result['winner'] == "tied":
                    print("The game is tied!")
                    break
            else:
                print("Invalid move. Please try again.")
                
        except KeyboardInterrupt:
            # Exit gracefully if the user hits Ctrl+C
            print("Exiting...")
            break


def join_game():
    game_id = int(input("Enter game id to join existing game: "))
    player_id = int(input("Enter your player id: "))
    
    response = requests.post(
                f"http://{BASE_URL}/game/{game_id}/join-game/",
                json={"player_id": player_id})
    
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
    elif args.action == "players":
        list_players()
    else:
        raise ValueError(f"Unknown action: {args.action}")


if __name__ == "__main__":
    main()
