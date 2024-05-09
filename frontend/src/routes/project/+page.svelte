<script lang="ts">
    import { Pane, Splitpanes } from 'svelte-splitpanes'
    import PanelBase from '$lib/components/core/PanelBase.svelte'
    import { stagedState } from '$lib/stores'
</script>

<Splitpanes theme="custom-theme" horizontal={!$stagedState.configuration.vertical}>
    {#each $stagedState.configuration.panels as panel}
        <Pane>
            <PanelBase bind:configuration={panel} />
        </Pane>
    {/each}
</Splitpanes>
