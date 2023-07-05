<script lang="ts">
    import * as echarts from 'echarts'
    import { onDestroy, onMount } from 'svelte'
    import type { ComponentSettings } from '$lib/api'
    import { ComponentDataManager } from '$lib/websocket/connectionManager'

    // comply with dashboard "standard"
    export let settings: ComponentSettings

    // data manager manages subscriptions dynamic websocket streams
    // the reason I am doing this right now is because I've realized that I'm unmounting and remounting the component every time I change the settings lol.
    const dataManager = new ComponentDataManager(settings.data_sources)
    $: dataManager.onSourceChange(settings.data_sources)

    /** ECharts stuff */
    let userInteracting = false
    let chartDOM: HTMLElement
    let option: echarts.EChartsCoreOption
    let myChart: echarts.ECharts
    let w: number
    let h: number

    /** sort of nice way to dynamically get websocket updates to ECharts */
    dataManager.updateCallback = (dataMap) => {
        const fields = dataManager.getActiveFields()
        myChart &&
            !userInteracting &&
            myChart.setOption({
                series: fields.map(([key, value]) => {
                    return {
                        name: key,
                        type: 'line',
                        data: value.map((field) => [field.timestamp, field.value]),
                        symbol: 'none',
                        showSymbol: false
                    }
                })
            })
    }

    onDestroy(() => {
        /** Unsubscribe from everything when the component is unmounted */
        dataManager.destroy()
    })

    onMount(async () => {
        /** initialize ECharts stuff */
        myChart = echarts.init(chartDOM, undefined, { width: 600, height: 400 })
        option = {
            legend: {},
            xAxis: {
                type: 'time',
                splitLine: {
                    show: false
                },
                name: 'Time'
            },
            yAxis: {
                type: 'value',
                name: '(%)',
                min: 0,
                max: 100,
                boundaryGap: [0, '100%'],
                splitLine: {
                    show: false
                }
            },
            animation: false,
            series: [],
            dataZoom: [
                {
                    id: 'dataZoomX',
                    type: 'slider',
                    realtime: true,
                    start: 0,
                    end: 100,
                    xAxisIndex: 0,
                    showDataShadow: false,
                    filterMode: 'empty'
                }
            ]
        }

        myChart.setOption(option)
    })

    // resize chart when panel changes
    $: myChart && myChart.resize({ width: w, height: h })
</script>

<div
    class="w-full h-96"
    role="presentation"
    bind:clientWidth={w}
    bind:clientHeight={h}
    on:mousedown={() => (userInteracting = true)}
    on:mouseup={() => (userInteracting = false)}
>
    <div bind:this={chartDOM} />
</div>
