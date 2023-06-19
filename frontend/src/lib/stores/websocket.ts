import { writable } from 'svelte/store'
import type { Measurement } from '$lib/api'
export const createMeasurementStore = () => {
    const { subscribe, set, update } = writable<Measurement[]>([])

    const shift = () =>
        update((queue: Measurement[]) => {
            queue.shift()
            return queue
        })

    const append = (measurement: Measurement) => {
        update((queue: Measurement[]) => {
            queue.push(measurement)
            return queue
        })
    }

    return {
        subscribe,
        set,
        update,
        shift,
        append
    }
}
