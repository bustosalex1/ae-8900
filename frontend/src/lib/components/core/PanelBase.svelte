<script lang="ts">
	import Icon from '$lib/components/general/Icon.svelte';
	import { fly } from 'svelte/transition';
	import DashboardComponent from './DashboardComponent.svelte';
	import type { PanelConfiguration } from '$lib/types';
	import LineChart from '../visualization/LineChart.svelte';
	export let configuration: PanelConfiguration;

	const addComponent = () => {
		configuration.components = [
			...configuration.components,
			{ title: 'New Component', component: LineChart, props: {} }
		];
	};
</script>

<div class="ring-2 ring-base-200 p-1 sticky flex flex-row justify-between items-center">
	<p class="font-bold">{configuration.title}</p>
	<button class="btn btn-circle btn-xs btn-ghost" on:click={addComponent}>
		<Icon name="plus" />
	</button>
</div>
<div class="flex flex-col gap-2 max-h-screen overflow-y-scroll overflow-x-hidden p-2 pb-20">
	{#each configuration.components as { title, component }}
		<div transition:fly={{ y: -10, duration: 350 }}>
			<DashboardComponent {title}>
				<svelte:component this={component} />
			</DashboardComponent>
		</div>
	{/each}
</div>
