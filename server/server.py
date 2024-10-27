import asyncio
import logging
from websockets.asyncio.server import serve

logging.basicConfig(
    format="%(message)s",
    level=logging.DEBUG,
)

async def echo(websocket):
    async for message in websocket:
        await websocket.send(message)

async def main():
    async with serve(echo, "127.0.0.1", 8080):
        await asyncio.get_running_loop().create_future()  # run forever

asyncio.run(main())


