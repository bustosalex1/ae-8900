from typing import List
from pydantic import BaseModel


class ComponentConfiguration(BaseModel):
    title: str
    component: str


class PanelConfiguration(BaseModel):
    title: str
    components: List[ComponentConfiguration]


class ProjectConfiguration(BaseModel):
    title: str
    panels: List[PanelConfiguration]
    vertical: bool
