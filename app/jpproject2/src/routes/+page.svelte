<!-- FRONT PAGE -->

<script>
  import { goto } from "$app/navigation";
  import { Alert, P } from "flowbite-svelte"; //Amanda's trying things lol
  import { Button } from "flowbite-svelte";
  import BottomNavigation from "../components/BottomNavigation.svelte";
  import TopBanner from "../components/TopBanner.svelte";
</script>

<!-- Flowbite Components -->
<TopBanner />

<!-- Start Scanning button -->
<Button
  size="xl"
  class="absolute inset-x-0 top-[300px] mx-auto w-max 
        bg-green-500 hover:bg-green-600 text-white w-70 h-20"
  href="/scanner"
  >
  <P size="3xl" class=text-white>Start Scanning</P>
</Button>

<!-- Manual Entry button -->
<div>
  <Button
    size="md"
    class="absolute inset-x-0 top-[390px] mx-auto w-max bg-green-500 hover:bg-green-600 text-white"
    href="/scan"
  >
    <P size="base" class=text-white>Manual Entry</P>
  </Button>
</div>

<BottomNavigation />

<!-- This style block will be going soon -->
<style lang="postcss">
  /* Heading styling , global for now */
  :global(h1) {
    color: #494949;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
      Oxygen-Sans, Ubuntu, Cantarell, "Helvetica Neue", sans-serif;
    font-size: 45px;
  }

  /* Background color styling, global for now */
  :global(body) {
    background-color: rgb(243, 243, 243);
  }
</style>
