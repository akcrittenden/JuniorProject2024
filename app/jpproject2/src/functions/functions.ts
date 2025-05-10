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

export var matchingAllergens: string[] = [];

async function getAllergens() {
    let allergensList = get(allergens);
    toSend.allergens = allergensList.map((item: { allergen: string }) => item.allergen);
    console.log("Looking for: ", toSend.allergens);
  }

export async function get_ingredients(){ 
  if (matchingAllergens.length > 0) {
    matchingAllergens.length = 0;
    console.log("Clearing previous food's allergens.")
  }
   // Clear the matchingAllergens array if it has elements
  await getAllergens(); // save user's allergens to the toSend object
  console.log("Sending to server: ", toSend);

  const ws = await WebSocket.connect("ws://foodlens.tplinkdns.com:8765");
  console.log("Connected to server");

  // home?: 192.168.0.124:8765
  //ws = await WebSocket.connect("ws://10.220.12.71:8765");
  return new Promise((resolve, reject) => {
    ws.addListener((msg) => {
      if (msg.type === "Close") {
        reject(new Error("Connection closed"));
        return;
      }
    
      console.log("Received from server:", msg);
      stringResult = String(msg.data); //receives allergens
      console.log("String from server: ", msg.data);

      console.log("String result: ", stringResult);

      if (stringResult.length == 0){ // empty array - no allergens found
            matchingAllergens.push('0'); 
            console.log("No matching allergens");
      }
      else if (stringResult.includes("Product not found")){ //if product not found, print product not found
            matchingAllergens.push('1'); //pushes allergens to array
            console.log("Product not found");
      }
      else { // if allergens found, push z
        matchingAllergens.push('z');
        console.log("Allergens detected");
      }
      resolve(matchingAllergens); // resolves the promise with the allergens
    });
    ws.send(JSON.stringify(toSend)); 
    
    ws.addListener = (error) =>{
      reject(new Error("Websocket error: ${error.message}"));
       };
       
      }); // sends the UPC and allergens to the server
 // returns result of ingredient comparison
}

  