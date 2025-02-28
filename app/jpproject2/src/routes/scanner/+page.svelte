<!-- //CANERA SCANNER PAGE// -->
<script lang="ts">
  import { goto } from "$app/navigation";
  import { Html5QrcodeScanner } from "html5-qrcode"; // easy mode: use .render to make the whole UI for you.
  //import { Html5Qrcode } from "html5-qrcode"; // custom mode: no UI built for you, but more customizable.
  import { get_ingredients, toSend, allergenResult } from "../../functions/functions";

function onScanSuccess(decodedText: string, decodedResult: object) {
    // handle the scanned code
    console.log(`Code matched = ${decodedText}`, decodedResult);
    toSend.upc = decodedText; // save to global variable
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

  <p>Scan Result: {toSend.upc ? toSend.upc : "Waiting..."}</p>
  <p>Info from Server:</p>
  <p></p>
  Food Item:
  {allergenResult.description} 
  <p></p>
  Brand:
  {allergenResult.brandName}
  <p></p>
  Allergens:
  {allergenResult.matching_allergens}
</div>


