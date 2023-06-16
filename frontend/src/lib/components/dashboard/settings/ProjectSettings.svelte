<script lang="ts">
    import Icon from '$lib/components/general/Icon.svelte'
    import { fade } from 'svelte/transition'
    import { applyProjectChanges, revertProjectChanges } from '$lib/stores'
    import { stagedState } from '$lib/stores'
    import type { Setting } from '$lib/types'
    import { goto } from '$app/navigation'
    import { page } from '$app/stores'

    const settings: Setting[] = [
        {
            icon: 'settings',
            label: 'Project Settings',
            callback: async () => {
                if ($page.route?.id === '/project') {
                    await goto('/project/settings')
                } else {
                    await goto('/project')
                }
            }
        },
        {
            icon: 'save',
            label: 'Save Changes',
            callback: applyProjectChanges
        },
        {
            icon: 'rotate-ccw',
            label: 'Revert Changes',
            callback: revertProjectChanges
        },
        {
            icon: 'plus',
            label: 'Add Panel',
            callback: () =>
                stagedState.update((state) => {
                    state.configuration.panels.push({ title: 'New Panel', components: [] })
                    return state
                })
        },
        {
            icon: 'minus',
            label: 'Remove Panel',
            callback: () =>
                stagedState.update((state) => {
                    state.configuration.panels.pop()
                    return state
                })
        }
    ]
</script>

<div
    class="join join-horizontal mx-4 outline outline-1 outline-neutral-400"
    transition:fade={{ duration: 300 }}
>
    {#each settings as { icon, label, callback }}
        <div class="tooltip tooltip-bottom" data-tip={label}>
            <button class="btn btn-sm join-item" on:click={callback}>
                <Icon name={icon} />
            </button>
        </div>
    {/each}
</div>
