<script lang="ts">
	import { fly, slide } from 'svelte/transition';
	import Icon from '../general/Icon.svelte';
	import LineChartSettings from '../visualization/settings/LineChartSettings.svelte';
	export let title: string;
	let expanded: 'component' | 'settings' | 'none' = 'none';

	const setExpanded = (value: 'component' | 'settings' | 'none') => {
		expanded = value;
	};

	const toggle = () => {
		if (expanded === 'component' || expanded === 'settings') {
			expanded = 'none';
		} else {
			expanded = 'component';
		}
	};
</script>

<div class="w-full rounded-md ring-1 ring-neutral-400 p-2 shadow-md">
	<div class="w-full flex flex-row items-center gap-1">
		<button class="w-full text-left" on:click={toggle}>
			<p class="font-bold">{title}{expanded === 'settings' ? ' / Settings' : ''}</p>
		</button>
		{#if expanded !== 'none'}
			<button transition:fly={{ x: 10, duration: 500 }} on:click={() => setExpanded('settings')}>
				<Icon name="edit" class="feather" />
			</button>
		{/if}
		<button on:click={toggle}>
			<Icon name={expanded === 'component' ? 'chevron-up' : 'chevron-down'} />
		</button>
	</div>
	{#if expanded === 'component'}
		<div transition:slide={{ duration: 500 }}>
			<slot />
		</div>
	{:else if expanded === 'settings'}
		<div>
			<LineChartSettings />
		</div>
	{/if}
</div>
