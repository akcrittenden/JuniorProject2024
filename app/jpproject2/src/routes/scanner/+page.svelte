<!-- //CANERA SCANNER PAGE// -->
<script lang="ts">
  import { toSend } from "../../functions/functions";
  import { dev } from "$app/environment";
  import BottomNavigation from "../../components/BottomNavigation.svelte";
  import TopBanner from "../../components/TopBanner.svelte";
  import CameraScanner from "../../components/CameraScanner.svelte";
  //--------------  custom mode scanner ---------------

</script>

<TopBanner />

<!-- loader: -->

<div>

  <CameraScanner />
  
  <p>Scan Result: {toSend.upc ? toSend.upc : "Waiting..."}</p>

</div>


<BottomNavigation />
