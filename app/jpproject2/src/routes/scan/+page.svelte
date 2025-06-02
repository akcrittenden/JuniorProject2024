<!-- //ENTER UPC PAGE// -->

<script lang="ts">
  import { onMount } from "svelte";
  import BottomNavigation from "../../components/BottomNavigation.svelte";
  import TopBanner from "../../components/TopBanner.svelte";
  import ProductNotFoundToast from "../../components/ProductNotFoundToast.svelte";
  import AllergensDetectedToast from "../../components/AllergensDetectedToast.svelte";
  import NoAllergensDetectedToast from "../../components/NoAllergensDetectedToast.svelte";
  import { get_ingredients } from "../../functions/functions.js";
  import { matchingAllergens } from "../../functions/functions.js";
  import { Button } from "flowbite-svelte";
  import { Input, Label } from "flowbite-svelte";
  import { toSend } from "../../functions/functions.js";

  let testing_UPC_code: string = "070847022909";

  let toast_ready: boolean = false;

  onMount(() => {
    // Reset the toSend object when the page is mounted
    toSend.upc = "";
    matchingAllergens[0] = "0"; // Reset matching allergens state
    toast_ready = false;
  });

</script>

<TopBanner />

<div class="form-row h-60 flex items-center space-x-4">
  <!-- UPC input -->
  <div class="form-field input-field flex-1">
    <Input type="text" bind:value={toSend.upc} />
  </div>

  <!-- Enter button -->
  <div class="form-field button-field">
    <Button
      size="sm"
      class="bg-green-500 hover:bg-green-600 text-white"
      on:click={() => {
        toast_ready = true;
        get_ingredients();
      }}
    >
      Enter
    </Button>
  </div>
</div>

<!-- Call get_ingredients upon clicking enter button -->

<!-- Call toasts -->
<div class="fixed top-15 left-0 w-full bg-white shadow z-50">
  {#if toast_ready}
    <!-- Only shows toast after get_ingredients() is finished -->
    {#if matchingAllergens[0] == "0"}
      <NoAllergensDetectedToast />
    {:else if matchingAllergens[0] == "1"}
      <ProductNotFoundToast />
    {:else if matchingAllergens[0] == "z"}
      <AllergensDetectedToast />
    {/if}
  {/if}
</div>

<BottomNavigation />