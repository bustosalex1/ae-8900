<script lang="ts">
    import { slide } from 'svelte/transition'
    import Icon from '../general/Icon.svelte'
    import GeneralSettings from '../dashboard/settings/GeneralSettings.svelte'
    import type { ComponentConfiguration, PanelConfiguration } from '$lib/api'

    // props
    export let componentConfiguration: ComponentConfiguration
    export let panelConfiguration: PanelConfiguration

    // component state
    let settings = false

    // callback to toggle expanded state
    const toggle = () => {
        componentConfiguration.expanded = !componentConfiguration.expanded
        settings = false
    }
</script>

<div class="w-full rounded-md ring-1 ring-neutral-400 p-2 shadow-md">
    <div class="w-full flex flex-row gap-1">
        <button class="w-full text-left flex flex-row items-center" on:click={toggle}>
            <input
                type="text"
                class="font-bold bg-transparent"
                bind:value={componentConfiguration.title}
                on:click|stopPropagation
                on:keyup|preventDefault
            />
        </button>

        <div class="flex flex-row gap-1 items-center">
            {#if componentConfiguration.expanded}
                <button
                    class="btn btn-xs btn-circle btn-ghost"
                    transition:slide={{ axis: 'x', duration: 500 }}
                    on:click={() => {
                        const index = panelConfiguration.components.indexOf(componentConfiguration)

                        if (index > -1) {
                            panelConfiguration.components.splice(index, 1)
                            panelConfiguration = panelConfiguration
                        }
                    }}
                >
                    <Icon name="x" class="feather" />
                </button>
                <button
                    class="btn btn-xs btn-circle btn-ghost"
                    transition:slide={{ axis: 'x', duration: 500 }}
                    on:click={() => (settings = !settings)}
                >
                    <Icon name="edit" class="feather" />
                </button>
            {/if}
            <button on:click={toggle} class="btn btn-xs btn-circle btn-ghost">
                <Icon name={componentConfiguration.expanded ? 'chevron-up' : 'chevron-down'} />
            </button>
        </div>
    </div>
    {#if componentConfiguration.expanded && !settings}
        <div transition:slide|local={{ duration: 500 }}>
            <slot />
        </div>
    {:else if settings && componentConfiguration.settings}
        <div>
            <GeneralSettings bind:componentSettings={componentConfiguration.settings} />
        </div>
    {/if}
</div>
