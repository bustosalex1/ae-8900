<script lang="ts">
	import '../app.css';
	import ThemeToggle from '$lib/components/general/ThemeToggle.svelte';
</script>

<div class="w-[100vw] h-[100vh]">
	<div class="navbar bg-base-200 px-5">
		<div class="flex-1">
			<div class="text-xl font-bold">Alex's AE 8900 Project</div>
		</div>
		<button class="btn animate-none mx-1">
			<div class="flex flex-row gap-1">
				<div>
					<kbd class="kbd font-bold">⌘</kbd>
				</div>
				<kbd class="kbd">K</kbd>
			</div>
		</button>
		<div class="flex-none">
			<ThemeToggle />
		</div>
	</div>
	<slot />
</div>
