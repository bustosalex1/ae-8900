<script lang="ts">
    import { Pane, Splitpanes } from 'svelte-splitpanes'
    import PanelBase from '$lib/components/core/PanelBase.svelte'
    import { projectState } from '$lib/stores'
</script>

<Splitpanes theme="custom-theme" horizontal={!$projectState.vertical}>
    {#each $projectState.panels as panel}
        <Pane>
            <PanelBase bind:configuration={panel} />
        </Pane>
    {/each}
</Splitpanes>
