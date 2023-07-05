"""Endpoints that are mostly relevant to websockets for my AE 8900 backend."""
from datetime import datetime
from typing import List

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from websockets.exceptions import (ConnectionClosed, ConnectionClosedError,
                                   ConnectionClosedOK)

from ae8900.infrastructure.dependencies import (ConnectionManagerDependency,
                                                DataManagerDependency)
from ae8900.models import websocket

router = APIRouter()


@router.get("/websocket_types")
def websocket_types() -> websocket.Message:
    """Just an endpoint so that the Measurement type will show up in the openapi.json."""
    pass


@router.get("/data_sources")
def data_sources(data_manager: DataManagerDependency) -> List[websocket.MessageConfiguration]:
    """
    Get the available data streams and their component fields.

    In order to accomplish this, I am executing each data stream's callback once, which... I feel
    like has the potential to be problematic in the future. Perhaps something to revisit.
    """
    sources: List[websocket.MessageConfiguration] = []
    for source, stream in data_manager.sources.items():
        sources.append(
            websocket.MessageConfiguration(
                header=websocket.Header(
                    name=source,
                    timestamp=datetime.now(),
                ),
                payload=[
                    websocket.FieldConfiguration(
                        name=field.name,
                        units=field.units,
                        enabled=False,
                    )
                    for field in stream.callback()
                ],
            )
        )

    return sources


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
