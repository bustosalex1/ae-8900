<script lang="ts">
	import { Pane, Splitpanes } from 'svelte-splitpanes';
	import LineChart from '$lib/components/visualization/LineChart.svelte';

	let horizontal = false;
	let panes = 2;
</script>

<Splitpanes theme="custom-theme" {horizontal}>
	<Pane minSize={20}>
		<div class="join join-vertical">
			<button class="btn join-item" on:click={() => (horizontal = !horizontal)}>swap!</button>
			<button class="btn join-item" on:click={() => (panes = panes + 1)}>increment panes</button>
			<button class="btn join-item" on:click={() => (panes = panes - 1)}>decrement panes</button>
		</div>
	</Pane>

	{#each { length: panes } as _, i}
		<Pane>
			<p>Panel {i}</p>
			<LineChart />
		</Pane>
	{/each}
</Splitpanes>
