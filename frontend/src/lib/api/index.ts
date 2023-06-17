import createClient from 'openapi-fetch'
import type { paths, components } from './schema'
export const { get, post, put } = createClient<paths>({ baseUrl: 'http://localhost:8000' })

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
export type PanelConfiguration = components['schemas']['PanelConfiguration']
export type ProjectState = components['schemas']['ProjectState']

export type KeyFilter<T, U> = {
    [K in keyof T]: T[K] extends U ? K : never
}[keyof T]
