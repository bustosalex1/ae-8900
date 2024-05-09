<script lang="ts">
    import { fly, fade } from 'svelte/transition'
    import { cubicInOut } from 'svelte/easing'

    export let dim: boolean | undefined = undefined
</script>

<div
    class="fixed top-0 left-0 h-screen w-screen flex items-center justify-center z-50"
    class:bg-black={dim}
    class:bg-opacity-80={dim}
    transition:fade|local={{ duration: 250 }}
>
    <div
        transition:fly|local={{ duration: 250, y: 50, easing: cubicInOut }}
        class="rounded-md bg-base-100 p-2 ring-1 ring-neutral-400"
    >
        <slot />
    </div>
</div>
