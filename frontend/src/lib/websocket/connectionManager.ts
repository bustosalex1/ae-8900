export class ConnectionManager {
    private websocket: WebSocket

    constructor(url: string) {
        this.websocket = new WebSocket(url)

        this.websocket.onmessage = (event: MessageEvent<any>) => {
            console.log(event)
            // sort messages here!
        }
    }
}
