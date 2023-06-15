<script lang="ts">
    import * as echarts from 'echarts'
    import { onMount, onDestroy } from 'svelte/internal'
    export const key = 'ReactiveChart'

    let chartDOM: HTMLElement
    let option: echarts.EChartsCoreOption
    let myChart: echarts.ECharts
    let w: number
    let h: number
    let ws: WebSocket
    let data: any[] = []
    onMount(() => {
        ws = new WebSocket('ws://localhost:8000/ws')

        ws.onmessage = (event) => {
            const message = JSON.parse(event.data)
            const timestamp = new Date(message.timestamp * 1000)
            const newData = [timestamp, message.data]
            if (data.length > 2000) {
                data.shift()
            }
            data.push(newData)
            myChart &&
                myChart.setOption({
                    series: [
                        {
                            data: data
                        }
                    ]
                })
        }

        myChart = echarts.init(chartDOM, undefined, { width: 600, height: 400 })
        option = {
            xAxis: {
                type: 'time',
                splitLine: {
                    show: false
                },
                name: 'Time'
            },
            yAxis: {
                type: 'value',
                name: 'Voltage',
                boundaryGap: [0, '100%'],
                splitLine: {
                    show: false
                }
            },
            animation: false,
            series: [
                {
                    name: 'Fake Data',
                    type: 'line',
                    showSymbol: false,
                    data: data
                }
            ],
            dataZoom: [
                {
                    id: 'dataZoomX',
                    type: 'slider',
                    realtime: true,
                    startValue: new Date(Date.now() - 1000 * 60 * 1),
                    endValue: new Date(Date.now()),
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

    onDestroy(() => {
        ws.close()
    })

    $: myChart && myChart.resize({ width: w, height: h })
</script>

<div class="w-full h-96" bind:clientWidth={w} bind:clientHeight={h}>
    <div bind:this={chartDOM} />
</div>
