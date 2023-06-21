import { writable } from 'svelte/store'
import { apiCall, put, type Measurement } from '$lib/api'

/**
 * A measurement store is basically a store that contains a list of messages of a certain type, or
 * name, that correspond to a DataStream on the backend. Measurement stores make use of the
 * StartStopNotifier in stores to notify the backend to start generating measurements when there is
 * at least one subscriber to the store on the frontend, and stop taking measurements when there are
 * no longer subscribers on the frontend.
 */
export const createMeasurementStore = (name: string) => {
    const { subscribe, set, update } = writable<Measurement[]>([], () => {
        console.log(`${name} has subscribers`)
        apiCall(
            put('/start_stream/{stream_name}', {
                params: {
                    path: {
                        stream_name: name
                    }
                }
            })
        )
        return () => {
            console.log(`${name} has no more subscribers`)
            set([])
            put('/stop_stream/{stream_name}', {
                params: {
                    path: {
                        stream_name: name
                    }
                }
            })
        }
    })

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
