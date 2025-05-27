<!-- Allergens detected toast -->
<script>
    import { Alert } from 'flowbite-svelte'
    import { CloseOutline } from 'flowbite-svelte-icons';
    import { vibrate } from "@tauri-apps/plugin-haptics"
  import { onMount } from 'svelte';

</script>

<Alert color="red" dismissable>
    <CloseOutline slot="icon" class="w-5 h-5" />
    Allergen(s) detected in product.
</Alert>