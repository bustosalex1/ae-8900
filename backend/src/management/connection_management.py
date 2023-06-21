"""
Connection management... stuff for my AE 8900 backend.

I don't really think this is the best place to put this but... I also don't want to put it in the
websocket router file.
"""
import asyncio
from typing import List

from fastapi import WebSocket

from src.data_processing.daq import DataManager


class ConnectionManager:
    """
    The ConnectionManager manages websocket connections to the backend.

    It allows multiple parties to connect to the backend and receive websocket data.
    """

    def __init__(self, data_manager: DataManager):
        """
        Create a new ConnectionManager instance.

        There should only be one ConnectionManager while the backend is running. The
        ConnectionManager also contains a reference to the data_manager, since it accesses the
        data_manager's queue to send messages.
        """
        self.active_connections: List[WebSocket] = []
        self.stop_event = asyncio.Event()
        self.data_manager = data_manager
        self.task = None

    async def connect(self, websocket: WebSocket) -> None:
        """Handle a new WebSocket connection to the backend."""
        await websocket.accept()
        self.active_connections.append(websocket)

        self.stop_event.clear()
        self.task = asyncio.create_task(self.broadcast_task())

    async def disconnect(self, websocket: WebSocket) -> None:
        """Handle a websocket disconnection from the backend."""
        self.active_connections.remove(websocket)

        if len(self.active_connections) == 0:
            for _, stream in self.data_manager.sources.items():
                await stream.stop()
            self.stop_event.set()
            self.task.cancel()
            self.task = None

    async def send(self, message: str, websocket: WebSocket):
        """Send a message to a specific websocket connection."""
        await websocket.send_text(message)

    async def broadcast(self, message: str) -> None:
        """Send a message to all active connections."""
        for connection in self.active_connections:
            await connection.send_text(message)

    async def broadcast_task(self) -> None:
        """Coroutine to broadcast messages to all available websockets."""
        while not self.stop_event.is_set():
            measurement = await self.data_manager.queue.get()
            await self.broadcast(measurement.json())
