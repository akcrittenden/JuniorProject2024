<!-- //CANERA SCANNER PAGE// -->
<script lang="ts">
  import { goto } from "$app/navigation";
  import { Html5QrcodeScanner } from "html5-qrcode"; // easy mode: use .render to make the whole UI for you.
  import { Html5Qrcode } from "html5-qrcode"; // custom mode: no UI built for you, but more customizable.
  import {
    get_ingredients,
    toSend,
    matchingAllergens,
  } from "../../functions/functions";
  import { dev } from "$app/environment";

  let isCoolingDown: boolean = false;
  let lastScanned: string | null = null;

 async function onScanSuccess(decodedText: string, decodedResult: object, scanner: Html5Qrcode) {
     if (isCoolingDown && decodedText === lastScanned) return; // Ignore if still in cooldown

    console.log(`Code matched = ${decodedText}`, decodedResult);
    toSend.upc = decodedText; // save to global variable
    lastScanned = decodedText; // save last scanned code
    await get_ingredients();
    
    setTimeout(() => {
      scanner.resume(); // resume scanning after 2 seconds
      console.log("Camera resumed to scan again");
    }, 2000);
    }
    // Activate cooldown
    isCoolingDown = true;
    setTimeout(() => {
      isCoolingDown = false; // 2 second cooldown, but this delays receiving stuff from the server
    }, 1500);
  
  function onScanFailure(error: any) {
    // handle scan failure, usually better to ignore and keep scanning.
    // for example:
    console.warn(`Code scan error = ${error}`);
  }

  const qrCodeSuccessCallback = (decodedText: string, decodedResult: string) => {
    //handle success
  }

  //--------------  custom mode scanner ---------------
  const getCameraPreview = async () => {
    console.log("Starting camera preview...");
    var cameraID;

    //check camera permissions
    console.log("Checking camera permissions...");
    try {
      await navigator.mediaDevices.getUserMedia({ video: true});
      console.log("Camera permissions granted.");
    
    
    //get camera
    Html5Qrcode.getCameras() 
      .then((devices) => {
        if (devices && devices.length) {
          cameraID = devices[1]?.id || devices[0].id; // fallback to the first camera if the second is unavailable

          //start camera
          const html5Qrcode = new Html5Qrcode("reader"); //create a new instance of the scanner
          html5Qrcode.start(
              cameraID,
              {
                fps: 8, //SCANNING speed, not camera's displayed fps
                qrbox: { width: 250, height: 250 },
              },
              (decodedText, decodedResult) => {
                html5Qrcode.pause(true) //call the function to handle the scan result
                console.log("QR code detected: ", decodedText);
                onScanSuccess(decodedText, decodedResult, html5Qrcode); 
              //call the function to handle the scan result
              },
              (errorMessage) => {
                //parse error, ignore it TODO: if wrong kind of code, say so
                console.log("Error: ", errorMessage);
              }
            )
            .catch((err) => {
              console.error("Start failed: ", err); //start failed, handle it.
            });
        } else {
          console.error("No cameras found.");
        }
      })
      .catch((err) => {
        console.error("Error getting cameras: ", err);
      });

    //start reader
  } catch (err) {
    console.error("Camera permissions denied or unavailable: ", err);
    alert("Camera access is needed to scan items. Please enable camera permissions for Food Lens on your device.");
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
