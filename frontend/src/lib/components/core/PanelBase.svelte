<script lang="ts">
    import Icon from '$lib/components/general/Icon.svelte'
    import { fly } from 'svelte/transition'
    import DashboardComponent from './DashboardComponent.svelte'
    import type { PanelConfiguration } from '$lib/api'
    import Modal from './Modal.svelte'
    import { dashboardMap } from '$lib/stores'
    export let configuration: PanelConfiguration

    let newComponent = Object.keys(dashboardMap)[0]

    let modal = false
    const addComponent = () => {
        configuration.components = [
            ...configuration.components,
            {
                title: 'New Component',
                component: newComponent
            }
        ]
    }
</script>

<div class="ring-2 ring-base-200 p-1 sticky flex flex-row justify-between items-center">
    <input type="text" class="font-bold bg-transparent" bind:value={configuration.title} />
    <button class="btn btn-circle btn-xs btn-ghost" on:click={() => (modal = !modal)}>
        <Icon name="plus" />
    </button>
</div>
<div class="flex flex-col gap-2 h-screen overflow-y-scroll overflow-x-hidden p-2 pb-20">
    {#each configuration.components as componentConfiguration}
        <div transition:fly={{ y: -10, duration: 350 }}>
            <DashboardComponent {componentConfiguration}>
                <svelte:component this={dashboardMap[componentConfiguration.component]} />
            </DashboardComponent>
        </div>
    {/each}
</div>

{#if modal}
    <Modal>
        <select class="select select-bordered w-full max-w-xs" bind:value={newComponent}>
            {#each Object.entries(dashboardMap) as [dashboardComponent]}
                <option>{dashboardComponent}</option>
            {/each}
        </select>
        <button
            class="btn"
            disabled={newComponent === undefined}
            on:click={() => {
                addComponent()
                modal = false
            }}>Add Component</button
        >
    </Modal>
{/if}
