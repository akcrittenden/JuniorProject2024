import asyncio
from collections import namedtuple

import websockets
import socket
import requests
from datetime import datetime
import json
import gzip

api_key = "DEMO_KEY"


# Search USDA Food Central Database for UPC key
async def get_data(search_term):
    # Define search endpoint and parameters
    url = "https://api.nal.usda.gov/fdc/v1/foods/search"

    # Create search parameter dictionary
    params = {
        "api_key": api_key,
        "query": search_term,
        "dataType": "Branded",
        "pageSize": 5,  # Number of results per page
    }

    try:
        # Make a GET request to the API endpoint & store response
        response = requests.get(url, params=params)

        # Print URL for debugging purposes
        print(f"{get_timestamp()} - {response.url}")

        # Check if the request was successful
        # Print status code if fail
        if response.status_code == 200:
            return response.json()
        else:
            print(f"{get_timestamp()} - Error: {response.status_code}")
            format_fun()
            return None

    # Network related error
    except requests.exceptions.RequestException as e:
        print(f"{get_timestamp()} - Error: {e}")
        format_fun()
        return None


# Receive incoming UPC key from client & send back description/ingredients
async def websocket_connection(websocket):
    try:
        # Wait for a message from the client
        search_term = str(await websocket.recv())

        if search_term == "":
            print(f"UPC empty")
            await websocket.send("Please enter a search term")
        else:
            print(f"{get_timestamp()} - Received {search_term}")

            # Search USDA database and print returned data
            data = await get_data(search_term)
            print_data(data)

            """
            # Send the search results back to the client STRING FORM
            ingredients = str(data["foods"][0].get("ingredients", "No ingredients found"))
            await websocket.send(ingredients)
            """

            # Send the search results back to the client JSON FORM
            new_data = {
                "description": data["foods"][0].get(
                    "description", "No description found"
                ),
                "brandName": data["foods"][0].get("brandName", "No brand name found"),
                "brandOwner": data["foods"][0].get(
                    "brandOwner", "No brand owner found"
                ),
                "foodCategory": data["foods"][0].get(
                    "foodCategory", "No category found"
                ),
                "ingredients": data["foods"][0].get(
                    "ingredients", "No ingredients found"
                ),
            }
            await websocket.send(json.dumps(new_data))

    # No product data returned from USDA database
    except Exception as e:
        print(f"{get_timestamp()} - Error: {e}")
        format_fun()
        await websocket.send("Product Not Found")


# Print formatted product data
def print_data(data):
    if data:
        for food in data["foods"]:
            print(f"Description: {food['description']}")
            print(f"Brand Name: {food['brandName']}")
            print(f"Data Type: {food['dataType']}")
            print(f"Ingredients: {food['ingredients']}")
            format_fun()
    else:
        print(f"{get_timestamp()} - Failed to fetch data from API")


# Formatted timestamp
def get_timestamp():
    return datetime.now().strftime("%H:%M:%S")


# Print listening message to confirm server is active
async def periodic_message():
    while True:
        print(f"{get_timestamp()} - Server is listening")
        format_fun()
        await asyncio.sleep(300)  # 300 seconds = 5 minutes


def format_fun():
    print("-" * 100)


async def main():
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    port = 8765

    # Start WebSocket server
    print(f"{get_timestamp()} - Starting server on {local_ip}:{port}")

    async with websockets.serve(websocket_connection, local_ip, port):

        # ----------------- BELOW IS FOR TED'S SERVER--------------------------
        # host = "0.0.0.0"    # Listen on all network interfaces
        # port = 443          # WSS port
        #
        # # Start WebSocket server
        # print(f"{get_timestamp()} - Starting server on allerscan.tplinkdns.com:{port}")
        #
        # async with websockets.serve(websocket_connection, host, port):
        # ------------------ABOVE IS FOR TED'S SERVER__________________________

        await asyncio.gather(periodic_message())
        await asyncio.Future()  # Run forever


asyncio.run(main())
