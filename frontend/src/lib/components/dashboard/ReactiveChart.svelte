<script lang="ts">
	import * as echarts from 'echarts';
	import { onMount } from 'svelte/internal';
	export const key = 'ReactiveChart';

	let chartDOM: HTMLElement;
	let option: echarts.EChartsCoreOption;
	let myChart: echarts.ECharts;
	let w: number;
	let h: number;

	let data: any[] = [];
	onMount(() => {
		let ws = new WebSocket('ws://localhost:8000/ws');

		ws.onmessage = (event) => {
			const message = JSON.parse(event.data);
			const timestamp = new Date(message.timestamp * 1000);
			const newData = [timestamp, message.data];
			if (data.length > 200) {
				data.shift();
			}
			data.push(newData);
			myChart &&
				myChart.setOption({
					series: [
						{
							data: data
						}
					]
				});
		};

		myChart = echarts.init(chartDOM, undefined, { width: 600, height: 400 });
		option = {
			xAxis: {
				type: 'time',
				splitLine: {
					show: false
				},
				min: new Date(Date.now() - 1000 * 60 * 1),
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
			]
		};

		myChart.setOption(option);
	});

	$: myChart && myChart.resize({ width: w, height: h });
</script>

<div class="w-full h-96" bind:clientWidth={w} bind:clientHeight={h}>
	<div bind:this={chartDOM} />
</div>
