<script lang="ts">
    import Icon from '$lib/components/general/Icon.svelte'
    import { fade } from 'svelte/transition'
</script>

<div
    class="join join-horizontal mx-4 outline outline-1 outline-neutral-400"
    transition:fade={{ duration: 300 }}
>
    <div class="tooltip tooltip-bottom" data-tip="Save Changes">
        <button class="btn btn-sm join-item btn-disabled">
            <Icon name="save" />
        </button>
    </div>

    <button class="btn btn-sm join-item"><Icon name="rotate-ccw" /></button>
    <button class="btn btn-sm join-item btn-disabled"><Icon name="database" /></button>
    <button class="btn btn-sm join-item"><Icon name="plus" /></button>
    <button class="btn btn-sm join-item"><Icon name="minus" /></button>
</div>
