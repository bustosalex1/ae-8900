export class ConnectionManager {
	private websocket: WebSocket

	constructor(url: string) {
		this.websocket = new WebSocket(url)

		this.websocket.onmessage = (event: MessageEvent<any>) => {
			// sort messages here!
		}
	}
}
