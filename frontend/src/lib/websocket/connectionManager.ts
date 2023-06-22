import { apiCall, get, type Measurement } from '$lib/api'
import { PUBLIC_HOST_IP } from '$env/static/public'
import type { Unsubscriber, Writable } from 'svelte/store'
import { createMeasurementStore } from '$lib/stores'

/**
 * Manages a WebSocket connection to the AE 8900 backend. This will begin a connection on page load,
 * and persist it. I think. Additionally, it will take messges and sort them from a single stream of
 * data into a bunch of stores of message lists based on the type of message, so that components on
 * the frontend can subscribe to particular message topics as appropriate.
 */
class ConnectionManager {
    private websocket: WebSocket
    public measurementQueues: Map<string, Writable<Measurement[]>>
    public cacheSize: number

    /**
     * @param url - the websocket URL to connect to
     * @param cacheSize - the number of milliseconds corresponding to the oldest messages to keep.
     * For example, a cacheSize of 60,000 would keep messages as old as 1 minute ago, and as new
     * messages arrive the ConnectionManager will begin to discard messages older than 1 minute.
     */
    constructor(url: string, cacheSize: number) {
        this.websocket = new WebSocket(url)
        this.cacheSize = cacheSize
        this.measurementQueues = new Map<string, Writable<Measurement[]>>()

        // setup the callback to handle new messages as they arrive
        this.websocket.onmessage = (event: MessageEvent<string>) => {
            const message = JSON.parse(event.data)
            const eChartsMessage: Measurement = [new Date(message.timestamp), message.value]

            if (!this.measurementQueues.has(message.name)) {
                this.measurementQueues.set(message.name, createMeasurementStore(message.name))
            }

            this.measurementQueues.get(message.name)?.update((queue: Measurement[]) => {
                if (queue.length >= 1) {
                    if (Date.now() - queue[0][0].valueOf() > this.cacheSize) {
                        queue.shift()
                    }
                }
                queue.push(eChartsMessage)
                return queue
            })
        }
    }

    getMeasurementStream(name: string) {
        return this.measurementQueues.get(name)
    }

    /** Create measurement stores for all data sources provided by the backend. */
    async syncSources() {
        const sources = await apiCall(get('/data_sources', {}))

        if (sources) {
            for (const source of sources) {
                this.measurementQueues.set(source, createMeasurementStore(source))
            }
        }
    }

    /** Get a list of all the available data sources provided by the backend */
    sources() {
        return [...this.measurementQueues.keys()]
    }
}

const baseURL = PUBLIC_HOST_IP || 'localhost'
export const connectionManager = new ConnectionManager(`ws://${baseURL}:8000/ws`, 1000 * 60 * 3)

/** This seems... wrong. or bad. */
await connectionManager.syncSources()

/**
 * A class for dynamically managing WebSocket data inside of individual components. Basically, this
 * class ensures that any data sources (string keys corresponding to a particular connectionManager store),
 * are either subscribed to or unsubscribed from whenever they are added or removed from the
 * component. It also prevents duplicate sources from being troublesome.
 */
export class ComponentDataManager {
    sources: string[]
    unsubscribers: Map<string, Unsubscriber>
    dataMap: Map<string, Measurement[]>
    updateCallback: ((dataMap: Map<string, Measurement[]>) => void) | undefined
    constructor(sources: string[]) {
        this.sources = [...new Set(sources)]
        this.unsubscribers = new Map<string, Unsubscriber>()
        this.dataMap = new Map<string, Measurement[]>()
    }

    onSourceChange(sources: string[]) {
        // remove duplicates
        this.sources = [...new Set(sources)]

        // unsubscribe from any sources that have been removed
        this.unsubscribers.forEach((unsubscribe: Unsubscriber, source) => {
            if (!this.sources.includes(source)) {
                unsubscribe()
                this.unsubscribers.delete(source)
                this.dataMap.delete(source)
            }
        })

        // subscribe to any new sources
        sources.forEach((source) => {
            if (!this.unsubscribers.has(source)) {
                const store = connectionManager.getMeasurementStream(source)
                if (store) {
                    const unsubscribe = store.subscribe((data) => {
                        this.dataMap.set(source, data)
                        this.updateCallback && this.updateCallback(this.dataMap)
                    })

                    this.unsubscribers.set(source, unsubscribe)
                }
            }
        })
    }

    destroy() {
        this.unsubscribers.forEach((unsubscribe) => unsubscribe())
    }
}
