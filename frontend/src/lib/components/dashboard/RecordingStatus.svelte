<script lang="ts">
    import { apiCall, get, post, type ComponentSettings } from '$lib/api'
    import { onMount } from 'svelte'
    import Icon from '../general/Icon.svelte'

    export let settings: ComponentSettings

    // parameters required to start a new recording
    let streams: Record<string, boolean> = {}
    let recordingFrequency = 0

    // just a helpful indicator, i think
    let canRecord = false

    $: canRecord =
        recordingFrequency > 0 &&
        Object.keys(streams).filter((stream) => streams[stream]).length > 0

    // list all the available data sources when the component mounts
    onMount(async () => {
        const result = await apiCall(get('/data_sources', {}))
        if (result) {
            result.forEach((stream) => {
                streams[stream] = false
                streams = streams
            })
        }

        console.log(`RecordingStatus has unused ${settings} right now :)`)
    })

    // kick of a recording with the parameters the user has specified when the `record` button is clicked
    const onRecord = () => {
        const sources = Object.keys(streams).filter((stream) => streams[stream])
        console.log(sources)
        console.log(1 / recordingFrequency)
        apiCall(
            post('/start_recording', {
                body: {
                    sources: sources,
                    interval: 1 / recordingFrequency
                }
            })
        )
    }

    const onStop = () => {
        apiCall(post('/stop_recording', {}))
    }
</script>

<!--outer container-->
<div class="flex flex-row gap-4">
    <!-- data sources -->
    <div class="flex flex-col">
        <div class="text-md">Sources</div>
        <div class="overflow-y-scroll rounded-md p-2 max-h-52 ring-1 ring-base-200">
            {#each Object.entries(streams) as [stream]}
                <div class="form-control w-min">
                    <label class="label cursor-pointer flex flex-row gap-2">
                        <input
                            type="checkbox"
                            class="checkbox checkbox-md"
                            bind:checked={streams[stream]}
                        />
                        <span class="text-md">{stream}</span>
                    </label>
                </div>
            {/each}
        </div>
    </div>
    <!-- controls and recording frequency container -->
    <div class="flex flex-col gap-4">
        <!-- controls container -->
        <div class="flex flex-col">
            <div class="text-md">Controls</div>
            <div class="join join-horizontal">
                <button
                    class="btn btn-md join-item w-1/2"
                    disabled={!canRecord}
                    on:click={onRecord}
                >
                    <Icon
                        name="circle"
                        class="w-[20px] h-[20px] fill-red-500 stroke-2 stroke-red-500"
                    /> Record
                </button>
                <button class="btn btn-md join-item w-1/2" on:click={onStop}>
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
