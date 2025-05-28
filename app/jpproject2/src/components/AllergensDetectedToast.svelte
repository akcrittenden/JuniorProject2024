<!-- Allergens detected toast -->
<script>
    export let message = "";
    import { Alert } from 'flowbite-svelte'
    import { CloseOutline } from 'flowbite-svelte-icons';

</script>

<Alert color="red" dismissable>
    <CloseOutline slot="icon" class="w-5 h-5" />
    <b>Allergen(s) detected in product: </b>
    {#if message}
      <div>{message}</div>
    {/if}
</Alert>