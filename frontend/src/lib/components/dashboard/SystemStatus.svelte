<script lang="ts">
    import type { ComponentSettings } from '$lib/api'
    import { ComponentDataManager } from '$lib/websocket/connectionManager'
    import { onDestroy } from 'svelte'
    import { tweened, type Tweened, type Unsubscriber } from 'svelte/motion'

    // comply with dashboard standard.
    export let settings: ComponentSettings

    const dataManager = new ComponentDataManager(settings.data_sources)

    const tweens = new Map<string, Tweened<number>>()

    let tweenValues = new Map<string, number>()
    const unsubscribers = new Map<string, Unsubscriber>()

    // this is ugly!
    dataManager.updateCallback = (dataMap) => {
        dataMap.forEach((fieldMap, messageName) => {
            fieldMap.forEach((fieldList, fieldName) => {
                const tweenedName = `${messageName}: ${fieldName}`

                if (!tweens.get(tweenedName)) {
                    const tween = tweened(0, { duration: 1000 })
                    const unsubscriber = tween.subscribe((value) => {
                        tweenValues.set(tweenedName, value)
                    })
                    tweens.set(tweenedName, tween)
                    unsubscribers.set(tweenedName, unsubscriber)
                }

                const tween = tweens.get(tweenedName)
                if (tween && fieldList.length > 0) {
                    tween.set(fieldList[fieldList.length - 1].value)
                }
            })
        })
        tweenValues = tweenValues
    }

    onDestroy(() => {
        /** Unsubscribe from everything when the component is unmounted */
        unsubscribers.forEach((unsubscriber) => {
            unsubscriber()
        })
        dataManager.destroy()
    })
</script>

<div class="flex flex-col gap-2 m-2">
    {#each tweenValues as [name, value]}
        <div class="flex flex-row items-center justify-between">
            <p class="whitespace-nowrap">{name} {value.toFixed(2)} (%)</p>
            <progress class="progress w-56" {value} max="100" />
        </div>
    {/each}
</div>
