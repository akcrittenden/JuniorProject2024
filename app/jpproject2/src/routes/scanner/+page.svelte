<!-- //CANERA SCANNER PAGE// -->


<script lang="ts">
  import { goto } from "$app/navigation";
  import { Html5QrcodeScanner } from "html5-qrcode"; // easy mode: use .render to make the whole UI for you.
  //import { Html5Qrcode } from "html5-qrcode"; // custom mode: no UI built for you, but more customizable.
  import WebSocket from "@tauri-apps/plugin-websocket";
  import { allergen, severity, allergens, addAllergen } from '../../stores/allergens.js'; //import allergens from store
  import { get } from 'svelte/store';

//------Global Variables------//

var scannedUPC = "Waiting....";
var ws: WebSocket;
var allergenResult: // what we get back from server
    {description: string; brandName: string, allergenFound: boolean, badIngredients?: string} =
        { description: "", brandName: "", allergenFound: false, badIngredients: ""};
//let jsonDump: object = {description: "", brandName: "", ingredients: ""}; // raw JSON ingredient dump from server - prob not needed anymore
var toSend: { allergens: 
    { allergen: string, severity: string }[], upc: string } 
        = { allergens: [], upc: "" };
var stringResult: string = ""; // in case we just get a string back, like product not found

async function getAllergens() {
    let allergensList = get(allergens);
    toSend.allergens = allergensList.map((item: { allergen: string, severity: string }) => {
      return { allergen: item.allergen, severity: item.severity };
    });
    console.log("Looking for: ", toSend.allergens);
  }

function onScanSuccess(decodedText: string, decodedResult: object) {
  // handle the scanned code
  console.log(`Code matched = ${decodedText}`, decodedResult);
  scannedUPC = decodedText; // save to global variable
  get_ingredients();
}

async function get_ingredients() { 
  toSend.upc = scannedUPC;
  await getAllergens(); // save user's allergens to the toSend object
  //  ws = await WebSocket.connect("ws://allerscan.tplinkdns.com:443");

  ws = await WebSocket.connect("ws://10.220.12.71:8765");

  ws.addListener((msg) => {
    console.log("Received Message:", msg);
    if (typeof msg.data === "string") { // if we just get a string back, like product not found
      allergenResult.allergenFound = false;
      stringResult = msg.data; //receives the ingredients and description as a one string
      console.log("Received string: ", stringResult);
      return stringResult;
    } 
    // else {
    //   jsonDump = JSON.parse(allergenResult);
    //   //console.log(jsonDump);
    //   console.log(jsonDump.description)
    // }
  });
  await ws.send(JSON.stringify(toSend));
  //await ws.disconnect(); // maybe make this on a timer? if not called in 30 seconds or something disconnect
  console.log(allergenResult);
  return allergenResult; // returns result of ingredient comparison
};

function onScanFailure(error: any) {
  // handle scan failure, usually better to ignore and keep scanning.
  // for example:
  console.warn(`Code scan error = ${error}`);
}

const getCameraPreview = async () => {
  console.log("Camera preview starting...");
  let html5QrcodeScanner = new Html5QrcodeScanner(
  "reader",
  { fps: 10, qrbox: {width: 250, height: 250} },
  /* verbose= */ false);
  html5QrcodeScanner.render(onScanSuccess, onScanFailure);
  var frame = document.getElementById('scanRegion');
  const stream = await navigator.mediaDevices.getUserMedia({ 
    audio: false,  
    video: {
      facingMode: 
      { ideal: "environment" }
    }
  });
  const video = document.getElementById('video') as HTMLVideoElement;
  video.srcObject = stream;
  video.play();
  if (frame) {
    if (frame.style.display === 'none') {
      frame.style.display = 'block';
    } else {
      frame.style.display = 'none';
    }
  }
};

</script>

<br />
<button onclick={() => goto("/")}>Back</button>

<div>
  <div id="reader" style="width: 400px;">
    <br />
    <button onclick={getCameraPreview}>Open Camera and Start Scanning</button>
    <br />
  </div>

  <p>Scan Result: {scannedUPC}</p>
  <p>Info from Server:</p>
  Allergens Found?: {allergenResult.allergenFound ? "Yes" : "No"}
  <p></p>
  Food Item:
  {allergenResult.description} 
  <p></p>
  Brand:
  {allergenResult.brandName}
  <p></p>
  Allergens:
  {allergenResult.badIngredients}
</div>


