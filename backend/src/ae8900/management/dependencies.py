"""Dependencies that can be used with FastAPI dependency injection for... safety or something."""
import logging
from typing import Annotated

from fastapi import Depends

from ae8900.data_processing import daq
from ae8900.management import connection_management
from ae8900.management.project_management import BACKEND_DIR
from ae8900.models import core

# set up managers, which should only be initialized once for a backend instance.
data_manager = daq.DataManager()
connection_manager = connection_management.ConnectionManager(data_manager=data_manager)

# initialize project-wide settings and pull in environment files
project_settings = core.ProjectSettings(
    _env_file=BACKEND_DIR.parent / ".env",
    _env_file_encoding="utf-8",
    active_project_directory=None,
)


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


def get_settings() -> core.ProjectSettings:
    """Dependency for project settings."""
    return project_settings


logging.warning((get_settings()))

# cool type hinting, even with dependencies, apparently
ConnectionManagerDependency = Annotated[connection_management.ConnectionManager, Depends(get_connection_manager)]
DataManagerDependency = Annotated[daq.DataManager, Depends(get_data_manager)]
ProjectSettingsDependency = Annotated[core.ProjectSettings, Depends(get_settings)]
