<script lang="ts">
    import ThemeToggle from '$lib/components/general/ThemeToggle.svelte'
    import Icon from '$lib/components/general/Icon.svelte'
    import ProjectSettings from '../dashboard/settings/ProjectSettings.svelte'
    import { stagedState } from '$lib/stores'
    import { page } from '$app/stores'
    import { fly } from 'svelte/transition'
    import { cubicInOut } from 'svelte/easing'
</script>

<div class="navbar bg-base-200 px-5">
    <div class="flex-1">
        <a class="hover:text-primary transition duration-300" href="/">
            <Icon name="zap" class="feather mr-1" />
        </a>
        <div class="text-xl font-bold">Alex's AE 8900 Project</div>
        {#if $page.route?.id && $page.route.id.includes('project')}
            <div class="divider divider-horizontal mx-1" />
            <input
                type="text"
                class="input input-sm bg-none text-xl font-bold input-ghost w-min p-0 m-0 bg-transparent"
                bind:value={$stagedState.configuration.title}
                transition:fly={{ x: -5, duration: 350, easing: cubicInOut }}
            />
        {/if}
    </div>

    {#if $page.route?.id && $page.route.id.includes('project')}
        <ProjectSettings />
    {/if}
    <div class="flex-none">
        <ThemeToggle />
    </div>
</div>
