<script lang="ts">
	import Icon from '$lib/components/general/Icon.svelte';
	import { get, type ProjectConfiguration, apiCall } from '$lib/api';
	import { onMount } from 'svelte';
	import { projectState } from '$lib/stores';

	let projects: ProjectConfiguration[] = [];

	onMount(async () => {
		const data = await apiCall(() => get('/projects/', {}));

		if (data?.data) {
			projects = data.data;
		} else {
		}
	});

	const setProject = (configuration: ProjectConfiguration) => {
		projectState.set(configuration);
	};
</script>

<div class="w-full flex justify-center items-center p-10">
	{#each projects as project}
		<div
			class="transition ease-in-out card w-full bg-base-100 shadow-xl hover:shadow-2xl hover:-translate-y-1 duration-300 ring-1 ring-neutral-400 h-full group"
		>
			<div class="p-3 card-body">
				<h2
					class="leading-tight text-md font-bold group-hover:text-primary transition ease-in-out duration-300"
				>
					{project.title}
				</h2>
				<p class="text-sm">{project.title}</p>
				<div class="card-actions justify-end">
					<a
						href="/project"
						class="btn w-full"
						on:click={() => {
							projectState.set(project);
						}}>Open</a
					>
				</div>
			</div>
		</div>
	{/each}
	<div>
		<Icon class="feather mx-auto" name="coffee" />

		<p class="p-2">I'm working on multiple project support. For now,</p>
		<a href="/project" class="btn w-full">Open Demo</a>
	</div>
</div>
