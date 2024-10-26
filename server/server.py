# import asyncio
# import logging
# from websockets.asyncio.server import serve
#
# logging.basicConfig(
#     format="%(message)s",
#     level=logging.DEBUG,
# )
#
# async def echo(websocket):
#     async for message in websocket:
#         await websocket.send(message)
#
# async def main():
#     async with serve(echo, "127.0.0.1", 8080):
#         await asyncio.get_running_loop().create_future()  # run forever
#
# asyncio.run(main())

from http.server import BaseHTTPRequestHandler, HTTPServer
import json

class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        message = post_data.decode('utf-8')
        print(f"Received message: {message}")

        response = {"status": "success", "message": f"You sent: {message}"}
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())


def run_server(port=8080):
    with HTTPServer(('', port), RequestHandler) as httpd:
        print(f"Serving on port {port}")
        httpd.serve_forever()


if __name__ == "__main__":
    run_server()
