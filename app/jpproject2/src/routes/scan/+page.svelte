<!-- //SCAN PAGE// -->

<script lang="ts">
  import { goto } from "$app/navigation";
  import { event } from "@tauri-apps/api";
  import WebSocket from "@tauri-apps/plugin-websocket";

  let upc = "";

  function showUPC() {
    console.log(upc);
  }
  var ws: WebSocket;

  const finalArray: string[] = [];
  //function set_allergen_severity() {} //TO DO
  async function get_ingredients(upc: string) {
   // ws = await WebSocket.connect("ws://10.220.8.180:8765");
    ws = await WebSocket.connect("ws://127.0.0.1:8080")
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

// THIS SHOULD BE WORKING WTF 
  const button = document.getElementById("button");
  button?.addEventListener("click", handleClick);

function handleClick(this: HTMLElement) {
    console.log("Clicked!");

}
  
</script>



<br />
<button on:click={() => goto("/")}>Back</button>
<h1>Enter UPC Code</h1>

<input bind:value={upc} placeholder="enter upc code" />
<button type="submit">Enter</button> 
<!-- removed the on:click(showUPC) thing to test the event listener on lines 40-45 but it no worky :( -->

<p>{finalArray}</p>


<!-- Here we basically need to call get_ingredients() with the UPC the user
entered in the input box (need an event listener to use get_ingredients with
a parameter). Then display
<p>{finalArray}</p> to show the ingredients from the server. If


TO DO: add error or nothing at all happen when user clicks Enter without
entering UPC - AKC-->

