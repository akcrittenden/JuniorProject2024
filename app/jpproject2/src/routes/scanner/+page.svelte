<!-- //CANERA SCANNER PAGE// -->


<script lang="ts">
  import { onMount } from 'svelte';
  import { goto } from "$app/navigation";
  import { scan, Format, checkPermissions, requestPermissions } from '@tauri-apps/plugin-barcode-scanner';

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
</div>

<style>
  body {
    background: transparent;
  }
</style>
