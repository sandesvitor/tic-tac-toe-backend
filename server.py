from aiohttp import web
import socketio
from resources.results import results_handler
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
            [],  # row 1
            [],  # row 2
            []  # row 3
        ],
        "total_moves": [],
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
async def handle_selected_cell(sid, data):

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

    print(f"\n<<< End of Results Validation for Player [{current_player}]\n")

    render_cell_data = {"cellToFill": cell_id, "currentPlayer": current_player}
    room_data["cellMatrix"].append([row, column])

    if room_data["isGameOver"] == True:
        room_data["state"] = "GAME_OVER"
        room_data["message"] = f"Game Over!\nPlayer {current_player} has won!"
        room_data["winner"] = current_player

        await io.emit("roomData", room_data)
        await io.emit("fillCell", render_cell_data)

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
