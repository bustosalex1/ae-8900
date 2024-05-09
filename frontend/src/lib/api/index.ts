import createClient from 'openapi-fetch'
import { PUBLIC_HOST_IP } from '$env/static/public'
import type { paths, components } from './schema'

const baseUrl = PUBLIC_HOST_IP || 'localhost'
console.log(baseUrl)
export const { get, post, put, del } = createClient<paths>({ baseUrl: `http://${baseUrl}:8000` })

// basically wraps an API call to make it safe. If the server returns an error code, or if there is
// a network error, this will handle it and process the errors in the same way. Which right now is
// just console.logging them lol
export const apiCall = async <T>(
    apiFunction: Promise<{ data?: T; error?: any; response?: Response }>
): Promise<T | undefined> => {
    try {
        const { data, error, response } = await apiFunction

        if (error || !response || response.status >= 400) {
            console.error(`Server Error: ${error}`)
            return undefined
        }
        return data
    } catch (e) {
        if (e instanceof TypeError) {
            console.error(e)
        } else {
            console.error(`Unknown Error: ${e}`)
        }
        return undefined
    }
}
/** types that are important enough to create aliases for */
export type ProjectConfiguration = components['schemas']['ProjectConfiguration']
export type ProjectMetadata = components['schemas']['ProjectMetadata']
export type ComponentConfiguration = components['schemas']['ComponentConfiguration']
export type ComponentSettings = components['schemas']['ComponentSettings']
export type PanelConfiguration = components['schemas']['PanelConfiguration']
export type ProjectState = components['schemas']['ProjectState']
export type Field = {
    name: string
    value: number
    units?: string | undefined
    timestamp: Date
}
export type FieldConfiguration = components['schemas']['FieldConfiguration']
export type MessageConfiguration = components['schemas']['MessageConfiguration']

/**
 * I can feel this getting convoluted, so for my own sake, a RawMessage is one that is parsed
 * straight from JSON -- i.e., it only contains JSON serializable objects, no Dates or anything.
 */
export type RawMessage = components['schemas']['Message']
export type Header = Omit<components['schemas']['Header'], 'timestamp'> & { timestamp: Date }

/**
 * A Message, in contrast to a RawMessage, is basically a RawMessage that has been parsed into more
 * usable information. Right now that just entails converting the timestamp from an ISO8601 string
 * to a Date.
 */
export type Message = Omit<RawMessage, 'header'> & { header: Header }

export type KeyFilter<T, U> = {
    [K in keyof T]: T[K] extends U ? K : never
}[keyof T]
