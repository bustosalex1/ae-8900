import createClient from 'openapi-fetch'
import type { paths } from './schema'

export const { get, post } = createClient<paths>({ baseUrl: 'http://localhost:8000' })
