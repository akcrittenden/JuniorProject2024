<script>
  let allergen = "";
  import { goto } from "$app/navigation";

  function showAllergen() {
    console.log(allergen);
  }
</script>

<br /><button onclick={() => goto("/")}>Back</button>

<h1>Enter Allergens</h1>

<input id="allergen" type="text" bind:value={allergen} />
<button type="submit" onclick={showAllergen}>Enter</button>
