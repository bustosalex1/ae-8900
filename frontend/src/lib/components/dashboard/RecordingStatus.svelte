<script lang="ts">
    import { apiCall, get, type ComponentSettings } from '$lib/api'
    import { onMount } from 'svelte'
    import Icon from '../general/Icon.svelte'

    export let settings: ComponentSettings

    let streams: string[] | undefined

    onMount(async () => {
        streams = await apiCall(get('/data_sources', {}))
        console.log(`RecordingStatus has unused ${settings} right now :)`)
    })
</script>

<div class="flex flex-col gap-4">
    <div class="flex flex-col">
        <div class="font-bold">Controls</div>
        <div class="join join-horizontal">
            <button class="btn btn-square btn-md join-item"> <Icon name="circle" /> </button>
            <button class="btn btn-square btn-md join-item"> <Icon name="square" /> </button>
        </div>
    </div>
    <div class="flex flex-row gap-4 items-start align-top">
        <div class="flex flex-col">
            <div class="font-bold">Data Sources</div>
            <div class="flex flex-row">
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
        <div class="flex flex-col">
            <div class="font-bold">Recording Frequency</div>
            <input type="number" class="input input-bordered" />
        </div>
    </div>
</div>
