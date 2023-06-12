<script lang="ts">
	import { slide } from 'svelte/transition';

	let ws = new WebSocket('ws://localhost:8000/ws');

	ws.onmessage = (event) => {
		receivedMessages.push(JSON.parse(event.data));
		receivedMessages = receivedMessages;
	};

	const sendMessage = () => {
		ws.send(message);
		message = '';
	};

	let message = '';
	let receivedMessages: any[] = [];

	$: if (receivedMessages.length > 5) {
		receivedMessages.shift();
	}

	import { flip } from 'svelte/animate';
	import { dndzone } from 'svelte-dnd-action';
	let items = [
		{ id: 1, name: 'item1' },
		{ id: 2, name: 'item2' },
		{ id: 3, name: 'item3' },
		{ id: 4, name: 'item4' }
	];
	const flipDurationMs = 300;
	function handleDndConsider(e) {
		items = e.detail.items;
	}
	function handleDndFinalize(e) {
		items = e.detail.items;
	}
</script>

<h1 class="text-xl">WebSocket Chat</h1>
<form>
	<input type="text" bind:value={message} class="input input-xs input-bordered" />
	<button class="btn btn-sm" on:click={sendMessage}>Send</button>
</form>

<ul>
	{#each receivedMessages as message}
		<li transition:slide={{ axis: 'y', duration: 300 }}>{new Date(message.timestamp * 1000)}</li>
	{/each}
</ul>
<section
	use:dndzone={{ items, flipDurationMs }}
	on:consider={handleDndConsider}
	on:finalize={handleDndFinalize}
>
	{#each items as item (item.id)}
		<div animate:flip={{ duration: flipDurationMs }}>{item.name}</div>
	{/each}
</section>

<style>
	section {
		width: 50%;
		padding: 0.3em;
		border: 1px solid black;
		/* this will allow the dragged element to scroll the list */
		overflow: scroll;
		height: 200px;
	}
	div {
		width: 50%;
		padding: 0.2em;
		border: 1px solid blue;
		margin: 0.15em 0;
	}
</style>
