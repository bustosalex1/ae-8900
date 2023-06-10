<script lang="ts">
	import '../app.css';
	import Navigation from '$lib/components/core/Navigation.svelte';
</script>

<div class="h-screen w-screen overflow-clip">
	<Navigation />
	<slot />
</div>
