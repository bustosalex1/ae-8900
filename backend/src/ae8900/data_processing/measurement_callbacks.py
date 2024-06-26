"""Functions that can be called by a DataStream to make a measurement."""
import struct
from typing import Callable, List

import daqhats
import psutil
import smbus2

from ae8900.models import core
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


def get_system_status(settings: core.Settings) -> Callable[[], List[PayloadField]]:
    def callback() -> List[PayloadField]:
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
            PayloadField(
                name="Recording",
                value=int(settings.recording),
                units=None,
            ),
        ]

        return payload

    return callback


def get_daq_channel(board: daqhats.mcc118, channel: int = 0) -> Callable[[], List[PayloadField]]:
    def callback() -> List[PayloadField]:
        payload = [
            PayloadField(
                name="Channel",
                value=board.a_in_read(channel),
                units="V",
            )
        ]

        return payload

    return callback


def get_imu(bus: smbus2.SMBus) -> Callable[[], List[PayloadField]]:
    def callback() -> List[PayloadField]:
        address = 0x10
        data_format = "ffff"
        num_bytes = struct.calcsize(data_format)
        data_bytes = bus.read_i2c_block_data(address, 0, num_bytes)
        real, i, j, k = struct.unpack(data_format, bytes(data_bytes))

        payload = [
            PayloadField(
                name="Real",
                value=real,
                units=None,
            ),
            PayloadField(
                name="i",
                value=i,
                units=None,
            ),
            PayloadField(
                name="j",
                value=j,
                units=None,
            ),
            PayloadField(
                name="k",
                value=k,
                units=None,
            ),
        ]

        return payload

    return callback
