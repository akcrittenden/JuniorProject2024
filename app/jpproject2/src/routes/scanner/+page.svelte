<!-- //CANERA SCANNER PAGE// -->


<script lang="ts">
  import { goto } from "$app/navigation";
  //import { scan, Format, checkPermissions, requestPermissions } from '@tauri-apps/plugin-barcode-scanner';


let scanResult = "";

// const handleScan = async () => {
// try {
//       const permissions = await checkPermissions();
//       if (permissions != "granted"){
//         const requestResult = await requestPermissions();
//         console.log("Permissions requested: ", requestResult);
//         if (requestResult != "granted"){
//           console.log("Permissions not granted or laptop can't grant permissions?");
//         }
//       }
//       const result = await scan({ windowed :true }); 
//       scanResult = result.content;
// } catch (error) {
//   console.error("Permissions wonky: ", error);
// }
// };


const getCameraPreview = async () => {
  console.log("Camera preview starting...");
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
  <!-- svelte-ignore a11y_media_has_caption -->
  <video 
    id="video" 
    autoplay
    disablepictureinpicture
    disableremoteplayback
    style="display: block; margin: 0 auto;">
  </video>

  <br />
  <button onclick={getCameraPreview}>Start Camera</button>
  <br />
  <button onclick={handleScan}>Scan</button>
</div>


