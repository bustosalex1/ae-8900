import { writable } from 'svelte/store'
import type { ProjectConfiguration } from '$lib/api'

const createProjectState = () => {
    const defaultState: ProjectConfiguration = {
        title: 'Project State',
        vertical: true,
        panels: [
            {
                title: 'Example Panel',
                components: [
                    {
                        title: 'Voltage, or Something',
                        component: 'ReactiveChart'
                    },
                    {
                        title: 'Power',
                        component: 'LineChart'
                    },
                    {
                        title: 'Websocket',
                        component: 'Websocket'
                    }
                ]
            }
        ]
    }

    const { subscribe, set, update } = writable<ProjectConfiguration>(defaultState)

    return {
        subscribe,
        set,
        update
    }
}

export const projectState = createProjectState()
