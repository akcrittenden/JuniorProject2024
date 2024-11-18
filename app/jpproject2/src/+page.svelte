<!-- FRONT PAGE -->

<script>
  import h1 from "$lib/components/Button.svelte";
  import { goto } from "$app/navigation";
</script>

<h1>Aller-Scan</h1>

<button onclick={() => goto("/dietary-profile")}>Dietary Profile</button>
<br /><button onclick={() => goto("/scan")}>Scan</button>
