# pyright: reportGeneralTypeIssues=false
# pyright: reportUnknownVariableType=false
# pyright: reportUnknownParameterType=false
# pyright: reportUnknownArgumentType=false
# pyright: reportUnknownMemberType=false
# pyright: reportMissingParameterType=false
from asyncio import get_event_loop
from websockets import serve
from http.server import BaseHTTPRequestHandler, HTTPServer
from requests import get
from threading import Thread
from sys import argv
from jacdac.constants import DEVTOOLS_HTTP_PORT, DEVTOOLS_WS_PORT

print("Jacdac DevTools (Python)")

internet = "--internet" in argv
HOST = '0.0.0.0' if internet else 'localhost'
clients = []
proxy_source: bytes

if internet:
    print("WARNING: server bound to all network interfaces")
else:
    print("use --internet to bind server to all network interfaces")

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
    clients.append(websocket)
    print("client connected (%d clients)" % len(clients))
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
                    try:
                        await client.send(frame)
                    except:
                        print("client receive error")
    except:
        print("client receive error")
    finally:
        # remove from clients
        clients.remove(websocket)
        print("client disconnected (%d clients)" % len(clients))
        
# get proxy source
resp = get('https://microsoft.github.io/jacdac-docs/devtools/proxy')
if not resp.ok:
    raise RuntimeError("proxy download failed")

proxy_source = resp.text.encode('utf-8')

def web():
    print("local web: http://" + HOST + ":" + str(DEVTOOLS_HTTP_PORT))
    http_server = HTTPServer( (HOST, DEVTOOLS_HTTP_PORT), Handler )
    http_server.serve_forever()

def ws():
    # start web socket server
    print("websockets: ws://" + HOST + ":" + str(DEVTOOLS_WS_PORT))
    ws_server = serve(proxy, HOST, DEVTOOLS_WS_PORT)
    get_event_loop().run_until_complete(ws_server)
    get_event_loop().run_forever()

# start http server
thread = Thread(target = web)
thread.daemon = True
thread.start()

# start http server
ws()
