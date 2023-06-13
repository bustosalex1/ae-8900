import yaml
from pathlib import Path
import src.types.core as core


def load_project(filepath: Path) -> None:
    with open(filepath, "r") as file:
        data = yaml.safe_load(file)

    core.ProjectConfiguration(
        title=data["title"],
        vertical=data["vertical"],
        panels=data["panels"],
    )
