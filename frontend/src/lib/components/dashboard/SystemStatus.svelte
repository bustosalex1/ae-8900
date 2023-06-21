<script lang="ts">
    import type { ComponentSettings } from '$lib/api'
    import { connectionManager } from '$lib/websocket/connectionManager'
    import { onMount } from 'svelte'
    import { tweened } from 'svelte/motion'

    // comply with dashboard standard.
    export let settings: ComponentSettings

    const cpuStore = connectionManager.getMeasurementStream('CPU')
    const ramStore = connectionManager.getMeasurementStream('RAM')

    const cpuTweened = tweened(0, { duration: 1000 })
    const ramTweened = tweened(0)

    $: $cpuStore && $cpuStore.length > 0 && cpuTweened.set($cpuStore[$cpuStore.length - 1][1])
    $: $ramStore && $ramStore.length > 0 && ramTweened.set($ramStore[$ramStore.length - 1][1])

    onMount(() => {
        console.log(`SystemStatus has unused ${settings} right now :)`)
    })
</script>

<div class="flex flex-col gap-2 m-2">
    <div class="flex flex-row items-center justify-between">
        <p class="whitespace-nowrap">CPU ({$cpuTweened.toFixed(2)}%)</p>
        <progress class="progress w-56" value={$cpuTweened} max="100" />
    </div>
    <div class="flex flex-row items-center justify-between">
        <p class="whitespace-nowrap">RAM</p>
        <progress class="progress w-56" value={$ramTweened} max="100" />
    </div>
</div>
