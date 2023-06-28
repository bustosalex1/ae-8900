<script lang="ts">
    import { apiCall, get, type ComponentSettings } from '$lib/api'
    import { onMount } from 'svelte'
    import Icon from '../general/Icon.svelte'

    export let settings: ComponentSettings

    let streams: string[] | undefined
    let canRecord = false

    let recordingFrequency = 0

    $: canRecord = recordingFrequency <= 0

    onMount(async () => {
        streams = await apiCall(get('/data_sources', {}))
        console.log(`RecordingStatus has unused ${settings} right now :)`)
    })
</script>

<!--outer container-->
<div class="flex flex-row gap-4">
    <!-- data sources -->
    <div class="flex flex-col">
        <div class="text-md">Sources</div>
        <div class="overflow-y-scroll rounded-md p-2 max-h-52 ring-1 ring-base-200">
            {#if streams}
                {#each streams as stream}
                    <div class="form-control w-min">
                        <label class="label cursor-pointer flex flex-row gap-2">
                            <input type="checkbox" class="checkbox checkbox-md" />
                            <span class="text-md">{stream}</span>
                        </label>
                    </div>
                {/each}
            {/if}
        </div>
    </div>
    <!-- controls and recording frequency container -->
    <div class="flex flex-col gap-4">
        <!-- controls container -->
        <div class="flex flex-col">
            <div class="text-md">Controls</div>
            <div class="join join-horizontal">
                <button class="btn btn-md join-item w-1/2" disabled={canRecord}>
                    <Icon
                        name="circle"
                        class="w-[20px] h-[20px] fill-red-500 stroke-2 stroke-red-500"
                    /> Record
                </button>
                <button class="btn btn-md join-item w-1/2">
                    <Icon
                        name="square"
                        class="w-[20px] h-[20px] fill-base-content stroke-base-content stroke-2"
                    /> Stop
                </button>
            </div>
        </div>
        <!-- recording frequency container -->
        <div class="flex flex-col">
            <div class="text-md">Recording Frequency</div>
            <div class="join join-horizontal">
                <input
                    type="number"
                    class="input input-bordered input-md join-item"
                    bind:value={recordingFrequency}
                />
                <span class="btn no-animation join-item">Hz</span>
            </div>
        </div>
    </div>
</div>
