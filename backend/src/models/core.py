"""Main Pydantic models for my AE-8900 Backend."""
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class ComponentConfiguration(BaseModel):
    """Defines a configuration for a single dashboard component."""

    title: str
    component: str
    expanded: bool


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
    value: float
    timestamp: datetime
