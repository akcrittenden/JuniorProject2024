<!-- //CANERA SCANNER PAGE// -->


<script lang="ts">
  import { goto } from "$app/navigation";
  import { scan, Format, checkPermissions, requestPermissions } from '@tauri-apps/plugin-barcode-scanner';

const handleScan = async () => {
try {
      const permissions = await checkPermissions();
      if (permissions != "granted"){
        const requestResult = await requestPermissions();
        if (requestResult !== "granted"){
          console.log("Permissions not granted");
        }
      }
      const result = await scan({ windowed :true }); 
} catch (error) {
  // TO DO: Handle error
}
};


const getCameraPreview = async () => {
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
};

</script>

<br />
<button onclick={() => goto("/")}>Back</button>

<div>
  <video id="video" width="300" height="300" autoplay></video>
  <br />
  <button onclick={getCameraPreview}>Start Camera</button>
  <br />
  <button onclick={handleScan}>Scan</button>
  <br />
  <div id="result"></div>
</div>


<style>
  body {
    background: transparent;
  }
</style>

