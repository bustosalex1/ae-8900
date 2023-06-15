<script lang="ts">
    import Icon from '$lib/components/general/Icon.svelte'
    import { get, type ProjectConfiguration, apiCall } from '$lib/api'
    import { onMount } from 'svelte'
    import ProjectCard from '$lib/components/general/ProjectCard.svelte'
    import { projectState } from '$lib/stores'

    let projects: ProjectConfiguration[] | undefined = undefined

    onMount(async () => {
        projects = await apiCall(get('/projects/', {}))
    })
</script>

<div class="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-6 xl:grid-cols-8 gap-4 items-center p-4">
    {#if projects}
        {#each projects as project}
            <ProjectCard {project} />
        {/each}
    {/if}

    <div
        class="flex flex-col items-center w-full h-full border border-1 border-dashed rounded-2xl justify-center py-20"
    >
        <a
            href="/project"
            class="btn btn-circle btn-outline"
            on:click={() => {
                projectState.set({
                    title: 'New Project',
                    vertical: false,
                    panels: [
                        {
                            title: 'New Panel',
                            components: []
                        }
                    ]
                })
            }}><Icon name="plus" /></a
        >
        <p class="text-lg font-bold">Create New Project</p>
    </div>
</div>
