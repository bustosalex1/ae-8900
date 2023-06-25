"""Websocket endpoints for my AE 8900 backend API."""
from datetime import datetime
from typing import List

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from websockets.exceptions import (ConnectionClosed, ConnectionClosedError,
                                   ConnectionClosedOK)

from ae8900.management.dependencies import (ConnectionManagerDependency,
                                            DataManagerDependency)
from ae8900.models import core

router = APIRouter()


@router.get("/websocket_types")
def websocket_types() -> core.Measurement:
    """Just an endpoint so that the Measurement type will show up in the openapi.json."""
    return core.Measurement(name="sample", value=0, timestamp=datetime.now())


@router.get("/data_sources")
def data_sources(data_manager: DataManagerDependency) -> List[str]:
    """Get the available DataStreams."""
    print(data_manager.sources)
    return list(data_manager.sources.keys())


@router.put("/start_stream/{stream_name}")
async def start_stream(stream_name: str, data_manager: DataManagerDependency) -> None:
    """
    Start collecting data from a stream.

    :param stream_name: the string key associated with the DataStream to start.
    """
    data_manager.start_stream(stream_name)


@router.put("/stop_stream/{stream_name}")
async def stop_stream(stream_name: str, data_manager: DataManagerDependency) -> None:
    """
    Stop data collection from a stream.

    :param stream_name: the string key associated with the DataStream to stop.
    """
    await data_manager.stop_stream(stream_name)


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
