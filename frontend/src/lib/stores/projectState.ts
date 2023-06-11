import { writable } from 'svelte/store'
import type { ProjectConfiguration } from '$lib/types'
import ReactiveChart from '$lib/components/visualization/ReactiveChart.svelte'
import LineChart from '$lib/components/visualization/LineChart.svelte'

const createProjectState = () => {
	const defaultState: ProjectConfiguration = {
		vertical: true,
		panels: [
			{
				title: 'Example Panel',
				components: [
					{
						title: 'Voltage, or something',
						component: ReactiveChart,
						props: {}
					},
					{
						title: 'Power',
						component: LineChart,
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
