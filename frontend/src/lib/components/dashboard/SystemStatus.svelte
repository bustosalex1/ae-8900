<script lang="ts">
    import { connectionManager } from '$lib/websocket/connectionManager'
    import { spring } from 'svelte/motion'

    let cpuStore = connectionManager.measurementQueues.get('CPU')
    let ramStore = connectionManager.measurementQueues.get('RAM')
    let cpu = spring(0, {
        stiffness: 0.05,
        damping: 0.8
    })

    let ram = spring(0, {
        stiffness: 0.05,
        damping: 0.8
    })

    $: {
        let newCPU = $cpuStore?.at($cpuStore.length - 1)

        if (newCPU) {
            cpu.set(newCPU[1])
        }

        let newRAM = $ramStore?.at($ramStore.length - 1)

        if (newRAM) {
            ram.set(newRAM[1])
        }
    }
</script>

<div class="flex flex-col gap-2 m-2">
    <div class="flex flex-row items-center justify-between">
        <p class="whitespace-nowrap">CPU Usage</p>
        <progress class="progress w-52 progress-primary" value={$cpu} max="100" />
    </div>
    <div class="flex flex-row items-center justify-between">
        <p class="whitespace-nowrap">RAM Usage</p>
        <progress class="progress progress-primary w-52" value={$ram} max="100" />
    </div>
</div>
