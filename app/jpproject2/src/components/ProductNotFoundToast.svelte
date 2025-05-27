<!-- Product not found toast -->
<script>
    import { Alert } from 'flowbite-svelte'
    import { InfoCircleSolid } from 'flowbite-svelte-icons';
</script>

<Alert color="yellow" dismissable>
    <InfoCircleSolid slot="icon" class="w-5 h-5" />
    <b>Product Not Found. Please read ingredients.</b>
</Alert>