from models.User import User
from resources.results import results_handler, parseJSON
import json

room_data = {
    "state": "WAITING_PLAYERS",
    "message": "",
    "players": [],
    "waitingRoom": [],
    "cellMatrix": [],
    "currentPlayer": None,
    "nextPlayer": None,
    "isGameOver": False,
    "winner": None
}


class Room():

    @staticmethod
    def add_player_to_room(sid):
        global room_data

        new_player = User(sid)
        socket_status = -1

        if len(room_data["players"]) <= 1:
            print(f"Adding socket to players array")

            if len(room_data["players"]) == 0:
                new_player.set_position(1)
            else:
                new_player.set_position(2)
                room_data["state"] = "PLAYER_1_TURN"

            room_data["players"].append(new_player.get_player_dictionary())
            socket_status = 1

        else:
            print("Game Room is full, adding socket to waiting room...")
            new_player.set_position(0)
            room_data["waitingRoom"].append(new_player.get_player_dictionary())
            socket_status = 0

        room_data["message"] = f"Socket {sid} has joined the room =)"
        print("\nroom_data:\n")
        print(json.dumps(room_data, sort_keys=True, indent=4))

        return socket_status

    @staticmethod
    def get_player_position(sid):
        player_position = [
            player["position"] for player in room_data["players"] if player["id"] == sid][0]

        return player_position

    @staticmethod
    def handle_turn_results(data):
        global room_data

        current_player = data["currentPlayer"]
        next_player = data["nextPlayer"]
        cell_id = data["cellId"]
        cell_coordinates = data["cellCoordinates"]

        print("Data from Client:")
        print(json.dumps(data, sort_keys=True, indent=4))

        total_moves = [player["total_moves"]
                       for player in room_data["players"] if player["position"] == 1][0]

        rows_matrix = [
            player["moves_matrix"] for player in room_data["players"] if player["position"] == current_player
        ][0]

        row = cell_coordinates[0]
        column = cell_coordinates[1]

        rows_matrix[row - 1].append(column)
        total_moves.append([row, column])

        # Sorting elements inside each ROW:
        list(map(lambda row: row.sort(), rows_matrix))

        print(f"\n<<< Results Validation for Player [{current_player}] >>>\n")

        is_game_over = results_handler(rows_matrix, total_moves)
        room_data["isGameOver"] = is_game_over

        print(
            f"\n<<< End of Results Validation for Player [{current_player}]\n")

        render_cell_data = {"cellToFill": cell_id,
                            "currentPlayer": current_player}
        room_data["cellMatrix"].append([row, column])

        if room_data["isGameOver"] == True:
            room_data["state"] = "GAME_OVER"
            room_data["message"] = f"Game Over!\nPlayer {current_player} has won!"
            room_data["winner"] = current_player

            room_data = {
                "state": "WAITING_PLAYERS",
                "message": "",
                "players": [],
                "waitingRoom": [],
                "cellMatrix": [],
                "currentPlayer": None,
                "nextPlayer": None,
                "isGameOver": False,
                "winner": None
            }

        else:
            room_data["state"] = f"PLAYER_{next_player}_TURN"

        return parseJSON(render_cell_data)

    @staticmethod
    def get_room_data():
        global room_data
        return parseJSON(room_data)

    @staticmethod
    def remove_user_from_list(sid, socket_status):
        if socket_status == 1:
            for i in range(len(room_data["players"])):
                if room_data["players"][i].get("id") == sid:
                    del(room_data["players"][i])
                    break
                elif socket_status == 0:
                    for i in range(len(room_data["waitingRoom"])):
                        if room_data["waitingRoom"][i].get("id") == sid:
                            del(room_data["waitingRoom"][i])
                            break

        room_data["message"] = f"Socket [{sid}] have disconnected =("
        data = json.dumps(room_data, sort_keys=True, indent=4)
        print(data)
