<script lang="ts">
    import type { ComponentSettings } from '$lib/api'
    import DataSelector from '$lib/components/core/DataSelector.svelte'
    export let componentSettings: ComponentSettings
</script>

<div class="form-control flex flex-col gap-2">
    <div class="font-bold">Data Sources</div>
    <DataSelector bind:componentSettings />
</div>
