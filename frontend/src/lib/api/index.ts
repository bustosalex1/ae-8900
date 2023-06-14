import createClient from 'openapi-fetch'
import type { paths, components } from './schema'

export const { get, post } = createClient<paths>({ baseUrl: 'http://localhost:8000' })

export const apiCall = async <T>(apiFunction: () => Promise<T>): Promise<T | null> => {
	try {
		return await apiFunction()
	} catch (error) {
		console.log('Network error: ', error)
		return null
	}
}

/** types that are important enough to create aliases for */
export type ProjectConfiguration = components['schemas']['ProjectConfiguration']
export type ComponentConfiguration = components['schemas']['ComponentConfiguration']
export type PanelConfiguration = components['schemas']['PanelConfiguration']
