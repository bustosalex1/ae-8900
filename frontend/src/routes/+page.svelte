<script lang="ts">
    import Icon from '$lib/components/general/Icon.svelte'
    import { get, apiCall, type ProjectState } from '$lib/api'
    import { onMount } from 'svelte'
    import ProjectCard from '$lib/components/general/ProjectCard.svelte'
    import { projectState, revertProjectChanges } from '$lib/stores'

    let projects: ProjectState[] | undefined = undefined

    onMount(async () => {
        projects = await apiCall(get('/projects', {}))
    })
</script>

<div class="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-6 xl:grid-cols-8 gap-4 p-4">
    {#if projects}
        {#each projects as state}
            <ProjectCard {state} />
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
                    configuration: {
                        title: 'New Project',
                        description: 'A new project.',
                        vertical: true,
                        panels: [
                            {
                                title: 'New Panel',
                                components: []
                            }
                        ]
                    },
                    metadata: undefined
                })
                revertProjectChanges()
            }}><Icon name="plus" /></a
        >
        <p class="text-lg font-bold">Create New Project</p>
    </div>
</div>
