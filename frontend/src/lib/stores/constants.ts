/**
 * @module Not technically stores, but I have decided to keep constants here... for now.
 */
import * as dashboard from '$lib/components/dashboard'

export const themes = {
	light: 'bumblebee',
	dark: 'dracula'
}

// insane that this works
export const dashboardMap = Object.entries(dashboard)
