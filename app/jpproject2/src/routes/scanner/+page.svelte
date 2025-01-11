<!-- //CANERA SCANNER PAGE// -->


<script lang="ts">
  import { goto } from "$app/navigation";
  import { scan, Format } from '@tauri-apps/plugin-barcode-scanner';

  scan({ windowed: true, formats: [Format.EAN13], cameraDirection: 'back' });

</script>

<br />
<button onclick={() => goto("/")}>Back</button>


