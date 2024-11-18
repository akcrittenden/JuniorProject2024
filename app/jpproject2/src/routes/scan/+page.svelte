<!-- //SCAN PAGE// -->

<script lang="ts">
  import { goto } from "$app/navigation";
  import WebSocket from "@tauri-apps/plugin-websocket";

  let upc = "";

  function showUPC() {
    console.log(upc);
  }
  var ws: WebSocket;

  const finalArray: string[] = [];
  //function set_allergen_severity() {} //TO DO
  async function get_ingredients(upc: string) {
    ws = await WebSocket.connect("ws://10.220.8.180:8765");
    ws.addListener((msg) => {
      // listens for msg back from server
      console.log("Received Message:", msg); // it will print "Rec'd message: blah" in console
      if (typeof msg.data === "string") {
        //if the message back from server is a string, set it to a variable
        finalArray[0] = msg.data; //receive
      } else if (typeof msg === "object") {
        finalArray[0] = Object.keys(msg)[0];
        finalArray[1] = Object.keys(msg)[1]; //TO DO: this still just
        // returns 'data' and 'type' literally - will look into how to fix - AKC
      } 
    });

    await ws.send(upc);
    await ws.disconnect();
    console.log(finalArray[0] + ", " + finalArray[1]);
    return finalArray; // front end displays
  }
</script>

<br />
<button on:click={() => goto("/")}>Back</button>
<p>I'm allergic to soy and wheat. Let's see what I can eat!</p>
<h1>Enter UPC Code</h1>

<input bind:value={upc} placeholder="enter upc code" />
<button type="submit" on:click={showUPC}>Enter</button>

<!-- Here we basically need to call get_ingredients() with the UPC the user
entered in the input box (I think it would look something like 
on:click={get_ingredients(upc from the box)}). Then display
<p>{finalArray}</p> to show the ingredients from the server. If
We wanted to add multiple actions on click, we would need to use an
event listener.

TO DO: add error or nothing at all happen when user clicks Enter without
entering UPC - AKC-->

