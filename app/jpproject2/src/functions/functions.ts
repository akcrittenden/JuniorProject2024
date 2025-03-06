import { allergens } from '../stores/allergens.js'; //import allergens from store
import { get } from 'svelte/store';
import WebSocket from "@tauri-apps/plugin-websocket";

var ws: WebSocket;
var stringResult: string = ""; // in case we just get a string back, like product not found
export var toSend: { 
  upc: string, 
  allergens: string[] 
} = { 
  upc: "", 
  allergens: [] 
};
let lastScannedUPC = ""; // Variable to store the last scanned UPC code

export var matchingAllergens: string[] = [];

async function getAllergens() {
    let allergensList = get(allergens);
    toSend.allergens = allergensList.map((item: { allergen: string }) => item.allergen);
    console.log("Looking for: ", toSend.allergens);
  }

export async function get_ingredients(){ 
  if (matchingAllergens.length > 0) matchingAllergens.length = 0; // Clear the matchingAllergens array if it has elements
  await getAllergens(); // save user's allergens to the toSend object
  ws = await WebSocket.connect("ws://foodlens.tplinkdns.com:8765");
  // home?: 192.168.0.124:8765
  //ws = await WebSocket.connect("ws://10.220.12.71:8765");
  ws.addListener((msg) => {
    console.log("Received Message:", msg);
// if we just get a string back, like product not found
      stringResult = String(msg.data); //receives the ingredients and description as a one string
      console.log("Received string: ", stringResult);
      console.log("Matching allergens: ", matchingAllergens);
      if (!stringResult.includes("Product not found"))
            matchingAllergens.push(stringResult);
          //TO DO - display when product not found in UI
  });
  await ws.send(JSON.stringify(toSend)); // sends the UPC and allergens to the server
  console.log("Matching allergens: ", matchingAllergens); //receive info from server
  return matchingAllergens; // returns result of ingredient comparison
  // TO DO: clear matchingAllergens
};

  