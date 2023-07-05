<script lang="ts">
    import { connectionManager } from '$lib/websocket/connectionManager'
    import type { ComponentSettings, MessageConfiguration } from '$lib/api'
    import { onMount } from 'svelte'
    import Icon from '../general/Icon.svelte'

    export let componentSettings: ComponentSettings

    let dataSources: MessageConfiguration[] = []
    let newSource: MessageConfiguration

    onMount(async () => {
        const sources = await connectionManager.sources()

        if (sources) {
            dataSources = sources
            newSource = dataSources[0]
        }
    })
</script>

<div class="flex flex-col gap-2">
    <!--message list-->
    {#each componentSettings.data_sources as source, index}
        <div class="ring-1 ring-neutral-200 rounded-md p-2">
            <div class="flex flex-row justify-between">
                <div class="text-md font-bold">
                    {source.header.name}
                </div>
                <button
                    class="btn btn-ghost btn-xs btn-circle"
                    on:click={() => {
                        componentSettings.data_sources.splice(index, 1)
                        componentSettings = componentSettings
                    }}
                >
                    <Icon name="x" />
                </button>
            </div>
            <div class="max-h-52 overflow-y-scroll flex flex-col gap-2">
                <!--fields within each message-->
                {#each source.payload as field}
                    <div class="flex flex-row gap-1">
                        <input
                            type="checkbox"
                            class="checkbox checkbox-sm"
                            bind:checked={field.enabled}
                        />
                        <div class="text-sm">
                            {field.name}
                            {field.units ? `(${field.units})` : '(no units)'}
                        </div>
                    </div>
                {/each}
            </div>
        </div>
    {/each}

    <!-- add new source button -->
    <div class="join">
        <select class="select select-bordered join-item w-full" bind:value={newSource}>
            {#each dataSources as source}
                <option value={source}>{source.header.name}</option>
            {/each}
        </select>
        <button
            class="btn join-item"
            on:click={() => {
                componentSettings.data_sources = [...componentSettings.data_sources, newSource]
            }}>Add Source</button
        >
    </div>
</div>
