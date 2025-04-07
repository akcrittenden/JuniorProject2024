<!-- //CANERA SCANNER PAGE// -->
<script lang="ts">
  import { goto } from "$app/navigation";
  import { Html5QrcodeScanner } from "html5-qrcode"; // easy mode: use .render to make the whole UI for you.
  import { Html5Qrcode } from "html5-qrcode"; // custom mode: no UI built for you, but more customizable.
  import { get_ingredients, toSend, matchingAllergens } from "../../functions/functions";
  import { dev } from "$app/environment";

let isCoolingDown: boolean = false;

function onScanSuccess(decodedText: string, decodedResult: object) {
    if (isCoolingDown == true) return; // Ignore if still in cooldown
    console.log(`Code matched = ${decodedText}`, decodedResult);
    toSend.upc = decodedText; // save to global variable
    get_ingredients();

    // Activate cooldown
    isCoolingDown = true;
    setTimeout(() => {
      isCoolingDown = false; // 2 second cooldown, but this delays receiving stuff from the server
    }, 2000);

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


//PLAYING WITH PRO VERSION


// const getCameraPreview = async () => {
//   console.log("Camera preview starting...");

//   Html5Qrcode.getCameras().then(devices =>{
//   if (devices && devices.length) {
//     const cameraId = devices[1].id;
//     const html5Qrcode = new Html5Qrcode("reader");
//     const config = {
//       fps: 10,
//       qrbox: { width: 250, height: 250 }
//     }
//     html5Qrcode.start(cameraId, config, onScanSuccess, onScanFailure);
//   }
//   else {
//     console.log("No cameras found");
//   }
// })

// };

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
  <!-- <p>Info from Server:</p> -->
  <p></p>
  <!-- Food Item:
  {allergenResult.description} 
  <p></p>
  Brand:
  {allergenResult.brandName}
  <p></p>
  TO DO: make matching allergens show on UI when found --> 
  Allergens: 
  <!-- Megaaaaaaaaan make it pretty pleeeeeease - matching allergens is the array that
   holds the allergens received from the server, but if the product isn't found, index 0 is == 
   to "Product not found", so we want to display that if index 0 = that -->

</div>


