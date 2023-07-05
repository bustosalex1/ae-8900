"""Core Pydantic models for my AE8900 Backend."""
from datetime import datetime
from pathlib import Path
from typing import List, Optional

from pydantic import BaseModel, BaseSettings, Field

from ae8900.models import websocket


class ComponentSettings(BaseModel):
    """Defines generic settings for a single dashboard component."""

    data_sources: List[websocket.MessageConfiguration]


class ComponentConfiguration(BaseModel):
    """Defines a configuration for a single dashboard component."""

    title: str
    component: str
    expanded: bool
    settings: ComponentSettings


class PanelConfiguration(BaseModel):
    """Defines a configuration for a single panel, which contains a list of components."""

    title: str
    components: List[ComponentConfiguration]


class ProjectConfiguration(BaseModel):
    """
    Defines a configuration for an entire project layout.

    Projects are composed of panels, which are in turn composed of components.
    """

    title: str
    description: str
    panels: List[PanelConfiguration]
    vertical: bool


class ProjectMetadata(BaseModel):
    """Contains relevant information about a project, such as its folder location, that is not managed by the user."""

    filepath: str
    last_modified: datetime


class ProjectState(BaseModel):
    """Defines the state of a project, which is composed of its configuration, and its metadata."""

    configuration: ProjectConfiguration
    metadata: Optional[ProjectMetadata]


class Settings(BaseSettings):
    """Settings that are generally useful across the backend."""

    # the absolute path of the project that is currently active on the frontend
    active_project_directory: Path | None

    # this comes from an environment variable... for now. If none, the server is deployed to
    # localhost. If it is some value, the server is deployed to that IP instead.
    host_ip: str | None = Field(default=None, env="PUBLIC_HOST_IP")

    # whether or not the system is recording
    recording: bool


class RecordingRequest(BaseModel):
    """Request parameters for a new recording."""

    sources: List[str]
    interval: float
