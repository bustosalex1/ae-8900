import { writable } from 'svelte/store'
import { apiCall, put, type Message, type Field, type MessageConfiguration } from '$lib/api'
import { tweened, type Tweened } from 'svelte/motion'

/**
 * A measurement store is basically a store that contains a list of messages of a certain type, or
 * name, that correspond to a DataStream on the backend. Measurement stores make use of the
 * StartStopNotifier in stores to notify the backend to start generating measurements when there is
 * at least one subscriber to the store on the frontend, and stop taking measurements when there are
 * no longer subscribers on the frontend.
 */
export const createMeasurementStore = (message: Message | MessageConfiguration) => {
    const { subscribe, set, update } = writable<Map<string, Field[]>>(
        new Map<string, Field[]>(),
        () => {
            console.log(`${message.header.name} has subscribers.`)
            apiCall(
                put('/start_stream/{stream_name}', {
                    params: {
                        path: {
                            stream_name: message.header.name
                        }
                    }
                })
            )
            return () => {
                console.log(`${message.header.name} has no more subscribers.`)

                // clear out messages, but retain the basic structure
                const cleanMap = new Map<string, Field[]>()
                for (const field of message.payload) {
                    cleanMap.set(field.name, [])
                }
                set(cleanMap)
                put('/stop_stream/{stream_name}', {
                    params: {
                        path: {
                            stream_name: message.header.name
                        }
                    }
                })
            }
        }
    )

    const latest = new Map<string, Tweened<number>>()

    const updateLatest = (message: Message) => {
        for (const { name, value } of message.payload) {
            latest.get(name)?.set(value)
        }
    }

    // initialize field lists
    update((queueMap) => {
        for (const field of message.payload) {
            queueMap.set(field.name, [])
            latest.set(field.name, tweened(0, { duration: 500 }))
        }

        return queueMap
    })

    return {
        subscribe,
        set,
        update,
        latest,
        updateLatest
    }
}

export type MessageStore = ReturnType<typeof createMeasurementStore>
