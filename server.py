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


@routes.get("/")
async def index(request):
    return web.Response(text="<h1>Server Running</h1>", content_type="text/html")


@io.event
async def connect(sid, environ):

    print("\n<<< New Socket Connected! >>>\n")
    print(f"[io.on('connect') - new socket with id [{sid}]")

    new_player = {
        "id": sid,
        "moves_matix": [
            [],  # row 1
            [],  # row 2
            []  # row 3
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


app.add_routes(routes)

if __name__ == "__main__":
    web.run_app(app, port=5000)
