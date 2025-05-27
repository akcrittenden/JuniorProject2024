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
  position="absolute"
  innerClass="grid-cols-4"
  activeClass="font-bold text-green-500"
>
  <BottomNavItem btnName="Home" href="/">
    <HomeSolid />
  </BottomNavItem>
  <BottomNavItem btnName="Allergens" href="/dietary-profile">
    <SeedlingSolid />
  </BottomNavItem>
  <BottomNavItem btnName="Scanner" href="/scanner">
    <EyeSolid />
  </BottomNavItem>
  <BottomNavItem btnName="Manual" href="/scan">
    <PenSolid />
  </BottomNavItem>
</BottomNav>
