<script>
  import { allergen, severity, allergens, addAllergen } from '../../stores/allergens.js'; //Imports store file
  import { goto } from '$app/navigation';
</script>

<!-- Back button -->
<br /><button on:click={() => goto("/")}>Back</button>

<!-- Ignore <style> for now, just playing around with it as I learn -->
<style>
  h1 {
      color: black;
  }

  button {
      background-color: rebeccapurple;
      color: white;
      border: none;
      padding: 10px;
  }
</style>

<h1>Enter Allergens:</h1>

<!-- Allergen input -->
<label for="allergen">Allergen:</label>
<input type="text" id="allergen" bind:value={$allergen}>

<!-- Severity dropdown menu -->
<label for="severity">Allergen severity:</label>
<select id="severity" bind:value={$severity}>
  <option value="mild">Mild</option>
  <option value="moderate">Moderate</option>
  <option value="severe">Severe</option>
</select>

<!-- Enter button -->
<button on:click={() => addAllergen($allergen, $severity)}>Enter</button>

<!-- Temporary for testing: Prints allergens/severity to screen -->
<p>
  {#each $allergens as { allergen, severity }}
      {allergen} - {severity}<br>
  {/each}
</p>
