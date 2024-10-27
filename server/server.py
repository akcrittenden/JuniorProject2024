import asyncio
import logging
from websockets.asyncio.server import serve

ingredients = "SALT, SUGAR, SPICES, SOY, WHEAT"

logging.basicConfig(
    format="%(message)s",
    level=logging.DEBUG,
)

# async def echo(websocket):
#     async for message in websocket:
#         await websocket.send(message)

async def server_handler(websocket):
    async for message in websocket:
        if message[0] == "1":
            upc = message[1:]
            # find upc in local database
            # if not found, return some error (if "totalHits" == 0)
            await websocket.send(ingredients)

# do as much as we can back here - for Alpha, do the string comparing here

async def main():
    async with serve(server_handler, "127.0.0.1", 8080):
        await asyncio.get_running_loop().create_future()  # run forever

asyncio.run(main())


