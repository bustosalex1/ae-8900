import { writable, get } from 'svelte/store'
import { apiCall, put, type ProjectState, post } from '$lib/api'
import { deepCopy } from '$lib/utils'

const createProjectState = () => {
    const defaultState: ProjectState = {
        configuration: {
            title: 'Project State',
            description: '',
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
        },
        metadata: undefined
    }

    const { subscribe, set, update } = writable<ProjectState>(defaultState)

    return {
        subscribe,
        set,
        update
    }
}

export const projectState = createProjectState()
export const stagedState = createProjectState()

export const revertProjectChanges = () => {
    stagedState.set(deepCopy(get(projectState)))
}

export const applyProjectChanges = async () => {
    const state = get(stagedState)
    let updatedState: ProjectState | undefined = undefined
    if (state.metadata) {
        updatedState = await apiCall(
            put('/project/', {
                body: state
            })
        )
    } else {
        updatedState = await apiCall(
            post('/project/', {
                body: state
            })
        )
    }

    if (updatedState) {
        projectState.set(updatedState)
        revertProjectChanges()
    }
}

export const setActiveProject = (project: ProjectState) => {
    projectState.set(deepCopy(project))
    stagedState.set(deepCopy(project))
}
