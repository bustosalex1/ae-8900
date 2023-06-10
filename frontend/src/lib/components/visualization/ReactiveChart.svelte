<script lang="ts">
	import * as echarts from 'echarts';
	import { onMount } from 'svelte/internal';

	let chartDOM: HTMLElement;
	let option: echarts.EChartsCoreOption;
	let myChart: echarts.ECharts;
	let w: number;
	let h: number;

	function randomData() {
		now = new Date(+now + oneDay);
		value = value + Math.random() * 21 - 10;
		return {
			name: now.toString(),
			value: [[now.getFullYear(), now.getMonth() + 1, now.getDate()].join('/'), Math.round(value)]
		};
	}

	let data: any[] = [];
	let now = new Date(1997, 9, 3);
	let oneDay = 24 * 3600 * 1000;
	let value = Math.random() * 1000;
	for (let i = 0; i < 1000; i++) {
		data.push(randomData());
	}
	onMount(() => {
		myChart = echarts.init(chartDOM, undefined, { width: 600, height: 400 });
		option = {
			tooltip: {
				trigger: 'axis',
				formatter: function (params: any) {
					params = params[0];
					var date = new Date(params.name);
					return (
						date.getDate() +
						'/' +
						(date.getMonth() + 1) +
						'/' +
						date.getFullYear() +
						' : ' +
						params.value[1]
					);
				},
				axisPointer: {
					animation: false
				}
			},
			xAxis: {
				type: 'time',
				splitLine: {
					show: false
				}
			},
			yAxis: {
				type: 'value',
				boundaryGap: [0, '100%'],
				splitLine: {
					show: false
				}
			},
			series: [
				{
					name: 'Fake Data',
					type: 'line',
					showSymbol: false,
					data: data
				}
			]
		};
		setInterval(function () {
			data.shift();
			data.push(randomData());
			myChart.setOption({
				series: [
					{
						data: data
					}
				]
			});
		}, 250);

		myChart.setOption(option);
	});

	$: myChart && myChart.resize({ width: w, height: h });
</script>

<div class="w-full h-96" bind:clientWidth={w} bind:clientHeight={h}>
	<div bind:this={chartDOM} />
</div>
