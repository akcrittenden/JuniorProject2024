import asyncio
import logging
from collections import namedtuple

from websockets.asyncio.server import serve

# not quite a struct b/c no types or methods
# can call like user_list[0].allergen
allergen = namedtuple("allergen", ["allergen", "severity"])

"""
small testing database to search against -
so we can do like ""SALT" in local_database['soyandwheat']" and
it returns true or false
TO DO - get severity pushed as well - can we do if "SALT" in local_database['soyandwheat'] == true, 
return userlist.allergen.severity that contains salt?
"""
ingredients = "SALT, SUGAR, SPICES, SOY, WHEAT"

local_database = {
    "FrenchFries": ["SALT", "SUGAR", "SPICES", "SOY", "WHEAT"],
    "soySauce": ["SALT, SOY, SUGAR, MILK"],
    "GlutenFreeCookies": ["SALT, SUGAR, CHOCOLATE"],
}

user_list = [
    allergen(allergen="WHEAT", severity="SEVERE"),
    allergen(allergen="SOY", severity="MILD"),
]  # ingredient allergic to, severity, so we can do like user_list[0].allergen


# get ingredients from UPC, return as string
def get_ingredients(upc: int) -> list[str]:
    pass


# get user allergens
def get_allergens(user_id: int) -> tuple[tuple[str, str]]:
    pass


# any([allergen[0] in local_database["soyandwheat"] for allergen in user_list])

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
            await websocket.send(
                ingredients
            )  # return object maybe? allergens if detected and their severity


# do as much as we can back here - for Alpha, do the string comparing here


async def main():
    async with serve(server_handler, "127.0.0.1", 8080):
        await asyncio.get_running_loop().create_future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())
