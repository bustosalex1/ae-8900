<script lang="ts">
	import type { ComponentConfiguration } from '$lib/api';
	export let componentConfiguration: ComponentConfiguration;
</script>

<div>
	<div class="form-control w-full max-w-xs">
		<label class="label">
			<span class="label-text">Component Name</span>
			<input
				type="text"
				class="input input-bordered w-full max-w-xs"
				bind:value={componentConfiguration.title}
			/>
		</label>
	</div>
</div>
