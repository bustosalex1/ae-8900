<script lang="ts">
    import type { ComponentSettings } from '$lib/api'
    import Icon from '$lib/components/general/Icon.svelte'
    import { connectionManager } from '$lib/websocket/connectionManager'
    export let componentSettings: ComponentSettings

    const dataSources = connectionManager.sources()
</script>

<div>
    <div class="form-control flex flex-col gap-2">
        <div class="font-bold">Data Sources</div>
        {#each componentSettings.data_sources as dataSource, index}
            <div class="flex flex-row gap-2">
                <select class="select select-sm select-bordered" bind:value={dataSource}>
                    {#each dataSources as source}
                        <option>{source}</option>
                    {/each}
                </select>
                <button
                    class="btn btn-sm btn-circle btn-ghost"
                    on:click={() => {
                        componentSettings.data_sources.splice(index, 1)
                        componentSettings = componentSettings
                    }}
                >
                    <Icon name="x" />
                </button>
            </div>
        {/each}
        <button
            class="btn btn-sm"
            on:click={() => {
                componentSettings.data_sources = [...componentSettings.data_sources, dataSources[0]]
            }}>Add Source</button
        >
    </div>
</div>
