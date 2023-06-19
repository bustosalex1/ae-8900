<script lang="ts">
    import * as echarts from 'echarts'
    import { onMount } from 'svelte/internal'
    import { connectionManager } from '$lib/websocket/connectionManager'

    let dataStore = connectionManager.measurementQueues.get('CPU')
    let ramStore = connectionManager.measurementQueues.get('RAM')
    let userInteracting = false
    let chartDOM: HTMLElement
    let option: echarts.EChartsCoreOption
    let myChart: echarts.ECharts
    let w: number
    let h: number

    let data = $dataStore ? $dataStore : []
    let ramData = $ramStore ? $ramStore : []

    onMount(() => {
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
                name: 'CPU Usage (%)',
                min: 0,
                max: 100,
                boundaryGap: [0, '100%'],
                splitLine: {
                    show: false
                }
            },
            animation: false,
            series: [
                {
                    name: 'CPU',
                    type: 'line',
                    symbol: 'none',
                    showSymbol: false,
                    data: data
                },
                {
                    name: 'RAM',
                    type: 'line',
                    symbol: 'none',
                    showSymbol: false,
                    data: ramData
                }
            ],
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

    $: myChart && myChart.resize({ width: w, height: h })

    $: if (!userInteracting) {
        myChart &&
            myChart.setOption(
                {
                    series: [
                        {
                            data: $dataStore
                        },
                        {
                            data: $ramStore
                        }
                    ]
                },
                { notMerge: false, lazyUpdate: true }
            )
    }
</script>

<div
    class="w-full h-96"
    bind:clientWidth={w}
    bind:clientHeight={h}
    on:mousedown={() => (userInteracting = true)}
    on:mouseup={() => (userInteracting = false)}
>
    <div bind:this={chartDOM} />
</div>
