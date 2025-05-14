<!-- //ENTER UPC PAGE// -->

<script lang="ts">
  import { goto } from "$app/navigation";
  import { json } from "@sveltejs/kit";
  import { event } from "@tauri-apps/api";
  import { dataDir } from "@tauri-apps/api/path";
  import WebSocket from "@tauri-apps/plugin-websocket";
  import { allergen, severity, allergens, addAllergen } from '../../stores/allergens.js'; //import allergens from store
  import { onMount } from 'svelte';
  import BottomNavigation from '../../components/BottomNavigation.svelte';
  import TopBanner from "../../components/TopBanner.svelte";

//------------------------------------------

  // async function showUPC(){
  //   console.log(testing_UPC_code);
  // }

  var ws: WebSocket;

  let testing_UPC_code: string = "070847022909";
  let jsonDump: object = {description: ""};

  let returnedIngredients = "";
  async function get_ingredients() {
    let upc = testing_UPC_code;
   //  ws = await WebSocket.connect("ws://allerscan.tplinkdns.com:443");
    ws = await WebSocket.connect("ws://192.168.0.124:8765");
    ws.addListener((msg) => {
      console.log("Received Message:", msg);
      if (typeof msg.data === "string") {
        returnedIngredients = msg.data; //receives the ingredients and description as a one string
        console.log("Received string");
      } 
      else {
        jsonDump = JSON.parse(returnedIngredients);
        console.log(jsonDump);
        console.log(jsonDump.description)
      }
    });

    await ws.send(upc);
    //await ws.disconnect(); // maybe make this on a timer? if not called in 30 seconds or something disconnect
    console.log(returnedIngredients);
    return returnedIngredients; // front end displays
  };

  // Sends allergens to server on navigation to scan page
  onMount(async () => {
        ws = await WebSocket.connect("ws://10.220.12.72:8765");
    await ws.send(JSON.stringify({ type: "allergens", payload: $allergens }));
    console.log("Allergens sent to server.");
    });
// TO DO: This sends a payload of allergens to the server when this screen is entered, 
// but the server doesn't know what to do with it. We'll have to figure out how to
// tell the server what we're sending - would be as easy as appending a 1 or 0
// to the beginning of some string and on the server doing a if/else thing
// depending on what it gets

</script>

<TopBanner />

<!-- <input bind:value={testing_UPC_code} placeholder="enter upc code" />
<button type="submit" onclick={get_ingredients} >Enter</button>  -->
<br><br />

<h1>Enter UPC:</h1>

<!-- Ignore <style> for now, just playing around with it as I learn -->
  <style>
    p {
        color: black;
    }
  
    button {
        background-color: rebeccapurple;
        color: white;
        border: none;
        padding: 10px;
    }
  </style>

<form>
  <label>
    <input bind:value={testing_UPC_code} />
  </label>
  <button onclick={get_ingredients} >Enter</button>
</form>

<p></p>
Food Item:
{jsonDump.description} 
<p></p>
Brand:
{jsonDump.brandName}
<p></p>
Ingredients:
{jsonDump.ingredients}

<BottomNavigation />

