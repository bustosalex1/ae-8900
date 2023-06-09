<script lang="ts">
	import '../app.css';
	import ThemeToggle from '$lib/components/ThemeToggle.svelte';
</script>

<div class="w-[100vw] h-[100vh]">
	<div class="navbar bg-base-200 px-5">
		<div class="flex-1">
			<div class="text-xl font-bold">Alex's AE 8900 Project</div>
		</div>
		<div class="flex-none">
			<ThemeToggle />
		</div>
	</div>
	<slot />
</div>
