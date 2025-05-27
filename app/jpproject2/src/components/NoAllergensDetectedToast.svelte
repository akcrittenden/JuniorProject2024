<!-- No allergens detected toast -->
<script>
    import { Alert } from 'flowbite-svelte'
    import { CheckOutline } from 'flowbite-svelte-icons';
</script>

<Alert color="green" dismissable>
    <CheckOutline slot="icon" class="w-5 h-5" />
    <b>No Allergens Detected!</b>
</Alert>