import type { Measurement } from '$lib/api'
import type { Writable } from 'svelte/store'
import { createMeasurementStore } from '$lib/stores'

const cacheSize = 5000

class ConnectionManager {
    private websocket: WebSocket
    public measurementQueues: Map<string, Writable<Measurement[]>>

    constructor(url: string) {
        this.websocket = new WebSocket(url)
        this.measurementQueues = new Map<string, Writable<Measurement[]>>()

        this.websocket.onmessage = (event: MessageEvent<string>) => {
            const message = JSON.parse(event.data)
            const eChartsMessage: Measurement = [message.timestamp, message.value]

            if (!this.measurementQueues.has(message.name)) {
                this.measurementQueues.set(message.name, createMeasurementStore())
            }

            this.measurementQueues.get(message.name)?.update((queue: Measurement[]) => {
                if (queue.length > cacheSize) {
                    queue.shift()
                }
                queue.push(eChartsMessage)
                return queue
            })
        }
    }
}

export const connectionManager = new ConnectionManager('ws://localhost:8000/ws')
