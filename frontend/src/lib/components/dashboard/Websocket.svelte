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
