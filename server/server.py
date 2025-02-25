import asyncio
import sqlite3
import os
from collections import namedtuple
import websockets
import socket
import requests
from datetime import datetime
import json
import gzip

api_key = "DEMO_KEY"
db_filename = "branded_foods.db"

# Initialize the SQLite database
def initialize_database():
    """Creates the database and table if they don't exist, and prints status messages."""
    
    db_exists = os.path.exists(db_filename)  # Check if database file already exists

    conn = sqlite3.connect(db_filename)
    cursor = conn.cursor()

    if db_exists:
        print(f"{get_timestamp()} - Connected to existing database.")
    else:
        print(f"{get_timestamp()} - Database created successfully.")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS FoodProducts (
            upc_code TEXT PRIMARY KEY,
            brand_name TEXT NOT NULL,
            description TEXT NOT NULL,
            ingredients TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


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


# WebSocket handler to process UPC and allergens in a single request
async def websocket_handler(websocket):
    try:
        # Receive JSON payload from client
        message = await websocket.recv()
        
        try:
            data = json.loads(message)  # Expecting a JSON object
            upc = data.get("upc")
            allergens = data.get("allergens", [])

            if not upc or not isinstance(allergens, list):
                raise ValueError("Invalid input format")
        
        except (json.JSONDecodeError, ValueError):
            await websocket.send(json.dumps({"error": "Invalid format. Send a JSON object with 'upc' and 'allergens' list."}))
            return

        print(f"{get_timestamp()} - Received UPC: {upc}")
        print(f"{get_timestamp()} - Received Allergens: {allergens}")

        

        # Fetch product data
        food_data = await get_data(upc)

        if food_data and "foods" in food_data and len(food_data["foods"]) > 0:
            food = food_data["foods"][0]
            ingredients = food.get("ingredients", "No ingredients found").lower()

            # Compare allergens with ingredients
            matches = [allergen for allergen in allergens if allergen.lower() in ingredients]

            # Construct response
            response_data = {
                "description": food.get("description", "No description found"),
                "brandName": food.get("brandName", "No brand name found"),
                "ingredients": ingredients,
                "matching_allergens": matches
            }

            await websocket.send(json.dumps(response_data))

        else:
            await websocket.send(json.dumps({"error": "Product not found"}))

    except Exception as e:
        print(f"{get_timestamp()} - Error: {e}")
        await websocket.send(json.dumps({"error": "Server error"}))

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


# Print a line of dashes for formatting
def format_fun():
    print("-" * 100)


async def main():
    host = "0.0.0.0"    # Listen on all network interfaces
    port = 8765         # WSS port

    # Initialize the database before starting the server
    initialize_database()

    # Start WebSocket server
    print(f"{get_timestamp()} - Starting server on allerscan.tplinkdns.com:{port}")

    async with websockets.serve(websocket_handler, host, port):
        await asyncio.gather(periodic_message())
        await asyncio.Future()  # Run forever


asyncio.run(main())
