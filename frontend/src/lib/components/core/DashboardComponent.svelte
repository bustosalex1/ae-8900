<script lang="ts">
    import { fly, slide } from 'svelte/transition'
    import Icon from '../general/Icon.svelte'
    import GeneralSettings from '../dashboard/settings/GeneralSettings.svelte'
    import type { ComponentConfiguration } from '$lib/api'

    // props
    export let componentConfiguration: ComponentConfiguration

    // component state
    let settings = false

    // callback to toggle expanded state
    const toggle = () => {
        componentConfiguration.expanded = !componentConfiguration.expanded
        settings = false
    }
</script>

<div class="w-full rounded-md ring-1 ring-neutral-400 p-2 shadow-md">
    <div class="w-full flex flex-row items-center gap-1">
        <button class="w-full text-left flex flex-row" on:click={toggle}>
            <input
                type="text"
                class="font-bold bg-transparent"
                bind:value={componentConfiguration.title}
                on:click|stopPropagation
                on:keyup|preventDefault
            />
        </button>
        {#if componentConfiguration.expanded}
            <div class="tooltip tooltip-left tooltip-primary z-50" data-tip="Edit">
                <button
                    transition:fly|local={{ x: 10, duration: 500 }}
                    on:click={() => (settings = !settings)}
                >
                    <Icon name="edit" class="feather" />
                </button>
            </div>
        {/if}
        <button on:click={toggle}>
            <Icon name={componentConfiguration.expanded ? 'chevron-up' : 'chevron-down'} />
        </button>
    </div>
    {#if componentConfiguration.expanded && !settings}
        <div transition:slide|local={{ duration: 500 }}>
            <slot />
        </div>
    {:else if settings}
        <div>
            <GeneralSettings bind:componentConfiguration />
        </div>
    {/if}
</div>
