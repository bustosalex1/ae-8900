<script lang="ts">
	import ThemeToggle from '$lib/components/general/ThemeToggle.svelte';
	import Icon from '$lib/components/general/Icon.svelte';
</script>

<div class="navbar bg-base-200 px-5">
	<div class="flex-1">
		<Icon name="zap" class="feather mr-1" />
		<div class="text-xl font-bold">Alex's AE 8900 Project</div>
	</div>
	<div class="flex-none">
		<ThemeToggle />
	</div>
</div>
