<script lang="ts">
  import { invoke } from "@tauri-apps/api/core";
  import WebSocket from "@tauri-apps/plugin-websocket";
  import { commands } from "./types";
  import type { allergen_severity } from "./types";

  // when using `"withGlobalTauri": true`, you may use
  // const WebSocket = window.__TAURI__.websocket;

  let name = "";
  let greetMsg = "";
  let sentMsg = "";
  var ws: WebSocket;

  let testing_UPC_code: "041570072561";

  // enum commands {
  //   GET_INGREDIENTS = '1'
  // }

  // enum allergen_severity { //first one is 1, then rest automatically incremented
  //   MILD = 1,
  //   MODERATE,
  //   SEVERE,
  //   RESTRICTED,
  // }

  let ingredient_and_severity: [string, allergen_severity];

  function set_allergen_severity() {} //TO DO

  async function greet() {
    // Learn more about Tauri commands at https://tauri.app/v1/guides/features/command
    greetMsg = await invoke("greet", { name }); //backend function - this is typescript in the front end,
    // sending a string "greet" over websocket to backend of Tauri, so Tauri searches for the function named "greet"
  }

  async function setup_socket() {
    ws = await WebSocket.connect("ws://127.0.0.1:8080");

    ws.addListener((msg) => {
      console.log("Received Message:", msg); //receives
    });

    async function send_hello() {
      await ws.send("Hello World!");
    }
  }

  // async function get_ingredients(upc: string) {
  //   ws = await WebSocket.connect("ws://127.0.0.1:8080");
  //   let ret = "";
  //   ws.addListener((msg) => {
  //     console.log("Received Message:", msg);
  //     if (typeof msg === "string") {
  //       ret = msg; //receives
  //     } else ret = "Either server isn't connected or something is broken.";
  //   });

  //   await ws.send(enums.commands.GET_INGREDIENTS + upc);
  //   await ws.disconnect();
  //   console.log(ret);
  //   return ret; // front end displays
  // }

      let ret = "";
  async function get_ingredients() {
    ws = await WebSocket.connect("ws://127.0.0.1:8080");
    ws.addListener((msg) => {
      console.log("Received Message:", msg);
      if (typeof msg.data === "string") {
        ret = msg.data; //receives
      } 
    });

    await ws.send(commands.GET_INGREDIENTS);
    await ws.disconnect();
    console.log(ret);
    return ret; // front end displays
  }

  setup_socket();
  get_ingredients();

</script>

<div class="container">
  <h1>Welcome to Tauri!</h1>

  <div class="row">
    <a href="https://vitejs.dev" target="_blank">
      <img src="/vite.svg" class="logo vite" alt="Vite Logo" />
    </a>
    <a href="https://tauri.app" target="_blank">
      <img src="/tauri.svg" class="logo tauri" alt="Tauri Logo" />
    </a>
    <a href="https://kit.svelte.dev" target="_blank">
      <img src="/svelte.svg" class="logo svelte-kit" alt="SvelteKit Logo" />
    </a>
  </div>

  <!-- <p>Click on the Tauri, Vite, and SvelteKit logos to learn more.</p>

  <form class="row" on:submit|preventDefault={greet}>
    <input
      id="greet-input"
      placeholder="Enter a message..."
      bind:value={name}
    />
    <button type="submit">Greet</button>
  </form>

  <p>{greetMsg}</p> -->

  <!-- <button on:click={send_hello}>
    <h1>Send Hello!</h1>
  </button> -->

  <!-- TO DO: dropdown go here -->

  <button on:click={() => get_ingredients()}>
    <h1>Find Ingredients</h1>
  </button>

  <!-- prints on screen! -->
  <p>{ret}</p> 

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
