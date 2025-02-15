<script>
  import { allergen, severity, allergens, addAllergen, removeAllergen } from '../../stores/allergens.js';
  import { goto } from '$app/navigation';
</script>

<!-- Back button -->
<br />
<button on:click={() => goto("/")}>Back</button>

<h1>Enter Allergens:</h1>

<div class="form-row">
  <!-- Allergen input -->
  <div class="form-field">
    <label for="allergen">Allergen:</label>
    <input type="text" id="allergen" bind:value={$allergen} />
  </div>

  <!-- Severity dropdown menu -->
  <div class="form-field">
    <label for="severity">Severity:</label>
    <select id="severity" bind:value={$severity}>
      <option value="mild">Mild</option>
      <option value="moderate">Moderate</option>
      <option value="severe">Severe</option>
    </select>
  </div>

  <!-- Enter button -->
  <div class="form-field">
    <button on:click={() => addAllergen($allergen, $severity)}>Enter</button>
  </div>
</div>

<h2><u>Allergen List:</u></h2>

<ul>
  {#each $allergens as item}
    <li>
      <span>{item.allergen} - {item.severity}</span>
      <button on:click={() => removeAllergen(item)}>&times;</button>
    </li>
  {/each}
</ul>

<style>
  .form-row {
    display: flex;
    align-items: flex-end;
    gap: 10px;
    flex-wrap: nowrap;
  }

  .form-field {
    display: flex;
    flex-direction: column;
  }
  
  /* Subheading styling */
  h2, div {
    color: #9395D3;
    max-width: 300px;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
      Oxygen-Sans, Ubuntu, Cantarell, "Helvetica Neue", sans-serif;
    font-size: 20px;
  }
  
  /* Heading styling */
  h1 {
    color: #006D77;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
      Oxygen-Sans, Ubuntu, Cantarell, "Helvetica Neue", sans-serif;
    font-size: 35px;
  }
  
  /* Button styling */
  button {
    background-color: rebeccapurple;
    color: white;
    border: none;
    padding: 8px;
    cursor: pointer;
  }
  
  /* Input styling */
  input[type="text"] {
    outline: none;
    margin: 0;
    padding: 5px;
    border: 1px solid #ccc;
    border-radius: 3px;
  }
  
  input[type="text"]:focus {
    border-color: #dc4f21;
    box-shadow: 0 0 2px #dc4f21;
  }
  
  /* Label styling */
  label {
    text-transform: uppercase;
    font-size: 0.8em;
    color: #777;
    margin-top: 10px;
  }
  
  /* List styling */
  ul {
    list-style: none;
    padding-left: 0;
  }
  
  li {
    padding: 6px 10px;
    border-bottom: 1px solid #ddd;
    background: #FFD5C2;
    color: #777;
  }
  
  li button {
    margin-left: 10px;
  }
</style>
