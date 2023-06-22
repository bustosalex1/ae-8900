<script lang="ts">
    import Icon from '$lib/components/general/Icon.svelte'
    import DashboardComponent from './DashboardComponent.svelte'
    import Modal from './Modal.svelte'
    import type { PanelConfiguration } from '$lib/api'
    import { fly } from 'svelte/transition'
    import { stagedState } from '$lib/stores'
    import { componentRegistry } from '../dashboard'

    // each panel gets passed a configuration
    export let configuration: PanelConfiguration

    let modal = false
    let newComponent = ''

    const addComponent = () => {
        configuration.components = [
            ...configuration.components,
            {
                title: 'New Component',
                component: newComponent,
                expanded: false,
                settings: {
                    data_sources: []
                }
            }
        ]
    }
</script>

<div class="ring-2 ring-base-200 p-1 sticky flex flex-row justify-between items-center">
    <input type="text" class="font-bold bg-transparent" bind:value={configuration.title} />

    <div class="flex flex-row gap-1">
        <button
            class="btn btn-circle btn-xs btn-ghost"
            on:click={() => {
                const index = $stagedState.configuration.panels.indexOf(configuration)
                if (index > -1) {
                    stagedState.update((state) => {
                        state.configuration.panels.splice(index, 1)
                        return state
                    })
                }
            }}><Icon name="x" /></button
        >
        <button class="btn btn-circle btn-xs btn-ghost" on:click={() => (modal = !modal)}>
            <Icon name="plus" />
        </button>
    </div>
</div>
<div class="flex flex-col gap-2 h-screen overflow-y-scroll overflow-x-hidden p-2 pb-20">
    {#each configuration.components as componentConfiguration}
        <div in:fly={{ y: -10, duration: 350 }}>
            <DashboardComponent {componentConfiguration}>
                <svelte:component
                    this={componentRegistry[componentConfiguration.component]}
                    settings={componentConfiguration.settings}
                />
            </DashboardComponent>
        </div>
    {/each}
</div>

{#if modal}
    <Modal dim={true}>
        <div class="flex flex-col gap-4 m-4">
            <div class="text-xl font-bold">Add New Component</div>
            <select class="select select-bordered w-full max-w-xs" bind:value={newComponent}>
                {#each Object.entries(componentRegistry) as [dashboardComponent]}
                    <option>{dashboardComponent}</option>
                {/each}
            </select>
            <button
                class="btn"
                disabled={newComponent === ''}
                on:click={() => {
                    addComponent()
                    modal = false
                }}>Add Component</button
            >
        </div>
    </Modal>
{/if}
