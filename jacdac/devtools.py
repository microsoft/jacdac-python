from asyncio import get_event_loop
from websockets import websocket, serve
from http.server import BaseHTTPRequestHandler, HTTPServer

PORT = 8081
clients: List[Web] = []

class Handler(BaseHTTPRequestHandler) :
        def do_GET(s) :

                print('-----------------------')
                print('GET %s (from client %s)' % (s.path, s.client_address))
                print(s.headers)
                super(Handler, s).do_GET() #inherited do_GET serves dirs&files.


async def proxy(websocket, path):
    clients.push(websocket)
    ## listen to websocket client until it closesw
    while True:
        frame: bytes = await websocket.recv()
        if (len(frame) == 0) continue
        # dispatch to other clients
        cs = clients.copy() # avoid races
        for client in cs:
            if client != websocket:
                await websocket.send(now)
        
# start web socket server
ws_server = serve(proxy, 'localhost', PORT)
get_event_loop().run_until_complete(ws_server)

# start http server
http_server = HTTPServer( ('', PORT), Handler )
s.serve_forever()
