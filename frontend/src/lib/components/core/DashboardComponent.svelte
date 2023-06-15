<script lang="ts">
    import { fly, slide } from 'svelte/transition'
    import Icon from '../general/Icon.svelte'
    import GeneralSettings from '../dashboard/settings/GeneralSettings.svelte'
    import type { ComponentConfiguration } from '$lib/api'

    // props
    export let componentConfiguration: ComponentConfiguration

    // component state
    let expanded: 'component' | 'settings' | 'none' = 'none'

    // callback to expand the dashboard component, or show settings
    const setExpanded = (value: 'component' | 'settings' | 'none') => {
        expanded = value
    }

    // callback to toggle expanded state
    const toggle = () => {
        if (expanded === 'component' || expanded === 'settings') {
            expanded = 'none'
        } else {
            expanded = 'component'
        }
    }
</script>

<div class="w-full rounded-md ring-1 ring-neutral-400 p-2 shadow-md">
    <div class="w-full flex flex-row items-center gap-1">
        <button class="w-full text-left" on:click={toggle}>
            <p class="font-bold">
                {componentConfiguration.title}{expanded === 'settings' ? ' / Settings' : ''}
            </p>
        </button>
        {#if expanded !== 'none'}
            <div class="tooltip tooltip-left tooltip-primary z-50" data-tip="Edit">
                <button
                    transition:fly={{ x: 10, duration: 500 }}
                    on:click={() => setExpanded('settings')}
                >
                    <Icon name="edit" class="feather" />
                </button>
            </div>
        {/if}
        <button on:click={toggle}>
            <Icon name={expanded === 'component' ? 'chevron-up' : 'chevron-down'} />
        </button>
    </div>
    {#if expanded === 'component'}
        <div transition:slide={{ duration: 500 }}>
            <slot />
        </div>
    {:else if expanded === 'settings'}
        <div>
            <GeneralSettings bind:componentConfiguration />
        </div>
    {/if}
</div>
