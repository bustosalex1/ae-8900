<script lang="ts">
	import Icon from '$lib/components/general/Icon.svelte';
	import LineChart from '$lib/components/visualization/LineChart.svelte';
	import { fly } from 'svelte/transition';
	import DashboardComponent from './DashboardComponent.svelte';
	import ReactiveChart from '../visualization/ReactiveChart.svelte';

	let components: any[] = [];

	const addComponent = () => {
		console.log('trying to add a component...');
		components.push(ReactiveChart);
		components = components;
	};
</script>

<div class="ring-2 ring-base-200 p-1 sticky flex flex-row justify-between items-center">
	<input
		type="text"
		placeholder="Panel"
		class="font-bold bg-none input input-ghost p-0 h-[1rem] w-min"
	/>
	<button class="btn btn-circle btn-xs btn-ghost" on:click={addComponent}>
		<Icon name="plus" />
	</button>
</div>
<div class="flex flex-col gap-2 max-h-screen overflow-y-scroll overflow-x-hidden p-2 pb-20">
	{#each components as component}
		<div transition:fly={{ y: -10, duration: 350 }}>
			<DashboardComponent>
				<svelte:component this={component} />
			</DashboardComponent>
		</div>
	{/each}
</div>
