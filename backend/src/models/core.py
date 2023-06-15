"""Main Pydantic models for my AE-8900 Backend."""
from typing import List
from pydantic import BaseModel


class ComponentConfiguration(BaseModel):
    """Defines a configuration for a single dashboard component."""

    title: str
    component: str


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
