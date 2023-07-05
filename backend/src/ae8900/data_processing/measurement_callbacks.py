"""Functions that can be called by a DataStream to make a measurement."""
from typing import List

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
