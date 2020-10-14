from aiohttp import web
import socketio
import json

app = web.Application()
io = socketio.AsyncServer(cors_allowed_origins=[])
io.attach(app)

routes = web.RouteTableDef()


# # Variables:
socket_status = 0
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


@io.event
async def connect(sid, environ):

    global socket_status

    print("\n<<< New Socket Connected! >>>\n")
    print(f"[io.on('connect') - new socket with id [{sid}]")

    new_player = {
        "id": sid,
        "moves_matrix": [
            [0, 1],  # row 1
            [2, 1],  # row 2
            [2, 0, 1]  # row 3
        ],
        "position": None
    }

    if len(room_data["players"]) <= 1:
        print(f"Adding socket to players array")

        if len(room_data["players"]) == 0:
            new_player["position"] = 1
        else:
            new_player["position"] = 2
            room_data["state"] = "PLAYER_1_TURN"

        room_data["players"].append(new_player)
        socket_status = 1
    else:
        print("Game Room is full, adding socket to waiting room...")
        new_player["position"] = 0
        room_data["waitingRoom"].append(new_player)
        socket_status = 0

    room_data["message"] = f"Socket {sid} has joined the room =)"
    print("\nroom_data:\n")
    print(json.dumps(room_data, sort_keys=True, indent=4))
    print("<<<  >>>\n ")

    await io.emit('whoAmI', new_player["position"], room=sid)
    await io.emit('roomData', room_data)


@io.on("selectCell")
def handle_selected_cell(sid, data):
    current_player = data["currentPlayer"]
    next_player = data["nextPlayer"]
    cell_id = data["cellId"]
    cell_coordinates = data["cellCoordinates"]

    print("\n<<< Results Validation for Player [%s] >>>\n", current_player)
    player_moves_matrix = [
        player["moves_matrix"] for player in room_data["players"] if player["position"] == current_player
    ][0]

    # Sorting elements inside each row:
    list(map(lambda row: row.sort(), player_moves_matrix))

    print("Moves Matrix Sorted:")
    print(player_moves_matrix)

    for i in range(3):
        # FIRST CHECK ===> check whether the player have completed any ROW:
        if len(player_moves_matrix[i]) == 3:
            room_data["isGameOver"] = True
            break
        else:
            # SECOND CHECK ===> check for any COLUMN completion, for a fixed ROW:
            temp_cols_array = []
            for j in range(3):
                temp_cols_array.append(player_moves_matrix[j][i])

            print("temp_cols_array:")
            print(temp_cols_array)

            # Checking if we are getting all elements allign in the columns:
            game_over_for_column_completed = len(temp_cols_array) == 3 and len(set(temp_cols_array)) = 1

            if game_over_for_column_completed == True:
                room_data["isGameOver"] = True
                break

    print("\n<<< End of Results Validation for Player [%s]\n", currentPlayer)

    if room_data["isGameOver"] == True:
        room_data["state"] = "GAME_OVER"
        room_data["message"] = f"Game Over!\nPlayer {current_player} has won!"
        room_data["winner"] = current_player
    else:
        room_data["state"] = f"PLAYER_{next_player}_TURN"

    render_cell_data = {"cellToFill": cell_id, "currentPlayer": current_player}

    await io.emit("roomData", room_data)
    await io.emit("fillCell", render_cell_data)


@io.event
async def disconnect(sid):
    print("\n<<<Disconnecting Socket >>>\n")

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
    print("<<<  >>>\n ")

    await io.emit(room_data)


@routes.get("/")
async def index(request):
    return web.Response(text="<h1>Server Running</h1>", content_type="text/html")

app.add_routes(routes)


if __name__ == "__main__":
    web.run_app(app, port=5000)
