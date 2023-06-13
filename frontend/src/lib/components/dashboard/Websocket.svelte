<script lang="ts">
	import { get } from '$lib/api';

	let items: string[] = [];

	const onClick = async () => {
		const { data, error } = await get('/', {});
		if (data) {
			items = [...items, data.message];
		}

		console.log(data);
		console.log(error);
	};
</script>

<h1 class="text-xl">API Tester</h1>
<button class="btn btn-outline" on:click={onClick}>Test HTTP API</button>
<div>
	{#each items as item}
		<p>{item}</p>
	{/each}
</div>
