"""Websocket connection management... stuff for my AE 8900 backend."""
import asyncio
import logging
from typing import List

from fastapi import WebSocket

from ae8900.data_processing import daq

logger = logging.getLogger(__name__)


class ConnectionManager:
    """
    The ConnectionManager manages websocket connections to the backend.

    It allows multiple parties to connect to the backend and receive websocket data.
    """

    # a list of all the active websocket connections to the backend.
    _active_connections: List[WebSocket]

    # the ConnectionManager's broadcast task, which will run as long as there is at least one connection to the backend.
    _task: asyncio.Task | None

    # the event that can be set to stop the ConnectionManager from broadcasting messages.
    _stop_event: asyncio.Event

    # a reference to the DataManager instance.
    _data_manager: daq.DataManager

    def __init__(self, data_manager: daq.DataManager):
        """
        Create a new ConnectionManager instance.

        There should only be one ConnectionManager while the backend is running. The
        ConnectionManager also contains a reference to the DataManager, since it accesses the
        DataManager's queue to send messages.
        """
        self._active_connections = []
        self._stop_event = asyncio.Event()
        self._data_manager = data_manager
        self._task = None

    async def connect(self, websocket: WebSocket) -> None:
        """
        Handle a new WebSocket connection to the backend.

        :param websocket: the new connection to accept.
        """
        await websocket.accept()
        self._active_connections.append(websocket)

        if self._stop_event.is_set():
            self._stop_event.clear()

        if self._task is None:
            self._task = asyncio.create_task(self.broadcast_task())

    async def disconnect(self, websocket: WebSocket) -> None:
        """
        Handle a websocket disconnection from the backend.

        :param websocket: the connection to disconnect.
        """
        self._active_connections.remove(websocket)

        if len(self._active_connections) == 0:
            logger.info(f"No active connections, stopping measurement coroutines.")
            for stream in self._data_manager.sources.values():
                await stream.stop()
            self._stop_event.set()
            self._task.cancel()

            if self._task:
                self._task = None

        logger.info(f"Stopped measurement and broadcast coroutines.")

    async def broadcast(self, message: str) -> None:
        """
        Send a message to all active connections.

        :param message: the message to send.
        """
        for connection in self._active_connections:
            await connection.send_text(message)

    async def broadcast_task(self) -> None:
        """Coroutine to broadcast messages to all available websockets."""
        while not self._stop_event.is_set():
            # basically wait until a message is available in the queue
            message = await self._data_manager.queue.get()

            # and then send the message
            await self.broadcast(message.json())
