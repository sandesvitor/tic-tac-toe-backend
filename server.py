from aiohttp import web
import socketio
from services.Room import Room
from resources.results import results_handler
import json

app = web.Application()
io = socketio.AsyncServer(cors_allowed_origins=[])
io.attach(app)
routes = web.RouteTableDef()

socket_status = -1


@io.event
async def connect(sid, environ):
    global socket_status

    print(f"[io.on('connect') - new socket [{sid}]")

    socket_status = Room.add_player_to_room(sid)

    await io.emit('whoAmI', Room.get_player_position(sid), room=sid)
    await io.emit('roomData', Room.get_room_data())


@io.on("selectCell")
async def handle_selected_cell(sid, data):
    render_cell_data = Room.handle_turn_results(data)

    await io.emit("roomData", Room.get_room_data())
    await io.emit("fillCell", render_cell_data)


@io.event
async def disconnect(sid):
    print(f"[io.on('disconnect') - socket [{sid}] disconnected ")

    Room.remove_user_from_list(sid, socket_status)
    await io.emit(Room.get_room_data())


@routes.get("/")
async def index(request):
    return web.Response(text="<h1>Server Running</h1>", content_type="text/html")

app.add_routes(routes)


if __name__ == "__main__":
    web.run_app(app, port=5000)
