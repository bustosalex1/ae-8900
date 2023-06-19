/**
 * @module Not technically stores, but I have decided to keep constants here... for now.
 */
import * as dashboard from '$lib/components/dashboard'

export const themes = {
    light: 'bumblebee',
    dark: 'dracula'
}

// for future reference, I made this a function because SvelteKit HMR would get mad if I tried to
// update components from the dashboard while running the development server. Not a huge deal but
// this seems to work around that.
export const getDashboardMap = () => Object.fromEntries(Object.entries(dashboard))
