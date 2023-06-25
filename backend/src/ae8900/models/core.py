"""Main Pydantic models for my AE-8900 Backend."""
from datetime import datetime
from pathlib import Path
from typing import List, Optional

from pydantic import BaseModel, BaseSettings, Field


class ComponentSettings(BaseModel):
    """Defines generic settings for a single dashboard component."""

    data_sources: List[str]


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


class Measurement(BaseModel):
    """Defines a single measurement value taken at a particular time."""

    name: str
    value: float | int
    units: str | None
    timestamp: datetime

    class Config:
        """Config options for the Measurement model."""

        json_encoders = {datetime: lambda value: value.isoformat()}


class ProjectSettings(BaseSettings):
    """Project wide backend settings."""

    active_project_directory: Path | None
    host_ip: str | None = Field(default=None, env="PUBLIC_HOST_IP")