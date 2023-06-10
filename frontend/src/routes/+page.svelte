<script lang="ts">
	import { Pane, Splitpanes } from 'svelte-splitpanes';
	import LineChart from '$lib/components/visualization/LineChart.svelte';
	import Icon from '$lib/components/general/Icon.svelte';

	let horizontal = false;
	let panes = 2;
</script>

<Splitpanes theme="custom-theme" {horizontal}>
	<Pane minSize={20}>
		<div class="flex flex-row gap-2">
			<div class="tooltip tooltip-bottom" data-tip="Pivot Panel Layout">
				<button class="btn btn-sm btn-circle btn-ghost" on:click={() => (horizontal = !horizontal)}
					><Icon name="refresh-ccw" /></button
				>
			</div>

			<div class="tooltip tooltip-bottom" data-tip="Increment Panels">
				<button class="btn btn-sm btn-circle btn-ghost" on:click={() => (panes = panes + 1)}
					><Icon name="plus-circle" /></button
				>
			</div>
			<div class="tooltip tooltip-bottom" data-tip="Decrement Panels">
				<button class="btn btn-sm btn-circle btn-ghost" on:click={() => (panes = panes - 1)}
					><Icon name="minus-circle" /></button
				>
			</div>
		</div>
	</Pane>

	{#each { length: panes } as _, i}
		<Pane>
			<p>Panel {i}</p>
			<div data-feather="alert-circle" class="bg-red-300" />
			<LineChart />
		</Pane>
	{/each}
</Splitpanes>
