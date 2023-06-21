"""Functions that can be called by a DataStream to make a measurement."""
import psutil


def get_cpu() -> float:
    """Get the CPU utilization as a percent."""
    return psutil.cpu_percent()


def get_ram() -> float:
    """Get the RAM utilization as a percent."""
    return psutil.virtual_memory().percent
