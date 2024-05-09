<script lang="ts">
    import { apiCall, post, type ComponentSettings } from '$lib/api'
    import Icon from '../general/Icon.svelte'
    import DataSelector from '../core/DataSelector.svelte'

    export let settings: ComponentSettings

    // parameters required to start a new recording
    let recordingFrequency = 0

    // just a helpful indicator, i think
    let canRecord = false

    $: canRecord = recordingFrequency > 0

    // kick off a recording with the parameters the user has specified when the `record` button is clicked
    const onRecord = () => {
        console.log(1 / recordingFrequency)
        apiCall(
            post('/start_recording', {
                body: {
                    sources: settings.data_sources,
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
        <DataSelector bind:componentSettings={settings} />
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
