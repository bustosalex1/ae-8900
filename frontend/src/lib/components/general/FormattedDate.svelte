<script lang="ts">
    export let date: Date
    export let prefix: string | undefined = undefined
</script>

<div class="text-xs font-mono whitespace-nowrap">
    {#if prefix}
        {`${prefix} `}
    {/if}
    {date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        timeZone: 'UTC'
    })}
</div>
