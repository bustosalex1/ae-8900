"""Functions that can be called by a DataStream to make a measurement."""
import psutil


def get_cpu() -> float:
    """Get the CPU utilization as a percent."""
    return psutil.cpu_percent()


def get_ram() -> float:
    """Get the RAM utilization as a percent."""
    return psutil.virtual_memory().percent


def get_cpu_temp() -> float:
    """
    Get CPU Temperature in degrees Celsius.

    Supports Thinkpads and Raspberry Pis only!
    """
    value = 0
    try:
        value = psutil.sensors_temperatures()["thinkpad"][0].current
    except Exception:
        value = psutil.sensors_temperatures()["cpu_thermal"][0].current
    finally:
        return value
