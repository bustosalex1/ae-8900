<script lang="ts">
    import { Canvas } from '@threlte/core'
    import type { ComponentSettings } from '$lib/api'
    import Scene from './Scene.svelte'
    import { connectionManager } from '$lib/websocket/connectionManager'
    import type { Unsubscriber } from 'svelte/motion'
    import { onDestroy } from 'svelte'
    import { Euler, Quaternion } from 'three'

    export let settings: ComponentSettings

    let values = new Map<string, number>()

    let orientation = {
        x: 0,
        y: 0,
        z: 0
    }

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

    $: {
        const quat = new Quaternion(
            values.get('i'),
            values.get('j'),
            values.get('k'),
            values.get('Real')
        )
        const euler = new Euler().setFromQuaternion(quat)
        orientation.x = euler.x
        orientation.y = euler.y
        orientation.z = euler.z
    }

    onDestroy(() => {
        for (const unsubscribe of unsubscribers) {
            unsubscribe()
        }
    })
</script>

<div class="w-full h-[28rem]">
    <Canvas>
        <Scene x={orientation.x} y={orientation.y} z={orientation.z} />
    </Canvas>
</div>
