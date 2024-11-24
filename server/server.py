import asyncio
from collections import namedtuple

import websockets
import requests

api_key = "DEMO_KEY"


# Search USDA Food Central Database with UPC key
async def get_data(search_term):
    # Define search endpoint and parameters
    url = "https://api.nal.usda.gov/fdc/v1/foods/search"

    params = {
        "api_key": api_key,
        "query": search_term,
        "dataType": "Branded",
        "pageSize": 5,  # Number of results per page
    }

    try:
        # Make a GET request to the API endpoint
        response = requests.get(url, params=params)
        print(response.url)

        # Check if the request was successful
        if response.status_code == 200:
            #
            return response.json()
        else:
            print("Error:", response.status_code)
            return None

    # Handle any network-related errors or exceptions
    except requests.exceptions.RequestException as e:
        print("Error:", e)
        return None


# Receive incoming UPC key from client & send back description/ingredients
async def websocket_connection(websocket):
    try:
        # Wait for a message from the client
        search_term = str(await websocket.recv())
        print(f"Received {search_term}")

        # Perform the search in the USDA database
        data = await get_data(search_term)
        print_data(data)

        # Combine ingredients and description into named tuple
        description = str(data["foods"][0].get("description", "No description found"))
        ingredients = str(data["foods"][0].get("ingredients", "No ingredients found"))

        product = namedtuple("Product", ["description", "ingredients"])
        p = product(description, ingredients)

        # Send named tuple back to client
        await websocket.send(p)

    except Exception as err:
        print(f"Error: {err}")
        await websocket.send("An error occurred while processing your request.")


# Print formatted product data
def print_data(data):
    if data:
        for food in data["foods"]:
            print(f"Description: {food['description']}")
            print(f"Brand Name: {food['brandName']}")
            print(f"FDC ID: {food['fdcId']}")
            print(f"Data Type: {food['dataType']}")
            print(f"Ingredients: {food['ingredients']}")
            print("-" * 100)  # format_fun()
    else:
        print("Failed to fetch data from API.")


# Print listening message every 5 minutes to confirm server is running
async def periodic_message():
    while True:
        # print("Server is listening on ws://10.220.8.180:8765")
        print("Server is listening on ws://127.0.0.1:8080")
        print("-" * 100)  # format_fun()
        await asyncio.sleep(300)  # 300 seconds = 5 minutes


async def main():
    # Start WebSocket server
    # async with websockets.serve(websocket_connection, "10.220.8.180", 8765):
    async with websockets.serve(websocket_connection, "127.0.0.1", 8080):
        await asyncio.gather(periodic_message())
        await asyncio.Future()  # Run forever


asyncio.run(main())
