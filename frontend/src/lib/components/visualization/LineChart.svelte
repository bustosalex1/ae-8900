<script lang="ts">
	import * as echarts from 'echarts';
	import { onMount } from 'svelte/internal';
	import Icon from '../general/Icon.svelte';

	let chartDOM: HTMLElement;
	let option;
	let myChart: echarts.ECharts;
	let w: number;
	let h: number;

	onMount(() => {
		console.log('bruh!');
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
					type: 'line'
				}
			]
		};

		myChart.setOption(option);
	});

	$: myChart && myChart.resize({ width: w, height: h });
</script>

<div class="w-full max-h-96" bind:clientWidth={w} bind:clientHeight={h}>
	{w} x {h}
	<Icon name="activity" />
	<div bind:this={chartDOM} />
</div>
