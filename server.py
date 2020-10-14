from aiohttp import web
import socketio
import json

app = web.Application()
sio = socketio.AsyncServer(cors_allowed_origins=[])
sio.attach(app)

routes = web.RouteTableDef()


users_dic_list = []


@routes.get("/")
async def index(request):
    return web.Response(text="<h1>Server Running</h1>", content_type="text/html")


@sio.event
async def connect(sid, environ):
    print("\nConnected: ", sid)
    print("...adding user to database\n")
    user_json = {"id": sid}
    users_dic_list.append(user_json)
    data = json.dumps(users_dic_list, sort_keys=True, indent=4)
    print(data)
    await sio.emit('data', data)


@sio.event
async def disconnect(sid):
    print("\nDisconnect ", sid)
    print("...Removing user from database\n")

    for i in range(len(users_dic_list)):
        if users_dic_list[i].get("id") == sid:
            del(users_dic_list[i])
            break
    data = json.dumps(users_dic_list, sort_keys=True, indent=4)
    print(data)


app.add_routes(routes)

if __name__ == "__main__":
    web.run_app(app, port=5000)
