"""Data acquisition for my AE 8900 backend."""
import asyncio
import csv
from datetime import datetime
from pathlib import Path
from typing import Callable, Dict, List

from src.data_processing import measurement_callbacks
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
        :param callback: The callback that the DataStream will execute whenever making a measurement. Callbacks take no arguments and return a measurement value.
        :param interval: The interval in seconds at which to sample. For example, interval=0.1 would sample 10 times every second.
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
        if self.task:
            await self.task
        self.task = None


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
    stop_recording_event: asyncio.Event
    recording_task: asyncio.Task
    queue: asyncio.Queue[core.Measurement]

    def __init__(self, sources: List[DataStream] = [], cache_size: int = 1000) -> None:
        """Create a new DataManager instance."""
        # initialize builtin sources
        self.sources = {}
        builtins = [
            DataStream(name="CPU", callback=measurement_callbacks.get_cpu, interval=0.1),
            DataStream(name="RAM", callback=measurement_callbacks.get_ram, interval=0.1),
            DataStream(name="Thermal", callback=measurement_callbacks.get_cpu_temp, interval=5),
        ]

        for source in builtins:
            self.sources[source.name] = source

        # initialize the rest of the stuff
        for source in sources:
            self.sources[source.name] = source

        self.queue = asyncio.Queue(maxsize=cache_size)
        self.stop_recording_event = asyncio.Event()

    def subscribe(self, stream: DataStream):
        """Register a new data stream with the Data Manager."""
        if not self.sources.get(stream.name):
            self.sources[stream.name] = stream
            stream.start(queue=self.queue)

    def start_stream(self, stream_name: str) -> None:
        """
        Start a stream based on its key.

        :param stream_name: the key of the DataStream to start.
        """
        if stream := self.sources.get(stream_name):
            stream.start(queue=self.queue)

    async def stop_stream(self, stream_name: str) -> None:
        """
        Stop a stream based on its key.

        :param stream_name: the key of the DataStream to stop.
        """
        if stream := self.sources.get(stream_name):
            await stream.stop()
            print(f"successfully stopped stream: {stream_name}")

    async def unsubscribe(self, stream_name: str):
        """Remove a data stream from the Data Manager."""
        if stream := self.sources.pop(stream_name, None):
            await stream.stop()

    def start_recording(self, sources: List[str], filepath: Path, interval: float = 1):
        """Start recording data from a specified set of sources."""
        if self.stop_recording_event.is_set():
            self.stop_recording_event.clear()

        self.recording_task = asyncio.create_task(self.record(sources, filepath, interval))

    async def stop_recording(self):
        """Stop data recording task."""
        self.stop_recording_event.set()
        await self.recording_task

    async def record(self, sources: List, filepath: Path, interval: float):
        """Record task."""
        # gather up all the callbacks
        callbacks = []
        for source in sources:
            if stream := self.sources.get(source):
                callbacks.append(stream.callback)

        # and add a timestamp column
        sources.insert(0, "timestamp")

        batch_size = 100
        measurements = []

        try:
            with open(filepath, "w") as csvfile:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow(sources)

                while not self.stop_recording_event.is_set():
                    measurement_row = [datetime.now()]
                    for callback in callbacks:
                        measurement_row.append(callback())
                    measurements.append(measurement_row)

                    if len(measurements) >= batch_size:
                        print("batching measurements")
                        csvwriter.writerows(measurements)
                        measurements.clear()

                    await asyncio.sleep(interval)
                csvfile.close()
        finally:
            with open(filepath, "a") as csvfile:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerows(measurements)
                csvfile.close()

            print(f"finished recording at {filepath}")
