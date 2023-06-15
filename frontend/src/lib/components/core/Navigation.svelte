<script lang="ts">
    import ThemeToggle from '$lib/components/general/ThemeToggle.svelte'
    import Icon from '$lib/components/general/Icon.svelte'
    import ProjectSettings from '../dashboard/settings/ProjectSettings.svelte'
    import { projectState } from '$lib/stores'
    import { page } from '$app/stores'
</script>

<div class="navbar bg-base-200 px-5">
    <div class="flex-1">
        <a class="hover:text-primary transition duration-300" href="/">
            <Icon name="zap" class="feather mr-1" />
        </a>
        <div class="text-xl font-bold">
            Alex's AE 8900 Project{$page.route?.id === '/project'
                ? ` / ${$projectState.title}`
                : ''}
        </div>
    </div>

    <div class="join join-horizontal p-2">
        <button
            class="btn btn-sm join-item"
            on:click={() =>
                projectState.update((state) => {
                    state.panels.push({ title: 'New Panel', components: [] })
                    return state
                })}><Icon name="plus" /></button
        >
        <button
            class="btn btn-sm join-item"
            on:click={() =>
                projectState.update((state) => {
                    state.panels.pop()
                    return state
                })}><Icon name="minus" /></button
        >
    </div>

    {#if $page.route?.id === '/project'}
        <ProjectSettings />
    {/if}
    <div class="flex-none">
        <ThemeToggle />
    </div>
</div>
