<script lang="ts">
    import { stagedState, applyProjectChanges, revertProjectChanges } from '$lib/stores'
    import type { KeyFilter, ProjectConfiguration } from '$lib/api'

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
                    <input
                        type="text"
                        class="input input-lg input-bordered"
                        bind:value={$stagedState.configuration[value]}
                    />
                </label>
            {/each}
        </div>

        <div class="flex flex-row gap-2 w-full justify-end py-2">
            <button class="btn btn-ghost" on:click={revertProjectChanges}>Discard Changes</button>
            <button class="btn" on:click={applyProjectChanges}>Apply Changes</button>
        </div>
    </div>
</div>
