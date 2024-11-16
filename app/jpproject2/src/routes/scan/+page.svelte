<script>
  import { goto } from "$app/navigation";
  let upc = "";

  function showUPC() {
    console.log(upc);
  }
</script>

<br />
<button on:click={() => goto("/")}>Back</button>

<h1>Enter UPC Code</h1>

<input bind:value={upc} placeholder="enter upc code" />
<button type="submit" on:click={showUPC}>Enter</button>
