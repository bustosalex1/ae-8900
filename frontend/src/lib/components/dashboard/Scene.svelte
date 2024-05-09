<script lang="ts">
    import { T } from '@threlte/core'
    import { OrbitControls } from '@threlte/extras'
    import { degToRad } from 'three/src/math/MathUtils'
    import { interactivity } from '@threlte/extras'
    import Cubesat_1u from '$lib/assets/Cubesat_1u.svelte'
    import { spring } from 'svelte/motion'

    export let x: number | undefined
    export let y: number | undefined
    export let z: number | undefined

    interactivity()
    let rotation = spring(0)
    setInterval(() => {
        rotation.update((value) => value + 1)
    }, 1000)
</script>

<!-- Environment stuff, lights, camera, and whatnot -->
<T.PerspectiveCamera makeDefault position={[10, 10, 10]} fov={24}>
    <OrbitControls maxPolarAngle={degToRad(80)} enableZoom={true} />
</T.PerspectiveCamera>
<T.DirectionalLight castShadow position={[3, 10, 10]} />
<T.DirectionalLight position={[-10, 10, -10]} intensity={0.2} />
<T.AmbientLight intensity={0.2} />

<Cubesat_1u rotation.y={y} rotation.x={x} rotation.z={z} position.y={1} scale={1} castShadow />

<T.Group>
    <T.GridHelper />
</T.Group>
