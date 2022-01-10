# pyright: reportGeneralTypeIssues=false
from asyncio import get_event_loop
from websockets import serve
from http.server import BaseHTTPRequestHandler, HTTPServer
from requests import get
from threading import Thread

HOST = 'localhost'
WS_PORT = 8081
HTTP_PORT = 8082
clients = []
proxy_source: bytes

class Handler(BaseHTTPRequestHandler) :
        def do_HEAD(self):
            self.send_response(200)    
        def do_GET(self) :
            if self.path == "/":
                self.send_response(200)
                self.send_header('Content-Type', 'text/html')
                self.send_header('Cache-Control', 'no-cache')
                self.send_header("Content-Length", str(len(proxy_source)))
                self.end_headers()
                self.wfile.write(proxy_source)
            else:
                self.send_error(404)

async def proxy(websocket, path: str):
    print("client connected")
    clients.append(websocket)
    ## listen to websocket client until it closesw
    try:
        while websocket.open:
            frame: bytes = await websocket.recv()
            if len(frame) == 0:
                continue
            # dispatch to other clients
            cs = clients.copy() # avoid races
            for client in cs:
                if client != websocket:
                    await websocket.send(frame)
    finally:
        # remove from clients
        print("client disconnected")
        clients.remove(websocket)
        
# get proxy source
resp = get('https://microsoft.github.io/jacdac-docs/devtools/proxy')
if not resp.ok:
    raise RuntimeError("proxy download failed")

print("proxy downloaded")
proxy_source = resp.text.encode('utf-8')

def web():
    print("local web: http://localhost:8082")
    http_server = HTTPServer( (HOST, HTTP_PORT), Handler )
    http_server.serve_forever()

def ws():
    # start web socket server
    print("websockets: ws://localhost:8081")
    ws_server = serve(proxy, HOST, WS_PORT)
    get_event_loop().run_until_complete(ws_server)
    get_event_loop().run_forever()

# start http server
thread = Thread(target = web)
thread.start()

# start http server
ws()
