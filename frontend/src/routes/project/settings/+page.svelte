<script lang="ts">
    import {
        stagedState,
        applyProjectChanges,
        revertProjectChanges,
        projectState
    } from '$lib/stores'
    import Icon from '$lib/components/general/Icon.svelte'
    import { apiCall, del, type KeyFilter, type ProjectConfiguration } from '$lib/api'
    import Modal from '$lib/components/core/Modal.svelte'
    import { goto } from '$app/navigation'
    let modal = false

    type ToggleSetting = {
        label: string
        value: KeyFilter<ProjectConfiguration, boolean>
    }

    type TextSetting = {
        label: string
        value: KeyFilter<ProjectConfiguration, string>
    }

    const toggles: ToggleSetting[] = [
        {
            label: 'Vertical Layout',
            value: 'vertical'
        }
    ]

    const textFields: TextSetting[] = [
        {
            label: 'Project Description',
            value: 'description'
        }
    ]
</script>

<div class="p-4">
    <div class="text-xl font-bold">Settings</div>
    <div class="max-w-xl">
        <div class="form-control">
            {#each toggles as { label, value }}
                <label class="label cursor-pointer pl-0">
                    <span>{label}</span>
                    <input
                        type="checkbox"
                        class="toggle"
                        bind:checked={$stagedState.configuration[value]}
                    />
                </label>
            {/each}
        </div>
        <div class="divider divider-vertical my-0" />

        <div class="form-control">
            {#each textFields as { label, value }}
                <label class="label cursor-pointer pl-0">
                    <span>{label}</span>
                    <textarea
                        class="textarea textarea-sm textarea-bordered"
                        bind:value={$stagedState.configuration[value]}
                    />
                </label>
            {/each}
        </div>

        <div class="divider divider-vertical my-0" />
        <div class="form-control">
            <div class="text-xl font-bold">Danger Zone</div>
            <button class="btn btn-error my-2" on:click={() => (modal = !modal)}>
                <Icon name="x-circle" />
                Delete Project</button
            >
        </div>
        <div class="flex flex-row gap-2 w-full justify-end py-2">
            <button class="btn btn-ghost" on:click={revertProjectChanges}>Discard Changes</button>
            <button class="btn" on:click={applyProjectChanges}>Apply Changes</button>
        </div>
    </div>
</div>

{#if modal}
    <Modal dim={true}>
        <div class="p-4">
            <div class="text-2xl font-bold flex flex-row gap-2 items-center">
                <Icon name="alert-triangle" />
                Just so you know...
            </div>
            <p>Deleting a project will delete all project data, configuration, and asset files.</p>
            <div class="flex flex-row w-full justify-end pt-5 gap-2">
                <button class="btn btn-ghost" on:click={() => (modal = !modal)}
                    >Do Not Delete</button
                >
                <button
                    class="btn btn-error"
                    on:click={async () => {
                        await apiCall(del('/project/', { body: $projectState }))
                        goto('/')
                    }}>Delete</button
                >
            </div>
        </div>
    </Modal>
{/if}
