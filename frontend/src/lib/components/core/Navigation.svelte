<script lang="ts">
	import ThemeToggle from '$lib/components/general/ThemeToggle.svelte';
	import Icon from '$lib/components/general/Icon.svelte';
</script>

<div class="navbar bg-base-200 px-5">
	<div class="flex-1">
		<Icon name="zap" class="feather mr-1"/>
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
