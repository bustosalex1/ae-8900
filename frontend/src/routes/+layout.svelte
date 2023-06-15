<script lang="ts">
    import '../app.css'
    import Navigation from '$lib/components/core/Navigation.svelte'
</script>

<div class="w-screen h-screen overflow-clip">
    <Navigation />
    <div class="h-full">
        <slot />
    </div>
</div>
