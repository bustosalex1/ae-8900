<script lang="ts">
    import type { ComponentSettings } from '$lib/api'
    import * as echarts from 'echarts'
    import { onMount } from 'svelte'

    // comply with dashboard standard.
    export let settings: ComponentSettings

    /** ECharts variables */
    let chartDOM: HTMLElement
    let option: echarts.EChartsCoreOption
    let myChart: echarts.ECharts
    let w: number
    let h: number

    onMount(() => {
        console.log(`LineChart has unused ${settings} right now :)`)

        myChart = echarts.init(chartDOM, undefined, { width: 600, height: 400 })
        option = {
            xAxis: {
                type: 'category',
                data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
            },
            yAxis: {
                type: 'value'
            },
            series: [
                {
                    data: [150, 230, 224, 218, 135, 147, 260],
                    type: 'line',
                    smooth: true,
                    markLine: {
                        data: [{ type: 'average', name: 'Average', symbol: 'none', label: 'bruh' }],
                        symbol: 'none',
                        silent: true
                    }
                }
            ],
            dataZoom: [
                {
                    id: 'dataZoomX',
                    type: 'slider',
                    xAxisIndex: 0,
                    filterMode: 'filter'
                }
            ]
        }

        myChart.setOption(option)
    })

    $: myChart && myChart.resize({ width: w, height: h })
</script>

<div class="w-full h-96" bind:clientWidth={w} bind:clientHeight={h}>
    <div bind:this={chartDOM} />
</div>
