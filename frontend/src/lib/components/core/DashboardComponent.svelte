<script lang="ts">
	import { fly, slide } from 'svelte/transition';
	import Icon from '../general/Icon.svelte';
	let expanded = false;

	const toggle = () => {
		expanded = !expanded;
	};
</script>

<div class="w-full rounded-md ring-1 ring-neutral-400 p-2 shadow-md">
	<div class="w-full flex flex-row items-center gap-1">
		<button class="w-full text-left" on:click={toggle}>
			<p class="font-bold">Component</p>
		</button>
		{#if expanded}
			<button transition:fly={{ x: 10, duration: 500 }}>
				<Icon name="edit" class="feather" />
			</button>
		{/if}
		<button on:click={toggle}>
			<Icon name={expanded ? 'minus' : 'plus'} />
		</button>
	</div>
	{#if expanded}
		<div transition:slide={{ duration: 500 }}>
			<slot />
		</div>
	{/if}
</div>
