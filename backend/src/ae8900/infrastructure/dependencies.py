"""Dependencies that can be used with FastAPI dependency injection for... safety or something."""
import logging
from typing import Annotated

from fastapi import Depends

from ae8900.data_processing import daq
from ae8900.infrastructure import connection_management
from ae8900.infrastructure.project_management import BACKEND_DIR
from ae8900.infrastructure.utils import initialize_logging
from ae8900.models import core

# initialize logging for the application
initialize_logging(log_level=logging.DEBUG)

# initialize settings and pull in environment files.
_project_settings = core.Settings(
    _env_file=BACKEND_DIR.parent / ".env",
    _env_file_encoding="utf-8",
    active_project_directory=None,
    recording=False,
)

# alright so... I am setting up managers here. Managers are only initialized once for a backend
# instance. I feel like this is not the best way to do this, and by "this" I mean initializing these
# sort of instances that are kind of passed around and widely used in the codebase, but I also feel
# like I am not smart enough to fix these right now. For now this works, but it is probably worth
# revisiting in the future.
_data_manager = daq.DataManager(state=_project_settings)

# is this... dependency injection?
_connection_manager = connection_management.ConnectionManager(data_manager=_data_manager)


def get_data_manager() -> daq.DataManager:
    """
    Dependency for the data_manager.

    Basically add a DataManagerDependency as an endpoint parameter if you need to access something from the data_manager.
    """
    return _data_manager


def get_connection_manager() -> connection_management.ConnectionManager:
    """
    Dependency for the connection_manager.

    Same as the data_manager, add a ConnectionManagerDependency if you need to access something from the connection_manager.
    """
    return _connection_manager


def get_settings() -> core.Settings:
    """Dependency for settings."""
    return _project_settings


# cool type hinting, even with dependencies, apparently
ConnectionManagerDependency = Annotated[connection_management.ConnectionManager, Depends(get_connection_manager)]
DataManagerDependency = Annotated[daq.DataManager, Depends(get_data_manager)]
ProjectSettingsDependency = Annotated[core.Settings, Depends(get_settings)]
