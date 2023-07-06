"""Functions that can be called by a DataStream to make a measurement."""
from typing import Callable, List

import daqhats
import psutil

from ae8900.models.websocket import PayloadField


def get_cpu() -> List[PayloadField]:
    """Get the CPU utilization as a percent."""
    payload = [
        PayloadField(
            name="CPU",
            value=psutil.cpu_percent(),
            units="%",
        )
    ]
    return payload


def get_ram() -> List[PayloadField]:
    """Get the RAM utilization as a percent."""
    payload = [
        PayloadField(
            name="RAM",
            value=psutil.virtual_memory().percent,
            units="%",
        )
    ]
    return payload


def get_cpu_temp() -> List[PayloadField]:
    """
    Get CPU Temperature in degrees Celsius.

    Supports Thinkpads and Raspberry Pis only!
    """
    value = 0
    try:
        value = psutil.sensors_temperatures()["thinkpad"][0].current
    except Exception:
        value = psutil.sensors_temperatures()["cpu_thermal"][0].current

    payload = [
        PayloadField(
            name="CPU",
            value=value,
            units="°C",
        )
    ]

    return payload


def get_system_status() -> List[PayloadField]:
    """
    Get system parameters.

    Basically a test to demonstrate new multi-field capabilities.
    """
    payload = [
        PayloadField(
            name="CPU",
            value=psutil.cpu_percent(),
            units="%",
        ),
        PayloadField(
            name="RAM",
            value=psutil.virtual_memory().percent,
            units="%",
        ),
    ]

    return payload


def get_daq_channel(channel: int = 0) -> Callable[[], List[PayloadField]]:
    def callback() -> List[PayloadField]:
        board = daqhats.mcc118(daqhats.hat_list(filter_by_id=daqhats.HatIDs.ANY)[0])
        payload = [
            PayloadField(
                name="Channel",
                value=board.a_in_read(channel),
                units="V",
            )
        ]

        return payload

    return callback
