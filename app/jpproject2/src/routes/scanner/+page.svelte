<!-- //CANERA SCANNER PAGE// -->
<script lang="ts">
  import { dev } from "$app/environment";
  import BottomNavigation from "../../components/BottomNavigation.svelte";
  import TopBanner from "../../components/TopBanner.svelte";
  import CameraScanner from "../../components/CameraScanner.svelte";
  //--------------  custom mode scanner ---------------

</script>

<div class="scanner-page">
  <TopBanner />
  <div class="scanner-content">
    <CameraScanner />
  </div>
  <BottomNavigation />
</div>

<style>
  .scanner-page {
    display: flex;
    flex-direction: column;
    min-height: 100vh;
  }
  .scanner-content {
    flex: 1 1 auto;
    display: flex;
    flex-direction: column;
    justify-content: center;
    /* Optionally add: justify-content: center; align-items: center; */
  }
</style>

