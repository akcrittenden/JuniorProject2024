<!-- FRONT PAGE -->

<script>
  import { goto } from "$app/navigation";
  import { Alert } from "flowbite-svelte"; //Amanda's trying things lol
  import { Button } from "flowbite-svelte";
  import BottomNavigation from "../components/BottomNavigation.svelte";
  import TopBanner from "../components/TopBanner.svelte";
</script>

<!-- Flowbite Components -->
<TopBanner />

<!-- Start Scanning button -->
<Button
  size="xl"
  class="absolute inset-x-0 top-[200px] mx-auto w-max bg-green-500 hover:bg-green-600 text-white"
  href="/scanner"
>
  Start Scanning
</Button>

<!-- Manual Entry button -->
<div>
  <Button
    size="md"
    class="absolute inset-x-0 top-[275px] mx-auto w-max bg-green-500 hover:bg-green-600 text-white"
    href="/scan"
  >
    Manual Entry
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
