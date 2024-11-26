import asyncio
import websockets
import socket
import requests
from datetime import datetime

api_key = 'DEMO_KEY'


# Search USDA Food Central Database for UPC key
async def get_data(search_term):
    # Define search endpoint and parameters
    url = 'https://api.nal.usda.gov/fdc/v1/foods/search'

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
        print(f"{get_timestamp()} - Received {search_term}")

        # Search USDA database and print returned data
        data = await get_data(search_term)
        print_data(data)

        # Send the search result back to the client
        ingredients = data['foods'][0].get('ingredients', 'No ingredients found')
        await websocket.send(ingredients)

    # No product data returned from USDA database
    except Exception as e:
        print(f"{get_timestamp()} - Error: {e}")
        format_fun()
        await websocket.send("Product Not Found")


# Print formatted product data
def print_data(data):
    if data:
        for food in data['foods']:
            print(f"Description: {food['description']}")
            print(f"Brand Name: {food['brandName']}")
            print(f"Data Type: {food['dataType']}")
            print(f"Ingredients: {food['ingredients']}")
            format_fun()
    else:
        print(f"{get_timestamp()} - Failed to fetch data from API")


# Generate formatted timestamp
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
    # Get local IP address and set port
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    port = 8765

    # Start WebSocket server
    print(f"{get_timestamp()} - Starting server on {local_ip}:{port}")

    async with websockets.serve(websocket_connection, local_ip, port):
        await asyncio.gather(periodic_message())
        await asyncio.Future()  # Run forever


asyncio.run(main())
