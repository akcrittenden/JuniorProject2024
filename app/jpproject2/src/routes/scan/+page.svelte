<!-- //ENTER UPC PAGE// -->

<script lang="ts">
  import { goto } from "$app/navigation";
  import { json } from "@sveltejs/kit";
  import { event } from "@tauri-apps/api";
  import { dataDir } from "@tauri-apps/api/path";
  import WebSocket from "@tauri-apps/plugin-websocket";
  

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

</script>


<br />
<button onclick={() => goto("/")}>Back</button>

<!-- <input bind:value={testing_UPC_code} placeholder="enter upc code" />
<button type="submit" onclick={get_ingredients} >Enter</button>  -->
<br><br />

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



<!-- <p>{finalArray}</p> -->


<!-- Here we basically need to call get_ingredients() with the UPC the user
entered in the input box (need an event listener to use get_ingredients with
a parameter). Then display
<p>{finalArray}</p> to show the ingredients from the server.-->

