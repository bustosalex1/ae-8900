"""Websocket endpoints for my AE 8900 backend API."""
from datetime import datetime

from fastapi import APIRouter, WebSocket

from src.data_processing import daq
from src.models import core

router = APIRouter()
dm = daq.DataManager()


@router.get("/websocket_types")
def websocket_types() -> core.Measurement:
    """Just an endpoint so that the Measurement type will show up in the openapi.json."""
    return core.Measurement(name="sample", value=0, timestamp=datetime.now())


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """Just an endpoint to test out websocket connections."""
    await websocket.accept()

    source1 = daq.DataStream(
        name="CPU",
        callback=daq.get_cpu,
        interval=0.1,
    )

    source2 = daq.DataStream(
        name="RAM",
        callback=daq.get_ram,
        interval=1,
    )
    dm.subscribe(source1)
    dm.subscribe(source2)

    while True:
        measurement = await dm.queue.get()
        measurement_dict = measurement.dict()
        measurement_dict["timestamp"] = measurement_dict["timestamp"].isoformat()
        await websocket.send_json(measurement_dict, mode="text")
