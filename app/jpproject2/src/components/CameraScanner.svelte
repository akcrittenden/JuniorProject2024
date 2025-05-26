<script lang="ts">
  import { Html5Qrcode } from "html5-qrcode";
  import { onDestroy, onMount } from "svelte";
  import {
    get_ingredients,
    matchingAllergens,
    toSend,
  } from "../functions/functions";
  import AllergensDetectedToast from "./AllergensDetectedToast.svelte";
  import NoAllergensDetectedToast from "./NoAllergensDetectedToast.svelte";
  import ProductNotFoundToast from "./ProductNotFoundToast.svelte";
  import { TextSizeOutline } from "flowbite-svelte-icons";

  let isPageLoaded = false;
  let html5QrcodeInstance: Html5Qrcode | null;

  let isCoolingDown: boolean = false;
  let lastScanned: string | null = null;
  let toast_ready: boolean = false; // Flag to control the toast display

  onMount(() => {
    console.log("page loaded, initializing camera preview");
    isPageLoaded = true; // Set the page as loaded
    getCameraPreview(); // Call the function to start the camera preview when the component mounts
  });

  onDestroy(() => {
    // Stop the camera when navigating away
    if (html5QrcodeInstance) {
      html5QrcodeInstance
        .stop()
        .then(() => {
          html5QrcodeInstance = null;
          console.log("Camera stopped");
        })
        .catch((err) => {
          console.error("Failed to stop camera:", err);
        });
    }
  });

  async function onScanSuccess(
    decodedText: string,
    decodedResult: object,
    scanner: Html5Qrcode
  ) {
    if (isCoolingDown && decodedText === lastScanned) return; // Ignore if still in cooldown

    console.log(`Code matched = ${decodedText}`, decodedResult);
    toSend.upc = decodedText; // save to global variable
    lastScanned = decodedText; // save last scanned code

    toast_ready = false; // Reset the toast flag
    await get_ingredients();
    toast_ready = true;

    setTimeout(() => {
      scanner.resume(); // resume scanning after 2 seconds
      console.log("Camera resumed to scan again");
    }, 500);

    isCoolingDown = true;
    setTimeout(() => {
      isCoolingDown = false; // 2 second cooldown, but this delays receiving stuff from the server
    }, 150);
  }

  // function switchCamera() {
  //   facingMode = facingMode === "environment" ? "user" : "environment";
  //   if (html5QrcodeInstance) {
  //     html5QrcodeInstance.stop().then(() => {
  //       getCameraPreview();
  //     });
  //   } else {
  //     getCameraPreview();
  //   }
  // }

  let facingMode: "environment" | "user" = "environment"; // default to back camera

  const getCameraPreview = async () => {
    console.log("Starting camera preview...");
    var cameraID;
    //get camera
    Html5Qrcode.getCameras() //should trigger permissions prompt
      .then((devices) => {
        if (devices && devices.length) {
          cameraID = devices[1]?.id || devices[0].id; // fallback to the first camera if the second is unavailable
          html5QrcodeInstance = new Html5Qrcode("scanner");          //start camera
          const config = { 
            qrbox: { width: 250, height: 250 }, // size of the scanning box
            fps: 3, //SCANNING speed, not camera's displayed fps
            aspectRatio: 1.0
          };
          console.log("Got scanner size: ", config.qrbox)
          html5QrcodeInstance
            .start(
              { facingMode },
              config,
              (decodedText, decodedResult) => {
                html5QrcodeInstance?.pause(true);
                console.log("QR code detected: ", decodedText);
                onScanSuccess(decodedText, decodedResult, html5QrcodeInstance);
                //call the function to handle the scan result
              },
              (errorMessage) => {
                //parse error
                html5QrcodeInstance?.resume(); // resume scanning after error
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

<div class="scanner-container">
    <div id="scanner" class="scanner"></div>
        <p>Scan Result: {toSend.upc ? toSend.upc : "Waiting..."}</p>

</div>

<!-- Triggers the toasts -->
{#if toast_ready}
  <!-- Only shows toast after get_ingredients() is finished -->
  {#if matchingAllergens[0] == "0"}
    <NoAllergensDetectedToast />
  {:else if matchingAllergens[0] == "1"}
    <ProductNotFoundToast />
  {:else if matchingAllergens[0] == "z"}
    <AllergensDetectedToast />
  {/if}
{/if}

<style>
    .scanner-container {
        display: grid;
        place-items: center;
    }

    .scanner {
        display: flex;
        width: 100%;
        height: 100%;
        max-width: 300px; /* Limit the maximum width */
        max-height: 300px; /* Limit the maximum height */
    }

</style>
