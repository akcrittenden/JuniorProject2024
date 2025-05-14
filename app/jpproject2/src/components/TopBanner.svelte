<script>
  import { Navbar, NavBrand, NavHamburger, NavUl, NavLi } from 'flowbite-svelte';
  import { UserSettingsSolid } from 'flowbite-svelte-icons';
</script>

<!-- Top Banner, height 15 (can be adjusted) -->
<Navbar class="h-15">
  <NavBrand class="absolute inset-x-0 mx-auto w-max">
    <span class="self-center text-xl font-semibold whitespace-nowrap text-green-500">FoodLens</span>
  </NavBrand>
  <NavHamburger class="z-10"/>
  <NavUl class="ml-auto z-10">
    <NavLi href="/settings">
      <UserSettingsSolid class="w-5 h-5" />
    </NavLi>
  </NavUl>
</Navbar>