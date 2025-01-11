<!-- //ENTER UPC PAGE// -->

<script lang="ts">
  import { goto } from "$app/navigation";
  import { event } from "@tauri-apps/api";
  import WebSocket from "@tauri-apps/plugin-websocket";
  

//------------------------------------------
// this stuff should work

  async function showUPC(){
    console.log(testing_UPC_code);
  }

  var ws: WebSocket;

  let testing_UPC_code: string = "070847022909";

  let ret = "";
  async function get_ingredients() {
    let upc = testing_UPC_code;
    ws = await WebSocket.connect("ws://192.168.0.124:8765");
    ws.addListener((msg) => {
      console.log("Received Message:", msg);
      if (typeof msg.data === "string") {
        ret = msg.data; //receives
      } 
      // else (typeof msg.data === obj){
        // TO DO - figure out how to receive each piece of the object rec'd
      // }
    });

    await ws.send(upc);
    //await ws.disconnect();
    console.log(ret);
    return ret; // front end displays
  };

  //get_ingredients();

</script>




<!-- <h1>Enter UPC Code</h1> -->
<!-- ------------------------------------------
Should work: -->

<!-- <button onclick={() => get_ingredients()}>
  <h2>Find Ingredients</h2>
</button> -->

<!-- prints on screen! -->


<!-- -------------------------------------- -->

<br />
<button onclick={() => goto("/")}>Back</button>

<input bind:value={testing_UPC_code} placeholder="enter upc code" />
<button type="submit" onclick={get_ingredients}>Enter</button> 

<p>{ret}</p> 


<!-- <p>{finalArray}</p> -->


<!-- Here we basically need to call get_ingredients() with the UPC the user
entered in the input box (need an event listener to use get_ingredients with
a parameter). Then display
<p>{finalArray}</p> to show the ingredients from the server. If


TO DO: add error or nothing at all happen when user clicks Enter without
entering UPC - AKC-->

