"""Dependencies that can be used with FastAPI dependency injection for... safety or something."""
from typing import Annotated

from fastapi import Depends

from src.data_processing import daq
from src.management import connection_management

# set up managers, which should only be initialized once for a backend instance.
data_manager = daq.DataManager()
connection_manager = connection_management.ConnectionManager(data_manager=data_manager)


def get_data_manager() -> daq.DataManager:
    """
    Dependency for the data_manager.

    Basically add a DataManagerDependency as an endpoint parameter if you need to access something from the data_manager.
    """
    return data_manager


def get_connection_manager() -> connection_management.ConnectionManager:
    """
    Dependency for the connection_manager.

    Same as the data_manager, add a ConnectionManagerDependency if you need to access something from the connection_manager.
    """
    return connection_manager


# cool type hinting, even with dependencies, apparently
ConnectionManagerDependency = Annotated[connection_management.ConnectionManager, Depends(get_connection_manager)]
DataManagerDependency = Annotated[daq.DataManager, Depends(get_data_manager)]
