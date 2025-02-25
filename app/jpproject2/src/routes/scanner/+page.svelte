<!-- //CANERA SCANNER PAGE// -->


<script lang="ts">
  import { goto } from "$app/navigation";
  import { Html5QrcodeScanner } from "html5-qrcode"; // easy mode: use .render to make the whole UI for you.
  //import { Html5Qrcode } from "html5-qrcode"; // custom mode: no UI built for you, but more customizable.
  import WebSocket from "@tauri-apps/plugin-websocket";
  //import { scan } from "@tauri-apps/plugin-barcode-scanner";


let scanResult = "Waiting....";
var ws: WebSocket;

let returnedIngredients = "";
let jsonDump: object = {description: "", brandName: "", ingredients: ""}; //initialize to empty string so it doesn't throw an error when trying to display it
async function get_ingredients() { 
  let upc = scanResult;
  //  ws = await WebSocket.connect("ws://allerscan.tplinkdns.com:443");
  ws = await WebSocket.connect("ws://10.174.243.114:8765");
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


function onScanSuccess(decodedText: string, decodedResult: object) {
  // handle the scanned code as you like, for example:
  console.log(`Code matched = ${decodedText}`, decodedResult);
  scanResult = decodedText;
  get_ingredients();
}

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
  <p>Scan Result: {scanResult}</p>
  <p>Info from Server:</p>
  Food Item:
  {jsonDump.description} 
  <p></p>
  Brand:
  {jsonDump.brandName}
  <p></p>
  Ingredients:
  {jsonDump.ingredients}
</div>


