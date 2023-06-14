<script lang="ts">
	import { fade, fly } from 'svelte/transition';
	import { cubicInOut } from 'svelte/easing';
</script>

<div class="fixed top-0 left-0 h-screen w-screen flex items-center justify-center z-50">
	<div
		transition:fly={{ duration: 250, y: 50, easing: cubicInOut }}
		class="rounded-md bg-base-100 p-2 ring-1 ring-neutral-400"
	>
		<slot />
	</div>
</div>
