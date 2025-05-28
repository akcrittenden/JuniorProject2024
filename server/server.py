import asyncio
import sqlite3
import os
import websockets
import requests
from datetime import datetime
import json

api_key = "DEMO_KEY"
db_filename = "branded_foods.db"


# Initialize the SQLite database
def initialize_database():
    # Creates the database and table if they don't exist, and prints status messages.

    conn = sqlite3.connect(db_filename)
    cursor = conn.cursor()

    # Check if database file already exists
    if os.path.exists(db_filename):
        print(f"{get_timestamp()} - Connected to existing database.")
    else:
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS FoodProducts (
            upc_code TEXT PRIMARY KEY,
            brand_name TEXT NOT NULL,
            description TEXT NOT NULL,
            ingredients TEXT NOT NULL
        )
        """)

        print(f"{get_timestamp()} - Database created successfully.")

    conn.commit()
    conn.close()


def fetch_from_db(upc_code):
    # Retrieve product details from the database by UPC code

    conn = sqlite3.connect(db_filename)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM FoodProducts WHERE upc_code = ?", (upc_code,))
    product = cursor.fetchone()  # Fetch one record

    conn.close()

    if product:
        return {
            "brand_name": product[1],
            "description": product[2],
            "ingredients": product[3]
        }
    return None  # No record found


# Search USDA Food Central Database for UPC key
async def fetch_from_usda(search_term):
    # Define search endpoint
    url = "https://api.nal.usda.gov/fdc/v1/foods/search"

    # Create search parameter dictionary
    params = {
        "api_key": api_key,
        "query": search_term,
        "dataType": "Branded",
        "pageSize": 1,  # Number of results per page
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


# Store a new product in the database
def add_to_db(upc_code, brand_name, description, ingredients):
    conn = sqlite3.connect(db_filename)
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO FoodProducts (upc_code, brand_name, description, ingredients)
            VALUES (?, ?, ?, ?)
        """, (upc_code, brand_name, description, ingredients))

        conn.commit()
        print(f"{get_timestamp()} - Product added to database: {upc_code}")

    except sqlite3.IntegrityError:
        print(f"{get_timestamp()} - UPC {upc_code} already exists in database.")
    finally:
        conn.close()


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
            await websocket.send(
                json.dumps({"error": "Invalid format. Send a JSON object with 'upc' and 'allergens' list."}))
            return

        print(f"{get_timestamp()} - Received UPC: {upc}")
        print(f"{get_timestamp()} - Received Allergens: {allergens}")

        # Check if the product exists in branded_foods.db
        product = fetch_from_db(upc)

        if product:
            print(f"{get_timestamp()} - Found UPC {upc} in {db_filename}.")
        else:
            print(f"{get_timestamp()} - UPC {upc} not found in {db_filename}. Fetching from USDA...")

            # Fetch data from USDA if not found
            product = await fetch_from_usda(upc)

            if product and "foods" in product and len(product["foods"]) > 0:
                food = product["foods"][0]
                description = food.get("description", "No description found")
                brand_name = food.get("brandName", "No brand name found")
                ingredients = food.get("ingredients", "No ingredients found")
                product = {"upc_code": upc, "brand_name": brand_name, "description": description,
                           "ingredients": ingredients}

                # Store fetched data in database
                add_to_db(upc, brand_name, description, ingredients)
            else:
                print(f"{get_timestamp()} - Product not found")
                await websocket.send(json.dumps({"error": "Product not found"}))
                return

        # Lowercase and split ingredient string by commas
        raw_ingredients = product["ingredients"].lower()
        ingredient_phrases = [ingredient.strip() for ingredient in raw_ingredients.split(",") if ingredient.strip()]

        # Tokenize each phrase into a tuple of words
        tokenized_ingredients = [tuple(phrase.split()) for phrase in ingredient_phrases]

        # Pair each tokenized tuple with its original phrase
        ingredient_map = list(zip(tokenized_ingredients, ingredient_phrases))

        # Normalize allergen input
        allergens_lower = [a.lower() for a in allergens]

        # Store original ingredient phrases that contain any allergen
        # Match if full allergen string is in the phrase or as a token group
        matches = []
        for tokens, original_phrase in ingredient_map:
            phrase_text = ' '.join(tokens)
            for allergen in allergens_lower:
                if allergen in phrase_text:
                    matches.append(original_phrase)
                    break  # Avoid duplicate entries

        # Check if any matches were found
        if not matches:
            # Send no matches found
            print(f"{get_timestamp()} - Matching Allergens Found: None")
            await websocket.send("None")
        else:
            # Send list of matches to the client
            print(f"{get_timestamp()} - Matching Allergens Found: {matches}")
            await websocket.send(matches)  # TO DO: Can we make this send an object with the Brand Name and
            # description so we can display them in the UI? (After JP
            # Presentation) - Amanda

    except Exception as e:
        print(f"{get_timestamp()} - Error: {e}")
        await websocket.send(json.dumps({"error": "Server error"}))


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
    host = "0.0.0.0"  # Listen on all network interfaces
    port = 8765

    # Initialize the database before starting the server
    initialize_database()

    # Start WebSocket server
    print(f"{get_timestamp()} - Starting server on foodlens.tplinkdns.com:{port}")
    async with websockets.serve(websocket_handler, host, port):
        await asyncio.gather(periodic_message())
        await asyncio.Future()  # Run forever


asyncio.run(main())
