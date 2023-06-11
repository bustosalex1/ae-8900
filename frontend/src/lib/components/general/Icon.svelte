<script lang="ts">
	import '../../../app.css';
	let clazz: string | undefined = 'feather';
	export { clazz as class };
	export let name: string;
</script>

<svg class={`${clazz}`}>
	<use href={`/images/feather-sprite.svg#${name}`} />
</svg>
