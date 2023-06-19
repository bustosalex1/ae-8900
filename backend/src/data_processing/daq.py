"""Data acquisition for my AE 8900 backend."""
import asyncio
from datetime import datetime
from typing import Callable, Dict

import psutil

from src.models import core


class DataStream:
    """
    A DataStream represents a source of data measurements.

    Basically, a DataStream will query this data source asynchronously at a certain frequency,
    which can be specified for any particular DataStream, and then pass measurements into a Queue
    in the DataManager. Measurements in the DataManager queue are then made available to all other
    parts of the backend.
    """

    def __init__(
        self,
        name: str,
        callback: Callable[[], float | int],
        interval: float,
    ):
        """
        Create a new DataStream.

        :param name: The name associated with the DataStream. DataStreams should have unique names.
        :param callback: The callback that the DataStream will execute whenever making a measurement.
            Callbacks take no arguments and return a measurement value.
        :param interval: The interval in seconds at which to sample. For example, interval=0.1 would
            sample 10 times every second.
        """
        self.name = name
        self.callback = callback
        self.interval = interval
        self.stop_event = asyncio.Event()
        self.task: asyncio.Task | None = None
        pass

    async def measure(self, queue: asyncio.Queue):
        """
        Measure is... I want to say a coroutine that will run until the DataStream is signaled to stop.

        While the stop event is not set, measure will take a measurement every interval (where interval is specified when the DataStream is initialized.),
        and then place each measurement on the DataManager queue.

        :param queue: The DataManager queue, where the measurement will be placed.
        """
        while not self.stop_event.is_set():
            measurement = core.Measurement(
                name=self.name,
                timestamp=datetime.now(),
                value=self.callback(),
            )

            await queue.put(measurement)
            await asyncio.sleep(self.interval)

    def start(self, queue: asyncio.Queue) -> None:
        """
        Start a DataStream's measure coroutine.

        This async stuff is still foreign to me, but what I'm trying to do here is basically make
        sure the stop event is not set, and then create an async task for this DataStream's measure
        coroutine, which can then be run concurrently with other DataStreams... I think.

        :param queue: The DataManager's queue to pass through to measure()
        """
        if self.task is None:
            self.stop_event.clear()
            self.task = asyncio.create_task(self.measure(queue))

    async def stop(self) -> None:
        """
        Stop a DataStream's measure coroutine.

        This will set the stop event for the DataStream, and then wait for the task to wrap up, and
        finally discard the task.
        """
        self.stop_event.set()
        await self.task
        self.task = None


def get_cpu() -> float:
    """Get the CPU utilization as a percent."""
    return psutil.cpu_percent()


def get_ram() -> float:
    """Get the RAM utilization as a percent."""
    return psutil.virtual_memory().percent


class DataManager:
    """
    Manages data collection across different data sources asynchronously.

    There should only be one DataManager while the backend is running. The idea is that the
    DataManager will handle streams of data from various sources, which may be being sampled at
    different frequencies, and basically abstract away all of the weird async stuff involved, so
    that the rest of the application can just access a queue of tagged data corresponding to each
    source.
    """

    sources: Dict[str, DataStream]
    queue: asyncio.Queue[core.Measurement]

    def __init__(self):
        """Create a new DataManager instance."""
        self.sources = {}
        self.queue = asyncio.Queue(maxsize=1000)

    def subscribe(self, stream: DataStream):
        """Register a new data stream with the Data Manager."""
        if not self.sources.get(stream.name):
            self.sources[stream.name] = stream
            stream.start(queue=self.queue)

    async def unsubscribe(self, stream_name: str):
        """Remove a data stream from the Data Manager."""
        stream = self.sources.pop(stream_name, None)
        if stream:
            await stream.stop()
