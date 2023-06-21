<script lang="ts">
    import type { ProjectState } from '$lib/api'
    import { setActiveProject } from '$lib/stores'
    import FormattedDate from './FormattedDate.svelte'
    import Icon from './Icon.svelte'

    export let state: ProjectState
</script>

<a
    href="/project"
    on:click={() => {
        setActiveProject(state)
    }}
>
    <div
        class="transition ease-in-out card w-full bg-base-100 shadow-xl hover:shadow-2xl hover:-translate-y-1 duration-300 ring-1 ring-neutral-400 h-full group"
    >
        <figure>
            <div
                class="w-full h-48 bg-gradient-to-br from-primary via-secondary to-white flex flex-col justify-center align-middle text-5xl font-black items-center"
            >
                <Icon name="hard-drive" />
            </div>
        </figure>
        <div class="p-3 card-body">
            <h2
                class="leading-tight text-md font-bold group-hover:text-primary transition ease-in-out duration-300"
            >
                {state.configuration.title}
            </h2>
            <p class="text-sm">{state.configuration.description}</p>
            <div class="card-actions justify-end">
                {#if state.metadata}
                    <FormattedDate
                        date={new Date(state.metadata.last_modified)}
                        prefix="Modified"
                    />
                {/if}
            </div>
        </div>
    </div>
</a>
