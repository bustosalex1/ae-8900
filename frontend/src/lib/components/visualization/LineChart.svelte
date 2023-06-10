<script lang="ts">
	import * as echarts from 'echarts';
	import { onMount } from 'svelte/internal';

	let chartDOM: HTMLElement;
	let option: echarts.EChartsCoreOption;
	let myChart: echarts.ECharts;
	let w: number;
	let h: number;

	onMount(() => {
		myChart = echarts.init(chartDOM, undefined, { width: 600, height: 400 });
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
					smooth: true
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
		};

		myChart.setOption(option);
	});

	$: myChart && myChart.resize({ width: w, height: h });
</script>

<div class="w-full h-96" bind:clientWidth={w} bind:clientHeight={h}>
	<div bind:this={chartDOM} />
</div>
