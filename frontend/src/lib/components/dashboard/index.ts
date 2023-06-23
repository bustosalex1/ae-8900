import LineChart from './LineChart.svelte'
import ReactiveChart from './ReactiveChart.svelte'
import SystemStatus from './SystemStatus.svelte'
import RecordingStatus from './RecordingStatus.svelte'
import type { SvelteComponent } from 'svelte'

/**
 * A string to component mapping that is used to dynamically render layouts saved as YAML.
 */
export const componentRegistry: Record<string, typeof SvelteComponent<any>> = {
    LineChart: LineChart,
    ReactiveChart: ReactiveChart,
    SystemStatus: SystemStatus,
    RecordingStatus: RecordingStatus
}
