<!-- //CANERA SCANNER PAGE// -->
<script lang="ts">
  import { goto } from "$app/navigation";
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



  //--------------  custom mode scanner ---------------
  const getCameraPreview = async () => {
    console.log("Starting camera preview...");
    var cameraID;
    
    //get camera
    Html5Qrcode.getCameras()         //should trigger permissions prompt
      .then((devices) => {
        if (devices && devices.length) {
          cameraID = devices[1]?.id || devices[0].id; // fallback to the first camera if the second is unavailable

          //start camera
          const html5Qrcode = new Html5Qrcode("reader"); //create a new instance of the scanner
          const config = {
            qrbox: { width: 200, height: 200 }, //TODO@akcrittenden make look nice
            fps: 2, //SCANNING speed, not camera's displayed fps
          }
          html5Qrcode.start(
              {facingMode: "environment"}, //presumably will start using back camera
              config,
              (decodedText, decodedResult) => {
                html5Qrcode.pause(true)
                console.log("QR code detected: ", decodedText);
                onScanSuccess(decodedText, decodedResult, html5Qrcode); 
              //call the function to handle the scan result
              },
              (errorMessage) => {
                //parse error
                //maybe toast here - scanning error, please try again TODO #1@megbyrne
                html5Qrcode.resume(); // resume scanning after error
                console.log("Error: ", errorMessage);
              }
            )
            .catch((err) => {
              console.error("Starting camera failed: ", err); //start failed, handle it.
            });
        } else {
          console.error("No cameras found.");
        }
      })
      .catch((err) => {
        console.error("Error getting cameras: ", err);
      });

    //start reader
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
