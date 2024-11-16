<script lang="ts">
  import { invoke } from "@tauri-apps/api/core";
  import WebSocket from "@tauri-apps/plugin-websocket";
  import { commands } from "./types";
  import type { allergen_severity } from "./types";
  import { dataDir } from "@tauri-apps/api/path";

  // when using `"withGlobalTauri": true`, you may use
  // const WebSocket = window.__TAURI__.websocket;

  let name = "";
  let greetMsg = "";
  let sentMsg = "";
  var ws: WebSocket;

  let testing_UPC_code: "041570072561";
  let entered_UPC: "";

  let ingredient_and_severity: [string, allergen_severity];

  const finalArray: string[] = [];
  //function set_allergen_severity() {} //TO DO
  async function get_ingredients(upc:string) {
    ws = await WebSocket.connect("ws://10.220.8.180:8765");
    ws.addListener((msg) => {
      // listens for msg back from server
      console.log("Received Message:", msg); // it will print "Rec'd message: blah" in console
      if (typeof msg.data === "string") {
        //if the message back from server is a string, set it to a variable
        finalArray[0] = msg.data; //receive
      }
      else if (typeof msg === "object"){
        finalArray[0] = Object.keys(msg)[0];
        finalArray[1] = Object.keys(msg)[1];        
      }
    });

    await ws.send(upc);
    await ws.disconnect();
    console.log(finalArray[0] + ', ' + finalArray[1]);
    return finalArray; // front end displays
  }

 // setup_socket();
  get_ingredients('034000056750');

  

</script>

<div class="container">
  <h1>Welcome to Tauri!</h1>

  <!-- <form class="row" on:submit|preventDefault={get_ingredients}>
    <input
      id="greet-input"
      placeholder="Enter a UPC"
      bind:value={entered_UPC}
    />
    <button type="submit">Submit</button>
  </form> -->

  <!-- <p>Click on the Tauri, Vite, and SvelteKit logos to learn more.</p>
  <p>{greetMsg}</p> -->

  <!-- <button on:click={send_hello}>
    <h1>Send Hello!</h1>
  </button> -->

<p>I'm allergic to soy and wheat. Let's see what I can eat!</p>

  <!-- TO DO: dropdown go here -->

   <form class="row" on:submit={() => get_ingredients(TO-TO)}>
   <label for="UPCs">Choose a UPC to check: </label>
   <select name="UPCs" id="UPCs">
    <option value="frenchFries">Frozen Seasoned French Fries</option>
    <option value="soySauce">Soy Sauce</option>
    <option value="glutenFreeCookie">Gluten-Free Cookie</option>
   </select>
  </form>

  <!-- <button on:click={() => get_ingredients()}>
    <h1>Find Ingredients</h1>
  </button> -->

  <!-- prints on screen! -->
  <p>{finalArray[0]}</p>
  <p>{finalArray[1]}</p>



</div>

<style>
  .logo.vite:hover {
    filter: drop-shadow(0 0 2em #747bff);
  }

  .logo.svelte-kit:hover {
    filter: drop-shadow(0 0 2em #ff3e00);
  }

  :root {
    font-family: Inter, Avenir, Helvetica, Arial, sans-serif;
    font-size: 16px;
    line-height: 24px;
    font-weight: 400;

    color: #0f0f0f;
    background-color: #f6f6f6;

    font-synthesis: none;
    text-rendering: optimizeLegibility;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    -webkit-text-size-adjust: 100%;
  }

  .container {
    margin: 0;
    padding-top: 10vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
    text-align: center;
  }

  .logo {
    height: 6em;
    padding: 1.5em;
    will-change: filter;
    transition: 0.75s;
  }

  .logo.tauri:hover {
    filter: drop-shadow(0 0 2em #24c8db);
  }

  .row {
    display: flex;
    justify-content: center;
  }

  a {
    font-weight: 500;
    color: #646cff;
    text-decoration: inherit;
  }

  a:hover {
    color: #535bf2;
  }

  h1 {
    text-align: center;
  }

  input,
  button {
    border-radius: 8px;
    border: 1px solid transparent;
    padding: 0.6em 1.2em;
    font-size: 1em;
    font-weight: 500;
    font-family: inherit;
    color: #0f0f0f;
    background-color: #ffffff;
    transition: border-color 0.25s;
    box-shadow: 0 2px 2px rgba(0, 0, 0, 0.2);
  }

  button {
    cursor: pointer;
  }

  button:hover {
    border-color: #396cd8;
  }
  button:active {
    border-color: #396cd8;
    background-color: #e8e8e8;
  }

  input,
  button {
    outline: none;
  }

  #greet-input {
    margin-right: 5px;
  }

  @media (prefers-color-scheme: dark) {
    :root {
      color: #f6f6f6;
      background-color: #2f2f2f;
    }

    a:hover {
      color: #24c8db;
    }

    input,
    button {
      color: #ffffff;
      background-color: #0f0f0f98;
    }
    button:active {
      background-color: #0f0f0f69;
    }
  }
</style>
