<script lang="ts">
    import type { ProjectConfiguration } from '$lib/api'
    import { projectState } from '$lib/stores'
    import Icon from './Icon.svelte'

    export let project: ProjectConfiguration
</script>

<a
    href="/project"
    on:click={() => {
        projectState.set(project)
    }}
>
    <div
        class="transition ease-in-out card w-full bg-base-100 shadow-xl hover:shadow-2xl hover:-translate-y-1 duration-300 ring-1 ring-neutral-400 h-full group"
    >
        <figure>
            <div
                class="w-full h-48 bg-gradient-to-br from-primary via-secondary to-white flex flex-col justify-center align-middle text-5xl font-black items-center"
            >
                <Icon name="heart" />
            </div>
        </figure>
        <div class="p-3 card-body">
            <h2
                class="leading-tight text-md font-bold group-hover:text-primary transition ease-in-out duration-300"
            >
                {project.title}
            </h2>
            <p class="text-sm">{project.description}</p>
            <div class="card-actions justify-end">
                Date goes here.
            </div>
        </div>
    </div>
</a>
