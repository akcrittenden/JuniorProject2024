<!-- Our main navigation component -->
<!-- TODO: add padding on top of navigation bar, center the icons, make them squish together or apart -->
<script>
  import { BottomNav, BottomNavItem } from "flowbite-svelte";
  import {
    HomeSolid,
    SeedlingSolid,
    EyeSolid,
    PenSolid,
  } from "flowbite-svelte-icons";
  import { page } from "$app/stores";

  let activeUrl;
  $: activeUrl = $page.url.pathname;
</script>

<BottomNav
  {activeUrl}
  position="fixed"
  class="bottom-nav bottom-0 left-0 w-full"
  innerClass="grid grid-cols-4"
  activeClass="font-bold text-green-500"
>
  <BottomNavItem btnName="Home" href="/">
    <HomeSolid class="w-8 h-8"/>
  </BottomNavItem>
  <BottomNavItem btnName="Allergens" href="/dietary-profile">
    <SeedlingSolid class="w-8 h-8"/>
  </BottomNavItem>
  <BottomNavItem btnName="Scanner" href="/scanner">
    <EyeSolid class="w-8 h-8"/>
  </BottomNavItem>
  <BottomNavItem btnName="Manual" href="/scan">
    <PenSolid class="w-8 h-8"/>
  </BottomNavItem>
</BottomNav>


<style>
  :global(.bottom-nav) {
    padding-top: 5rem;
  }
</style>