<script lang="ts">
	import { Pane, Splitpanes } from 'svelte-splitpanes';
	import Icon from '$lib/components/general/Icon.svelte';
	import PanelBase from '$lib/components/core/PanelBase.svelte';
	import { projectState } from '$lib/stores';
</script>

<Splitpanes theme="custom-theme" horizontal={!$projectState.vertical}>
	<Pane minSize={20}>
		<div class="join join-horizontal p-2">
			<button
				class="btn btn-sm join-item"
				on:click={() =>
					projectState.update((state) => {
						state.panels.push({ title: 'new panel', components: [] });
						return state;
					})}><Icon name="plus" /></button
			>
			<button
				class="btn btn-sm join-item"
				on:click={() =>
					projectState.update((state) => {
						state.panels.pop();
						return state;
					})}><Icon name="minus" /></button
			>
		</div>
	</Pane>

	{#each $projectState.panels as panel}
		<Pane>
			<PanelBase bind:configuration={panel} />
		</Pane>
	{/each}
</Splitpanes>
