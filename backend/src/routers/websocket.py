"""Websocket endpoints for my AE 8900 backend API."""
from datetime import datetime

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from websockets.exceptions import (ConnectionClosed, ConnectionClosedError,
                                   ConnectionClosedOK)

from src.management.dependencies import ConnectionManagerDependency
from src.models import core

router = APIRouter()


@router.get("/websocket_types")
def websocket_types() -> core.Measurement:
    """Just an endpoint so that the Measurement type will show up in the openapi.json."""
    return core.Measurement(name="sample", value=0, timestamp=datetime.now())


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, connection_manager: ConnectionManagerDependency):
    """Just an endpoint to test out websocket connections."""
    try:
        await connection_manager.connect(websocket)
        while True:
            # I'm not expecting any text from connections at the moment, this is just to keep the connection open.
            await websocket.receive_text()
    except (ConnectionClosed, ConnectionClosedOK, ConnectionClosedError, WebSocketDisconnect):
        await connection_manager.disconnect(websocket)
