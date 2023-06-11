export type SvelteComponent = any

export type ComponentConfiguration = {
	title: string
	component: SvelteComponent
	props: any
}

export type PanelConfiguration = {
	title: string
	components: ComponentConfiguration[]
}

export type ProjectConfiguration = {
	panels: PanelConfiguration[]
	vertical: boolean
}
