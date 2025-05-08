<!-- FRONT PAGE -->

<script>
  import { goto } from "$app/navigation";
  import { Alert } from 'flowbite-svelte'; //Amanda's trying things lol
  import BottomNavigation from "../components/BottomNavigation.svelte";
</script>

<!-- Barcode Icon -->
<link
  rel="stylesheet"
  href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.2/css/all.min.css"
/>

<style lang="postcss">
/* Button styling */
  button {
    border: none;
    display: flex;
    padding: 0.75rem 1.5rem;
    background-color: rgb(18, 189, 95);
    color: #ffffff;
    font-size: 0.75rem;
    line-height: 1rem;
    font-weight: 700;
    cursor: pointer;
    text-align: center;
    text-transform: uppercase;
    vertical-align: middle;
    align-items: center;
    border-radius: 0.5rem;
    user-select: none;
    gap: 0.75rem;
    box-shadow: 0 4px 6px -1px #488aec31, 0 2px 4px -1px #488aec17;
    transition: all 0.6s ease;
  }

  button:hover {
    box-shadow: 0 10px 15px -3px #488aec4f, 0 4px 6px -2px #488aec17;
  }

  button:focus,
  button:active {
    opacity: 0.85;
    box-shadow: none;
  }

  button i {
    font-size: 1rem;
  }

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

<h1>FoodLens</h1>

<BottomNavigation />
