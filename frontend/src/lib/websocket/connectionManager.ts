import {
    apiCall,
    get,
    type Field,
    type Message,
    type RawMessage,
    type MessageConfiguration
} from '$lib/api'
import { PUBLIC_HOST_IP } from '$env/static/public'
import type { Unsubscriber } from 'svelte/store'
import { createMeasurementStore, type MessageStore } from '$lib/stores'

/**
 * Manages a WebSocket connection to the AE 8900 backend. This will begin a connection on page load,
 * and persist it. I think. Additionally, it will take messges and sort them from a single stream of
 * data into a bunch of stores of message lists based on the type of message, so that components on
 * the frontend can subscribe to particular message topics as appropriate.
 */
class ConnectionManager {
    private websocket: WebSocket
    public messageQueues: Map<string, MessageStore>
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
        this.messageQueues = new Map<string, MessageStore>()

        // setup the callback to handle new messages as they arrive
        this.websocket.onmessage = (event: MessageEvent<string>) => {
            // first parse out the message from the JSON
            const rawMessage: RawMessage = JSON.parse(event.data)

            // then parse out the date in this... pretty ugly way
            const message: Message = {
                ...rawMessage,
                header: { ...rawMessage.header, timestamp: new Date(rawMessage.header.timestamp) }
            }

            // if a store for this type of message does not already exist in the connection manager, create a new one.
            if (!this.messageQueues.has(message.header.name)) {
                this.messageQueues.set(message.header.name, createMeasurementStore(message))
            }

            // then split up the message into its component fields and add them into the appropriate areas.
            this.messageQueues
                .get(message.header.name)
                ?.update((queueMap: Map<string, Field[]>) => {
                    // basically, iterate over each field in the message payload...
                    for (const field of message.payload) {
                        const queue = queueMap.get(field.name)

                        // ... and for each field queue, check if the queue should get shortened...
                        if (queue) {
                            if (
                                queue.length >= 1 &&
                                Date.now() - queue[0].timestamp.valueOf() > this.cacheSize
                            ) {
                                queue.shift()
                            }

                            //... and then finally append the new field to the queue.
                            queue.push({ ...field, timestamp: message.header.timestamp })
                        } else {
                            // this is necessary if you (meaning me) want to clear out queues when there are no more subscribers.
                            queueMap.set(field.name, [])
                        }
                    }

                    return queueMap
                })

            this.messageQueues.get(message.header.name)?.updateLatest(message)
        }
    }

    getMeasurementStream(name: string) {
        return this.messageQueues.get(name)
    }

    /** Create measurement stores for all data sources provided by the backend. */
    async syncSources() {
        const sources = await apiCall(get('/data_sources', {}))

        if (sources) {
            for (const source of sources) {
                this.messageQueues.set(source.header.name, createMeasurementStore(source))
            }
        }
    }

    /** Get a list of all the available data sources provided by the backend */
    async sources() {
        const sources = await apiCall(get('/data_sources', {}))

        return sources
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
    // a list of all the string keys that correspond to DataStreams
    public sources: MessageConfiguration[]

    // a map of Unsubscriber objects, so that sources can be manually unsubscribed from when the map is updated
    private unsubscribers: Map<string, Unsubscriber>

    // uhhhh ummm
    public dataMap: Map<string, Map<string, Field[]>>

    // user definable ummmmm
    public updateCallback: ((dataMap: Map<string, Map<string, Field[]>>) => void) | undefined

    constructor(sources: MessageConfiguration[]) {
        this.sources = sources
        this.unsubscribers = new Map<string, Unsubscriber>()
        this.dataMap = new Map<string, Map<string, Field[]>>()
        this.onSourceChange(this.sources)
    }

    onSourceChange(sources: MessageConfiguration[]) {
        // remove duplicates
        this.sources = [...new Set(sources)]

        // unsubscribe from any sources that have been removed
        this.unsubscribers.forEach((unsubscribe: Unsubscriber, source) => {
            if (
                !this.sources.find(
                    (MessageConfiguration) => MessageConfiguration.header.name === source
                )
            ) {
                unsubscribe()
                this.unsubscribers.delete(source)
                this.dataMap.delete(source)
            }
        })

        // subscribe to any new sources
        for (const source of sources) {
            // if the source is not already registered...
            if (!this.unsubscribers.has(source.header.name)) {
                // ... get it from the connection manager
                const store = connectionManager.getMeasurementStream(source.header.name)
                if (store) {
                    const unsubscribe = store.subscribe((data) => {
                        this.dataMap.set(source.header.name, data)
                        this.updateCallback && this.updateCallback(this.dataMap)
                    })

                    this.unsubscribers.set(source.header.name, unsubscribe)
                }
            }
        }
    }

    // this is moderately cursed
    getActiveFields() {
        const fields: [string, Field[]][] = []
        for (const [messageName, messageFields] of this.dataMap) {
            const messageConfig = this.sources.find((source) => source.header.name === messageName)
            for (const [fieldName, fieldList] of messageFields) {
                if (messageConfig) {
                    const fieldConfig = messageConfig.payload.find(
                        (field) => field.name === fieldName
                    )

                    if (fieldConfig && fieldConfig.enabled) {
                        fields.push([`${messageName}: ${fieldName}`, fieldList])
                    }
                }
            }
        }
        return fields
    }

    destroy() {
        this.unsubscribers.forEach((unsubscribe) => unsubscribe())
    }
}
