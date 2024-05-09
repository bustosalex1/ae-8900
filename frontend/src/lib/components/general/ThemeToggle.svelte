<script lang="ts">
    import { onMount } from 'svelte'
    import { themeChange } from 'theme-change'
    import { themes } from '$lib/stores'
    import Icon from './Icon.svelte'

    onMount(() => {
        themeChange(false)
    })
</script>

<!--@component
A simple theme toggle designed to be used with a themes object containing a light and dark
attribute. These attributes should map to daisyUI themes. ThemeToggle takes no arguments and can be
used like:
```tsx
<ThemeToggle />
```
-->

<label class="swap swap-rotate">
    <!-- this hidden checkbox controls the state -->
    <input
        type="checkbox"
        data-toggle-theme={`${themes.dark},${themes.light}`}
        data-active-class="ACTIVECLASS"
    />

    <!-- sun icon -->
    <Icon name="sun" class="feather swap-on fill-current" />

    <!-- moon icon -->
    <Icon name="moon" class="feather swap-off fill-current" />
</label>
