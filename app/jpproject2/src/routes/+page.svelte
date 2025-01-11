<!-- FRONT PAGE -->

<script>
  import { goto } from "$app/navigation";
</script>

<h1>Aller-Scan</h1>

<button onclick={() => goto("/dietary-profile")}>Dietary Profile</button>
<br /><button onclick={() => goto("/scan")}>Enter UPC</button>
<br /><button onclick={() => goto("/scanner")}>Camera</button>
