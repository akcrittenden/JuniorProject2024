<!-- Our main navigation component -->

<script>
  import { BottomNav, BottomNavItem } from "flowbite-svelte";
  import {
    HomeSolid,
    SeedlingSolid,
    EyeSolid,
    UserSettingsSolid,
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
  <BottomNavItem btnName="Dietary Profile" href="/dietary-profile">
    <SeedlingSolid />
  </BottomNavItem>
  <BottomNavItem btnName="Scanner" href="/scanner">
    <EyeSolid />
  </BottomNavItem>
  <BottomNavItem btnName="Settings" href="/settings">
    <UserSettingsSolid />
  </BottomNavItem>
</BottomNav>
