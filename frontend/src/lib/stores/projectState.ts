import { writable } from 'svelte/store'
import type { ProjectConfiguration } from '$lib/types'
import ReactiveChart from '$lib/components/dashboard/ReactiveChart.svelte'
import LineChart from '$lib/components/dashboard/LineChart.svelte'
import Websocket from '$lib/components/dashboard/Websocket.svelte'

const createProjectState = () => {
	const defaultState: ProjectConfiguration = {
		vertical: true,
		panels: [
			{
				title: 'Example Panel',
				components: [
					{
						title: 'Voltage, or Something',
						component: ReactiveChart,
						props: {}
					},
					{
						title: 'Power',
						component: LineChart,
						props: {}
					},
					{
						title: 'Websocket',
						component: Websocket,
						props: {}
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
