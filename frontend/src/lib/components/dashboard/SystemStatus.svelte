<script lang="ts">
    import type { ComponentSettings } from '$lib/api'
    import { connectionManager } from '$lib/websocket/connectionManager'
    import { onDestroy } from 'svelte'
    import type { Unsubscriber } from 'svelte/motion'

    // comply with dashboard standard
    export let settings: ComponentSettings

    let values = new Map<string, number>()

    const unsubscribers: Unsubscriber[] = []
    for (const source of settings.data_sources) {
        const stream = connectionManager.getMeasurementStream(source.header.name)
        if (stream) {
            for (const field of source.payload) {
                if (field.enabled) {
                    const tween = stream.latest.get(field.name)
                    if (tween) {
                        unsubscribers.push(
                            tween.subscribe((value) => {
                                values.set(field.name, value)
                                values = values
                            })
                        )
                    }
                }
            }
        }
    }

    onDestroy(() => {
        for (const unsubscribe of unsubscribers) {
            unsubscribe()
        }
    })
</script>

<div class="flex flex-col gap-2 m-2">
    {#each values as [name, value]}
        <div class="flex flex-row items-center justify-between">
            <p class="whitespace-nowrap">{name} {value.toFixed(2)} (%)</p>
            <progress class="progress w-56" {value} max="100" />
        </div>
    {/each}
</div>
