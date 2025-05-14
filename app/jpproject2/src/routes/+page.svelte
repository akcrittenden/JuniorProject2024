<!-- FRONT PAGE -->

<script>
  import { goto } from "$app/navigation";
  import { Alert } from 'flowbite-svelte'; //Amanda's trying things lol
  import BottomNavigation from "../components/BottomNavigation.svelte";
  import TopBanner from "../components/TopBanner.svelte";

</script>

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

<!-- Flowbite Components -->
<TopBanner />

<BottomNavigation />
