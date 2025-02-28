import { allergens } from '../stores/allergens.js'; //import allergens from store
import { get } from 'svelte/store';
import WebSocket from "@tauri-apps/plugin-websocket";

var ws: WebSocket;
var stringResult: string = ""; // in case we just get a string back, like product not found
export var toSend: { allergens: 
  { allergen: string, severity: string }[], upc: string } 
      = { allergens: [], upc: "" };

export var allergenResult: // what we get back from server
  {description: string; brandName: string, ingredients: "", matching_allergens?: string} =
      { description: "", brandName: "", ingredients: "", matching_allergens: ""};

async function getAllergens(toSend: { allergens: 
    { allergen: string, severity: string }[], upc: string } 
           = { allergens: [], upc: "" }) {
    let allergensList = get(allergens);
    toSend.allergens = allergensList.map((item: { allergen: string, severity: string }) => {
      return { allergen: item.allergen, severity: item.severity };
    });
    console.log("Looking for: ", toSend.allergens);
  }

  export async function get_ingredients(){ 
    await getAllergens(); // save user's allergens to the toSend object
    //  ws = await WebSocket.connect("ws://foodlens.tplinkdns.com:443");
    // home?: 192.168.0.124:8765
    ws = await WebSocket.connect("ws://10.220.12.71:8765");
    ws.addListener((msg) => {
      console.log("Received Message:", msg);
      if (typeof msg.data === "string") { // if we just get a string back, like product not found
        stringResult = msg.data; //receives the ingredients and description as a one string
        console.log("Received string: ", stringResult);
        return stringResult;
      } 
    });
    await ws.send(JSON.stringify(toSend)); // sends the UPC and allergens to the server
    //await ws.disconnect(); // maybe make this on a timer? if not called in 30 seconds or something disconnect
    console.log(allergenResult); //receive info from server
    return allergenResult; // returns result of ingredient comparison
  };

  